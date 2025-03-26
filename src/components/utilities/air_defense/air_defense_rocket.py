from src.components.effects.big_explosion import BigExplosion
from src.components.effects.explosion import Explosion
from PIL import Image, ImageTk
import math

class AirDefenseRocket:
    def __init__(self, canvas, coordinates, colors, position):
        self.canvas = canvas

        self.coordinates = coordinates
        self.colors = colors
        self.position = position

        self.rocket_pil_object = Image.open(f"assets/air_defense/air-defense-rocket-{position}-active.png")
        self.rocket_img = ImageTk.PhotoImage(self.rocket_pil_object)

        self.target_letter = None
        self.rocket = self.create_rocket()

    def create_rocket(self):
        rocket = self.canvas.create_image(self.coordinates[0], self.coordinates[1],
                                          image=self.rocket_img, anchor="nw")
        self.canvas.lower(rocket)
        return {
            "rocket": rocket,
            "has_target": False,
            "rocket_img": self.rocket_img,
            "hp": 2
        }

    def move_rocket(self, letter):
        letter_item = letter.letter_item
        rocket = self.rocket["rocket"]

        letter_exists = len(self.canvas.coords(letter_item)) != 0

        if letter_exists is False:
            self.destroy()
            return

        if self.target_letter is None:
            self.target_letter = letter
            self.rocket["has_target"] = True

        if self.target_letter is not letter:
            self.rocket["has_target"] = False
            return

        letter_x0, letter_y0 = self.canvas.coords(letter_item)
        rocket_x0, rocket_y0 = self.canvas.coords(rocket)

        if abs(rocket_x0 - letter_x0) <= 10 and abs(rocket_y0 - letter_y0) <= 5:
            BigExplosion(self.canvas).show(rocket_x0, rocket_y0, disappear_after_ms=1000)
            self.destroy()
            letter.destroy()
            return

        if rocket_y0 > 740:
            self.canvas.move(rocket, 0, -10)
            self.canvas.after(30, self.move_rocket, letter)
            return

        # Calculate angle (in radians) to target
        angle_in_degrees = math.degrees(math.atan2(letter_y0 - rocket_y0, letter_x0 - rocket_x0))
        angle_margin = 90
        if abs(rocket_x0 - letter_x0) >= 1500:
            angle_margin = 130
        angle = angle_in_degrees + angle_margin

        step_size = 10
        step_x = step_size * math.cos(math.radians(angle - 90))
        step_y = step_size * math.sin(math.radians(angle - 90))

        self.canvas.move(rocket, step_x, step_y)

        rotated_image = self.rocket_pil_object.rotate(-angle, expand=True)
        self.rocket_img = ImageTk.PhotoImage(rotated_image)

        self.canvas.itemconfig(rocket, image=self.rocket_img)

        self.canvas.after(30, self.move_rocket, letter)

    def heal(self):
        if self.rocket["hp"] == 1:
            self.rocket["hp"] += 1
            # self.canvas.itemconfig(self.device["item"], fill="white")

    def hit(self):
        rocket_coordinates = self.canvas.coords(self.rocket["rocket"])

        Explosion(self.canvas).show(rocket_coordinates[0], rocket_coordinates[1])

    def destroy(self):
        self.canvas.delete(self.rocket["rocket"])