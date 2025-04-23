from src.components.interfaces.points_sensor import PointsSensor
from src.states.state import State
from PIL import Image, ImageTk

class MedicinePack:
    def __init__(self, canvas, screen_width, screen_height, tool_panel):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tool_panel = tool_panel
        self.is_disabled = True

        self.point_sensor = PointsSensor(canvas, screen_width, screen_height)
        self.point_sensor.repairing_key = self

        self.active_img = ImageTk.PhotoImage(Image.open("../assets/medicine_pack/medicine_pack.png"))
        self.disabled_img = ImageTk.PhotoImage(Image.open("../assets/medicine_pack/medicine_pack_disabled.png"))

        self.img_width = self.active_img.width()
        self.img_height = self.active_img.height()

        medicine_cost = State().get_data("difficulty")["medicine_cost"]
        self.medicine_pack_wall_cost = medicine_cost["wall"]
        self.medicine_pack_radar_cost = medicine_cost["radar"]
        self.medicine_pack_air_defense_cost = medicine_cost["air_defence"]

        self.medicine_pack = self.create()
        self.recalculate()

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        pack = self.canvas.create_image(
            tp_x0 + 10, tp_y0 + 10,
            image=self.disabled_img, anchor="nw", tags="drag_medicine_pack")

        if not self.is_disabled:
            self.canvas.itemconfig(pack, image=self.active_img)

        return pack

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

        self.canvas.move(self.medicine_pack, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        if self.is_disabled:
            return

        x1, y1 = self.canvas.coords(self.medicine_pack)
        x2 = x1 + self.img_width
        y2 = y1 + self.img_height

        self.__heal_wall_cell(x1, y1, x2, y2)
        self.__heal_radars(x1, y1, x2, y2)
        self.__heal_air_defense(x1, y1, x2, y2)

        self.__reset()

    def recalculate(self):
        self.is_disabled = self.point_sensor.counter < self.medicine_pack_wall_cost
        if not self.is_disabled:
            self.canvas.itemconfig(self.medicine_pack, image=self.active_img)
        else:
            self.canvas.itemconfig(self.medicine_pack, image=self.disabled_img)

    def __heal_wall_cell(self, x1, y1, x2, y2):
        for cell in State().get_data("wall_cells"):
            cell_state = self.canvas.itemcget(cell, "state")
            if cell_state == "normal" or cell_state == '':
                continue

            # TODO move cell image width and height to constant or something
            cx1, cy1 = self.canvas.coords(cell)
            cx2 = cx1 + 26
            cy2 = cy1 + 15

            if x1 < cx2 and x2 > cx1 and y1 < cy2 and y2 > cy1:
                if self.point_sensor.counter >= self.medicine_pack_wall_cost:
                    self.canvas.itemconfig(cell, state="normal")
                    self.point_sensor.decrease(self.medicine_pack_wall_cost)
                    self.recalculate()
                self.__reset()
                return

    def __heal_radars(self, x1, y1, x2, y2):
        radars_for_healing = [
            radar for radar in State().get_data("radars")
                if len(self.canvas.coords(radar.radar["item"])) != 0
                    and radar.radar["hp"] == 1
        ]

        for radar in radars_for_healing:
            radar_object = radar.radar
            rx1, ry1 = self.canvas.coords(radar_object["item"])
            rx2 = rx1 + radar_object["image"].width()
            ry2 = ry1 + radar_object["image"].height()

            if x1 >= rx1 and x2 <= rx2 and y1 >= ry1 and y2 <= ry2:
                if self.point_sensor.counter >= self.medicine_pack_radar_cost:
                    self.point_sensor.decrease(self.medicine_pack_radar_cost)
                    self.recalculate()
                    radar.heal()

                self.__reset()

                return

    def __heal_air_defense(self, x1, y1, x2, y2):
        air_defense_for_healing = [
            air_device for air_device in State().get_data("air_defense")
            if len(self.canvas.coords(air_device.rocket["rocket"])) != 0
               and air_device.rocket["hp"] == 1
        ]

        for air_device in air_defense_for_healing:
            device_object = air_device.rocket

            dx1, dy1, dx2, dy2 = self.canvas.coords(device_object["rocket"])

            if x1 >= dx1 and x2 <= dx2 and y1 >= dy1 and y2 <= dy2:
                if self.point_sensor.counter >= self.medicine_pack_air_defense_cost:
                    air_device.heal()
                    self.point_sensor.decrease(self.medicine_pack_air_defense_cost)
                    self.recalculate()

                self.__reset()

                return

    def __reset(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        self.canvas.coords(self.medicine_pack, tp_x0 + 10, tp_y0 + 5)