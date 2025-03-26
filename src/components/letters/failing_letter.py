import random

from src.components.effects.explosion import Explosion
from src.constants import alphabet, small_letter_color, big_letter_color
from src.states.state import State


class FallingLetter:
    def __init__(self, canvas, screen_height, tank_current_position_x0):
        self.canvas = canvas
        self.screen_height = screen_height
        self.tank_current_position_x0 = tank_current_position_x0

        self.target_letter_circle = None
        self.letter_item = self.create()
        self.letter_coordinates = self.canvas.coords(self.letter_item)

    def create(self):
        is_uppercase = random.choice([True, False])
        letter_symbol = random.choice(alphabet)
        letter_symbol_color = small_letter_color

        if is_uppercase:
            letter_symbol = letter_symbol.upper()
            letter_symbol_color = big_letter_color

        letter_item = self.canvas.create_text(self.tank_current_position_x0 + 50, 75,
                                       text=letter_symbol,
                                       fill=letter_symbol_color,
                                       font=("Arial", 12, "bold"))

        air_defence_devices = State().get_data("air_defense")

        if is_uppercase:
            self.canvas.tag_bind(letter_item, "<Button-3>",
                                 lambda event: self.__launch_the_rocket(air_defence_devices[0],
                                                                        letter_item, letter_symbol_color))
        else:
            self.canvas.tag_bind(letter_item, "<Button-1>",
                             lambda event: self.__launch_the_rocket(air_defence_devices[1],
                                                                    letter_item, letter_symbol_color))

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

            if self.target_letter_circle is not None:
                self.canvas.move(self.target_letter_circle, 0, 10)

            self.canvas.after(500, self.move)

            self.__check_radars_for_damage()
            self.__check_air_defense_for_damage()
            self.__check_wall_for_damage()

    def destroy(self):
        State().remove("letters", self)
        self.canvas.delete(self.letter_item)
        self.canvas.delete(self.target_letter_circle)
        self.target_letter_circle = None

    def __check_radars_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates
        potentially_damaged_radars = [
            radar for radar in State().get_data("radars")
            if len(self.canvas.coords(radar.radar["item"])) != 0
            and self.canvas.coords(radar.radar["item"])[0] <= falling_letter_x0 <=
                self.canvas.coords(radar.radar["item"])[0] + radar.radar["image"].width()
            and radar.radar["hp"] != 0
        ]

        for radar in potentially_damaged_radars:
            radar_object = radar.radar
            radar_item = radar_object["item"]

            radar_x0, radar_y0 = self.canvas.coords(radar_item)

            if abs(falling_letter_y0 - radar_y0) < 15:
                radar_object["hp"] -= 1

                if radar_object["hp"] == 0:
                    radar.destroy()
                if radar_object["hp"] == 1:
                    radar.hit(falling_letter_x0, falling_letter_y0)

                self.destroy()
                return

    def __check_air_defense_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates

        potentially_damaged_air_defenses = [
            air_defense for air_defense in State().get_data("air_defense")
            if len(self.canvas.coords(air_defense.rocket["rocket"])) != 0
            and self.canvas.coords(air_defense.rocket["rocket"])[0] <= falling_letter_x0 <=
                   self.canvas.coords(air_defense.rocket["rocket"])[0]
               + air_defense.rocket["rocket_img"].width()
            and air_defense.rocket["hp"] != 0
        ]

        for air_defense in potentially_damaged_air_defenses:
            air_rocket = air_defense.rocket
            air_x0, air_y0 = self.canvas.coords(air_rocket["rocket"])

            if abs(falling_letter_y0 - air_y0) < 15:
                air_rocket["hp"] -= 1

                if air_rocket["hp"] == 1:
                    air_defense.hit()

                if air_rocket["hp"] == 0:
                    air_defense.destroy()

                self.destroy()
                return

    def __check_wall_for_damage(self):
        falling_letter_x0, falling_letter_y0 = self.letter_coordinates
        potentially_damaged_cells = [
            cell for cell in State().get_data("wall_cells")
            if abs(falling_letter_x0 - self.canvas.coords(cell)[0]) <= 15
               and "hidden" not in self.canvas.itemcget(cell, "state")
        ]

        for cell in potentially_damaged_cells:
            cell_x0, cell_y0 = self.canvas.coords(cell)

            if abs(falling_letter_y0 - cell_y0) <= 15:
                self.canvas.itemconfig(cell, state="hidden")
                Explosion(self.canvas).show(falling_letter_x0, falling_letter_y0 + 15)
                self.destroy()
                return

    def __launch_the_rocket(self, air_rocket, letter_item, color):
        air_rocket.move_rocket(self)
        if air_rocket.rocket["has_target"]:
            self.__target_letter(letter_item, color)

    def __target_letter(self, letter_item, color):
        if self.target_letter_circle is not None:
            return

        x1, y1, x2, y2 = self.canvas.bbox(letter_item)

        padding = 5
        width = (x2 - x1) + 2 * padding
        height = (y2 - y1) + 2 * padding
        diameter = max(width, height)

        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        x1 = x_center - diameter / 2
        y1 = y_center - diameter / 2
        x2 = x_center + diameter / 2
        y2 = y_center + diameter / 2

        self.target_letter_circle = self.canvas.create_oval(x1, y1, x2, y2, outline=color, width=2)