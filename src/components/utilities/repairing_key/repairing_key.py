from src.components.interfaces.points_sensor import PointsSensor
from src.constants import repairing_key_radar_cost, repairing_key_wall_cost, repairing_key_air_defense_cost
from src.states.state import State
from PIL import Image, ImageTk

class RepairingKey:
    def __init__(self, canvas, screen_width, screen_height, tool_panel):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tool_panel = tool_panel
        self.is_disabled = True

        self.point_sensor = PointsSensor(canvas, screen_width, screen_height)
        self.point_sensor.repairing_key = self

        self.active_img = ImageTk.PhotoImage(
            Image.open("C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/repairing_key/repairing-key.png")
            # TODO replace with relative path
        )
        self.disabled_img = ImageTk.PhotoImage(
            Image.open("C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/repairing_key/repairing-key-disabled.png")
            # TODO replace with relative path
        )
        self.repair_key = self.create()
        self.recalculate()

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        key = self.canvas.create_image(
            tp_x0 + 10, tp_y0 + 5,
            image=self.disabled_img, anchor="nw")

        if not self.is_disabled:
            self.canvas.itemconfig(key, image=self.active_img)

        return key

    def on_drag_start(self, event):
        if self.is_disabled:
            return

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        if self.is_disabled:
            return

        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.repair_key, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        if self.is_disabled:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.repair_key)

        self.__heal_wall_cell(x1, y1, x2, y2)
        self.__heal_radars(x1, y1, x2, y2)
        self.__heal_air_defense(x1, y1, x2, y2)

        self.__reset_repairing_key()

    def recalculate(self):
        self.is_disabled = self.point_sensor.counter < repairing_key_wall_cost
        if not self.is_disabled:
            self.canvas.itemconfig(self.repair_key, image=self.active_img)
        else:
            self.canvas.itemconfig(self.repair_key, image=self.disabled_img)

    def __heal_wall_cell(self, x1, y1, x2, y2):
        for cell in State().get_data("wall_cells"):
            cell_state = self.canvas.itemcget(cell, "state")
            if cell_state == "normal" or cell_state == '':
                continue

            cx1, cy1, cx2, cy2 = self.canvas.coords(cell)
            if x1 < cx2 and x2 > cx1 and y1 < cy2 and y2 > cy1:
                if self.point_sensor.counter >= repairing_key_wall_cost:
                    self.canvas.itemconfig(cell, state="normal")
                    self.point_sensor.decrease(repairing_key_wall_cost)
                    self.recalculate()
                self.__reset_repairing_key()
                return

    def __heal_radars(self, x1, y1, x2, y2):
        radars_for_healing = [
            radar for radar in State().get_data("radars")
                if len(self.canvas.coords(radar.radar["item"])) != 0
                    and radar.radar["hp"] == 1
        ]

        for radar in radars_for_healing:
            radar_object = radar.radar
            rx1, ry1, rx2, ry2 = self.canvas.coords(radar_object["item"])

            if x1 >= rx1 and x2 <= rx2 and y1 >= ry1 and y2 <= ry2:
                if self.point_sensor.counter >= repairing_key_radar_cost:
                    self.point_sensor.decrease(repairing_key_radar_cost)
                    self.recalculate()
                    radar.heal()

                self.__reset_repairing_key()

                return

    def __heal_air_defense(self, x1, y1, x2, y2):
        air_defense_for_healing = [
            air_device for air_device in State().get_data("air_defense")
            if len(self.canvas.coords(air_device.device["item"])) != 0
               and air_device.device["hp"] == 1
        ]

        for air_device in air_defense_for_healing:
            device_object = air_device.device

            dx1, dy1, dx2, dy2 = self.canvas.coords(device_object["item"])

            if x1 >= dx1 and x2 <= dx2 and y1 >= dy1 and y2 <= dy2:
                if self.point_sensor.counter >= repairing_key_air_defense_cost:
                    air_device.heal()
                    self.point_sensor.decrease(repairing_key_air_defense_cost)
                    self.recalculate()

                self.__reset_repairing_key()

                return

    def __reset_repairing_key(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        self.canvas.coords(self.repair_key,
                           tp_x0 + 10, tp_y0 + 5,
                           tp_x0 + 30, tp_y0 + 20)