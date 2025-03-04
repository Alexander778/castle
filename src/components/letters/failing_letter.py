import random

from src.components.storage.falling_letter_storage import FallingLetterStorage
from src.constants import alphabet, small_letter_color, big_letter_color


class FallingLetter:
    def __init__(self, canvas, screen_height, tank_current_position_x0, launch_rocket):
        self.canvas = canvas
        self.screen_height = screen_height
        self.tank_current_position_x0 = tank_current_position_x0
        self.launch_rocket = launch_rocket
        self.letter_item = self.create()

        self._letter_storage = FallingLetterStorage()

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

        self.canvas.tag_bind(letter_item, "<Button-1>",
                             lambda event: self.launch_rocket(event, letter_item, is_uppercase))
        self.canvas.tag_bind(letter_item, "<Button-3>",
                             lambda event: self.launch_rocket(event, letter_item, is_uppercase))

        return letter_item

    def move(self):
        letter_x0, letter_y0 = self.canvas.coords(self.letter_item)

        if abs(letter_y0 - self.screen_height) < 100:
            self.destroy()
        else:
            self.canvas.move(self.letter_item, 0, 10)
            self.canvas.after(500, self.move)



            # # hit the radar
            # for radar in radars:
            #     if radar["hp"] != 0:
            #         radar_x, radar_y, _, _ = canvas.coords(radar["radar"])
            #
            #         if abs(letter_x - radar_x) <= 100 and abs(letter_y - radar_y) < 15:
            #             damaged_radar = radar["radar"]
            #             radar["hp"] -= 1
            #
            #             if radar["hp"] == 0:
            #                 canvas.delete(damaged_radar)
            #             if radar["hp"] == 1:
            #                 canvas.itemconfig(damaged_radar, fill="yellow")
            #
            #             canvas.delete(letter)
            #             falling_letters.remove(letter)
            #             return
            #
            # # hit the air defense
            # for air_defense in air_defenses:
            #     if air_defense["hp"] != 0:
            #         air_x, air_y, _, _ = canvas.coords(air_defense["item"])
            #
            #         if abs(letter_x - air_x) <= 100 and abs(letter_y - air_y) < 15:
            #             air = air_defense["item"]
            #             air["hp"] -= 1
            #
            #             if air["hp"] == 0:
            #                 canvas.delete(air)
            #             if air["hp"] == 1:
            #                 canvas.itemconfig(air, fill="yellow")
            #
            #             canvas.delete(letter)
            #             falling_letters.remove(letter)
            #             return
            #
            # # hit the wall
            # for wall_cell in wall_cells:
            #     wall_cell_x, wall_cell_y, _, _ = canvas.coords(wall_cell)
            #
            #     if abs(letter_x - wall_cell_x) < 15 and abs(letter_y - wall_cell_y) < 15:
            #         canvas.itemconfig(wall_cell, state="hidden")
            #         # wall_cells.remove(wall_cell)
            #
            #         canvas.delete(letter)
            #         falling_letters.remove(letter)
            #         return

    def destroy(self):
        self._letter_storage.remove(self)
        self.canvas.delete(self.letter_item)