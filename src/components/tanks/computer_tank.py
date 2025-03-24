import random
from src.components.letters.failing_letter import FallingLetter
from src.states.state import State
from PIL import Image, ImageTk

class ComputerTank:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        self.image = ImageTk.PhotoImage(Image.open("assets/tanks/computer_tank.png"))

        self.tank = self.canvas.create_image(0, 5, image=self.image, anchor="nw")

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

        letter = FallingLetter(self.canvas,
                               self.screen_height,
                               current_tank_position_x0)

        State().append("letters", letter)
        letter.move()