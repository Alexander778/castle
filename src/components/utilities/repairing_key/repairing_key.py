from src.components.interfaces.points_sensor import PointsSensor
from src.constants import repairing_key_cost
from src.states.state import State

class RepairingKey:
    def __init__(self, canvas, screen_width, screen_height, tool_panel):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tool_panel = tool_panel
        self.is_disabled = True

        self.point_sensor = PointsSensor(canvas, screen_width, screen_height)
        self.point_sensor.repairing_key = self

        self.repair_key = self.create()
        self.recalculate_properties()

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        color = "gray"
        if not self.is_disabled:
            color = "yellow"

        return self.canvas.create_rectangle(
            tp_x0 + 10, tp_y0 + 5,
            tp_x0 + 30, tp_y0 + 20,
            fill=color,
            tags="draggable")

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

    def recalculate_properties(self):
        self.is_disabled = self.point_sensor.counter < repairing_key_cost
        if not self.is_disabled:
            self.canvas.itemconfig(self.repair_key, fill="yellow")
        else:
            self.canvas.itemconfig(self.repair_key, fill="gray")

    def __heal_wall_cell(self, x1, y1, x2, y2):
        for cell in State().get_data("wall_cells"):
            cell_state = self.canvas.itemcget(cell, "state")
            if cell_state == "normal" or cell_state == '':
                continue

            cx1, cy1, cx2, cy2 = self.canvas.coords(cell)
            if x1 < cx2 and x2 > cx1 and y1 < cy2 and y2 > cy1:
                self.canvas.itemconfig(cell, state="normal")
                self.point_sensor.decrease(repairing_key_cost)
                self.recalculate_properties()
                self.__reset_repairing_key()
                return

    def __heal_radars(self, x1, y1, x2, y2):
        radars_for_healing = [
            radar for radar in State().get_data("radars")
                if len(self.canvas.coords(radar.radar["item"])) != 0
                    and radar.radar["hp"] != 0
        ]

        for radar in radars_for_healing:
            radar_object = radar.radar
            rx1, ry1, rx2, ry2 = self.canvas.coords(radar_object["item"])

            if x1 >= rx1 and x2 <= rx2 and y1 >= ry1 and y2 <= ry2:
                radar.heal()

                self.__reset_repairing_key()

                return

    def __heal_air_defense(self, x1, y1, x2, y2):
        for air_device in State().get_data("air_defense"):
            device_object = air_device.device

            dx1, dy1, dx2, dy2 = self.canvas.coords(device_object["item"])

            if x1 >= dx1 and x2 <= dx2 and y1 >= dy1 and y2 <= dy2:
                air_device.heal()

                self.__reset_repairing_key()

                return

    def __reset_repairing_key(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        self.canvas.coords(self.repair_key,
                           tp_x0 + 10, tp_y0 + 5,
                           tp_x0 + 30, tp_y0 + 20)