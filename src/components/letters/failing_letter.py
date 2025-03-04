import random

from src.components.storage.air_defense_storage import AirDefenseStorage
from src.components.storage.falling_letter_storage import FallingLetterStorage
from src.components.storage.radar_storage import RadarStorage
from src.components.storage.wall_storage import WallStorage
from src.constants import alphabet, small_letter_color, big_letter_color


class FallingLetter:
    def __init__(self, canvas, screen_height, tank_current_position_x0):
        self.canvas = canvas
        self.screen_height = screen_height
        self.tank_current_position_x0 = tank_current_position_x0

        self._letter_storage = FallingLetterStorage()
        self._radar_storage = RadarStorage()
        self._wall_storage = WallStorage()
        self._air_defense_storage = AirDefenseStorage()

        self.letter_item = self.create()
        self.letter_coordinates = self.canvas.coords(self.letter_item)

    def create(self):
        is_uppercase = random.choice([True, False])
        letter_symbol = random.choice(alphabet)
        letter_symbol_color = small_letter_color

        if is_uppercase:
            letter_symbol = letter_symbol.upper()
            letter_symbol_color = big_letter_color

        letter_item = self.canvas.create_text(self.tank_current_position_x0 + 50, 60,
                                       text=letter_symbol,
                                       fill=letter_symbol_color)

        air_defence_devices = self._air_defense_storage.get_data()

        self.canvas.tag_bind(letter_item, "<Button-1>",
                             lambda event: air_defence_devices[1].move_rocket(self.letter_item))
        self.canvas.tag_bind(letter_item, "<Button-3>",
                             lambda event: air_defence_devices[0].move_rocket(self.letter_item))

        return letter_item

    def move(self):
        self.letter_coordinates = self.canvas.coords(self.letter_item)

        falling_letter_x0 = self.letter_coordinates[0]

        if abs(falling_letter_x0 - self.screen_height) < 100:
            self.destroy()
        else:
            self.canvas.move(self.letter_item, 0, 10)
            self.canvas.after(500, self.move)

            self.__check_radars_for_damage()
            self.__check_air_defense_for_damage()
            self.__check_wall_for_damage()

    def destroy(self):
        self._letter_storage.remove(self)
        self.canvas.delete(self.letter_item)

    def __check_radars_for_damage(self):
        for radar in self._radar_storage.get_data():
            if radar["hp"] == 0:
                return

            falling_letter_x0, falling_letter_y0 = self.letter_coordinates

            radar_item = radar["item"]
            radar_x0, radar_y0, radar_x1, _ = self.canvas.coords(radar_item)

            if abs(falling_letter_x0 - radar_x0) <= 100 and abs(falling_letter_y0 - radar_y0) < 15:
                radar["hp"] -= 1

                if radar["hp"] == 0:
                    self.canvas.delete(radar_item)
                if radar["hp"] == 1:
                    self.canvas.itemconfig(radar_item, fill="yellow")

                self.destroy()
                return

    def __check_air_defense_for_damage(self):
        for air_defense in self._air_defense_storage.get_data():
            air_device = air_defense.device
            if air_device["hp"] != 0:
                air_x0, air_y0, _, _ = self.canvas.coords(air_device["item"])
                falling_letter_x0, falling_letter_y0 = self.letter_coordinates

                if abs(falling_letter_x0 - air_x0) <= 50 and abs(falling_letter_y0 - air_y0) < 15:
                    air_device["hp"] -= 1

                    if air_device["hp"] == 0:
                        self.canvas.delete(air_device["item"])
                        self.canvas.delete(air_device["rocket"])
                    if air_defense["hp"] == 1:
                        self.canvas.itemconfig(air_device["item"], fill="yellow")

                    self.destroy()
                    return

    def __check_wall_for_damage(self):
        for cell in self._wall_storage.get_data():

            if self.canvas.itemcget(cell, "state") == "hidden":
                continue

            cell_x0, cell_y0, _, _ = self.canvas.coords(cell)
            falling_letter_x0, falling_letter_y0 = self.letter_coordinates

            if abs(falling_letter_x0 - cell_x0) < 15 and abs(falling_letter_y0 - cell_y0) < 15:
                self.canvas.itemconfig(cell, state="hidden")
                self.destroy()
                return