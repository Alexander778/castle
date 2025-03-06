from src.components.storage.air_defense_storage import AirDefenseStorage
from src.components.storage.radar_storage import RadarStorage
from src.components.storage.wall_storage import WallStorage


class RepairingKey:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self._wall_storage = WallStorage()
        self._radar_storage = RadarStorage()
        self._air_defense_storage = AirDefenseStorage()

        self.repair_key = canvas.create_rectangle(
                screen_width / 2 - 80, screen_height - 65,
                screen_width / 2 - 60, screen_height - 50,
                fill="yellow",
                tags="draggable")

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def on_drag_start(self, event):
        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.repair_key, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        x1, y1, x2, y2 = self.canvas.coords(self.repair_key)

        self.__heal_wall_cell(x1, y1, x2, y2)
        self.__heal_radars(x1, y1, x2, y2)
        self.__heal_air_defense(x1, y1, x2, y2)

        self.canvas.coords(self.repair_key, self.screen_width / 2 - 80, self.screen_height - 65,
                           self.screen_width / 2 - 60, self.screen_height - 50)

    def __heal_wall_cell(self, x1, y1, x2, y2):
        for cell in self._wall_storage.get_data():

            if self.canvas.itemcget(cell, "state") == "normal":
                continue

            cx1, cy1, cx2, cy2 = self.canvas.coords(cell)
            if x1 < cx2 and x2 > cx1 and y1 < cy2 and y2 > cy1:
                self.canvas.itemconfig(cell, state="normal")
                self.__reset_repairing_key()
                return

    def __heal_radars(self, x1, y1, x2, y2):
        for radar in self._radar_storage.get_data():
            radar_object = radar.radar
            rx1, ry1, rx2, ry2 = self.canvas.coords(radar_object["item"])

            if x1 >= rx1 and x2 <= rx2 and y1 >= ry1 and y2 <= ry2:
                radar.heal()

                self.__reset_repairing_key()

                return

    def __heal_air_defense(self, x1, y1, x2, y2):
        for air_device in self._air_defense_storage.get_data():
            device_object = air_device.device

            dx1, dy1, dx2, dy2 = self.canvas.coords(device_object["item"])

            if x1 >= dx1 and x2 <= dx2 and y1 >= dy1 and y2 <= dy2:
                air_device.heal()

                self.__reset_repairing_key()

                return

    def __reset_repairing_key(self):
        self.canvas.coords(self.repair_key,
                           self.screen_width / 2 - 80, self.screen_height - 65,
                           self.screen_width / 2 - 60, self.screen_height - 50)