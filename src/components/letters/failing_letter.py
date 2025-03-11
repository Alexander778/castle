import random

from src.components.storage.air_defense_storage import AirDefenseStorage
from src.components.storage.radar_storage import RadarStorage
from src.components.storage.wall_storage import WallStorage
from src.constants import alphabet, small_letter_color, big_letter_color


class FallingLetter:
    def __init__(self, canvas, screen_height, tank_current_position_x0, falling_letters):
        self.canvas = canvas
        self.screen_height = screen_height
        self.tank_current_position_x0 = tank_current_position_x0

        self.falling_letters = falling_letters

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

        if len(self.letter_coordinates) == 0:
            return

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
        self.falling_letters.remove(self)
        self.canvas.delete(self.letter_item)

    def __check_radars_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates
        potentially_damaged_radars = [
            radar for radar in self._radar_storage.get_data()
            if len(self.canvas.coords(radar.radar["item"])) != 0
            and self.canvas.coords(radar.radar["item"])[0] <= falling_letter_x0 <=
                self.canvas.coords(radar.radar["item"])[2]
            and radar.radar["hp"] != 0
        ]

        for radar in potentially_damaged_radars:
            radar_object = radar.radar
            radar_item = radar_object["item"]

            radar_x0, radar_y0, radar_x1, _ = self.canvas.coords(radar_item)

            if abs(falling_letter_y0 - radar_y0) < 15:
                radar_object["hp"] -= 1

                if radar_object["hp"] == 0:
                    radar.destroy()
                if radar_object["hp"] == 1:
                    radar.hit()

                self.destroy()
                return

    def __check_air_defense_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates
        potentially_damaged_air_defenses = [
            air_defense for air_defense in self._air_defense_storage.get_data()
            if len(self.canvas.coords(air_defense.device["item"])) != 0
            and self.canvas.coords(air_defense.device["item"])[0] <= falling_letter_x0 <=
               self.canvas.coords(air_defense.device["item"])[2]
            and air_defense.device["hp"] != 0
        ]

        for air_defense in potentially_damaged_air_defenses:
            air_device = air_defense.device
            air_x0, air_y0, _, _ = self.canvas.coords(air_device["item"])

            if abs(falling_letter_y0 - air_y0) < 15:
                air_device["hp"] -= 1

                if air_device["hp"] == 1:
                    air_defense.hit()

                if air_device["hp"] == 0:
                    air_defense.destroy()

                self.destroy()
                return

    def __check_wall_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates
        potentially_damaged_cells = [
            cell for cell in self._wall_storage.get_data()
            if abs(self.canvas.coords(cell)[0] - falling_letter_x0) <= 5
               and "hidden" not in self.canvas.itemcget(cell, "state")
        ]

        for cell in potentially_damaged_cells:
            cell_x0, cell_y0, _, _ = self.canvas.coords(cell)

            if abs(falling_letter_y0 - cell_y0) < 15:
                self.canvas.itemconfig(cell, state="hidden")
                self.destroy()
                return