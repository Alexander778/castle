from src.components.effects.damage import Damage
from src.components.effects.explosion import Explosion
from PIL import Image, ImageTk
import math

class AirDefenseDevice:
    def __init__(self, canvas, coordinates, colors, position):
        self.canvas = canvas

        self.coordinates = coordinates
        self.colors = colors
        self.position = position

        self.rocket_pil_object = Image.open(f"assets/air_defense/air-defense-rocket-{position}-active.png")
        self.rocket_img = ImageTk.PhotoImage(self.rocket_pil_object)

        self.device = self.create_device()

    def create_device(self):
        rocket = self.canvas.create_image(self.coordinates[0], self.coordinates[1],
                                          image=self.rocket_img, anchor="nw")
        self.canvas.lower(rocket)
        return {
            "rocket": rocket,
            "rocket_img": self.rocket_img,
            "hp": 2
        }

    def move_rocket(self, letter):
        rocket = self.device["rocket"]

        letter_exists = len(self.canvas.coords(letter)) != 0

        if letter_exists is False:
            self.canvas.delete(rocket)
            return

        letter_x0, letter_y0 = self.canvas.coords(letter)
        rocket_x0, rocket_y0 = self.canvas.coords(rocket)

        if abs(rocket_x0 - letter_x0) < 5 and abs(rocket_y0 - letter_y0) < 5:
            self.canvas.delete(rocket)
            self.canvas.delete(letter)
            Explosion(self.canvas).show(rocket_x0, rocket_y0)
            return

        # Calculate angle (in radians) to target
        angle = math.degrees(math.atan2(letter_y0 - rocket_y0, letter_x0 - rocket_x0)) - 90

        # Compute smooth movement steps
        distance = math.hypot(letter_x0 - rocket_x0, letter_y0 - rocket_y0)
        step_size = min(10, int(distance / 5))

        step_x = step_size * math.cos(math.radians(angle + 90))
        step_y = step_size * math.sin(math.radians(angle + 90))

        self.canvas.move(rocket, step_x, step_y)

        rotated_image = self.rocket_pil_object.rotate(angle, expand=True)
        self.rocket_img = ImageTk.PhotoImage(rotated_image)

        self.canvas.itemconfig(rocket, image=self.rocket_img)

        self.canvas.after(30, self.move_rocket, letter)

    def heal(self):
        if self.device["hp"] == 1:
            self.device["hp"] += 1
            # self.canvas.itemconfig(self.device["item"], fill="white")

    def hit(self):
        rocket_coordinates = self.canvas.coords(self.device["rocket"])

        Explosion(self.canvas).show(rocket_coordinates[0], rocket_coordinates[1])

    def destroy(self):
        self.canvas.delete(self.device["rocket"])