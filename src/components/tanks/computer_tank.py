import random
from src.components.letters.failing_letter import FallingLetter
from src.components.storage.falling_letter_storage import FallingLetterStorage


class ComputerTank:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False
        self.tank = self.canvas.create_rectangle(
            0, 10,
            100, 40,
            fill='gray')

        self._letter_storage = FallingLetterStorage()

    def move_to_new_position(self):
        current_tank_position = self.canvas.coords(self.tank)
        current_tank_position_x0 = current_tank_position[0]

        if abs(current_tank_position_x0 - self.new_position_for_shot_x0) < 10:
            self.shot_letter()
            self.new_position_for_shot_x0 = random.randrange(0, self.screen_width - 100)

        if current_tank_position_x0 < self.new_position_for_shot_x0:
            self.canvas.move(self.tank, 10, 0)
            current_tank_position_x0 += 10
        else:
            self.canvas.move(self.tank, -10, 0)
            current_tank_position_x0 -= 10

        self.canvas.after(100, self.move_to_new_position)

    def shot_letter(self):
        current_tank_position = self.canvas.coords(self.tank)
        current_tank_position_x0 = current_tank_position[0]

        letter = FallingLetter(self.canvas, self.screen_height, current_tank_position_x0)

        self._letter_storage.append(letter)

        letter.move()