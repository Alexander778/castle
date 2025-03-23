from src.components.effects.damage import Damage
from src.components.effects.explosion import Explosion
from PIL import Image, ImageTk

class AirDefenseDevice:
    def __init__(self, canvas, coordinates, colors, position):
        self.canvas = canvas

        self.coordinates = coordinates
        self.colors = colors
        self.position = position

        self.inactive_rocket_img = ImageTk.PhotoImage(
            Image.open(f"C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/air-defense-rocket-{position}-inactive.png")
            # TODO replace with relative path
        )

        self.device = self.create_device()

    def create_device(self):
        rocket = self.canvas.create_image(self.coordinates[0], self.coordinates[1],
                                          image=self.inactive_rocket_img, anchor="nw")
        self.canvas.lower(rocket)
        return {
            "rocket": rocket,
            "rocket_img": self.inactive_rocket_img,
            "hp": 2
        }

    def move_rocket(self, letter):
        rocket = self.device["rocket"]

        letter_exists = len(self.canvas.coords(letter)) != 0

        if letter_exists is False:
            self.canvas.delete(rocket)

        letter_x0, letter_y0 = self.canvas.coords(letter)
        rocket_x0, rocket_y0, _, _ = self.canvas.coords(rocket)

        if abs(rocket_x0 - letter_x0) < 10 and abs(rocket_y0 - letter_y0) < 10:
            self.canvas.delete(rocket)
            self.canvas.delete(letter)
            return

        if rocket_y0 < 10:
            self.canvas.delete(rocket)
        else:
            step_x = 10 if rocket_x0 < letter_x0 else -10
            step_y = -10 if rocket_y0 > letter_y0 else 10

            self.canvas.move(rocket, step_x, step_y)
            self.canvas.after(100, self.move_rocket, letter)

    def heal(self):
        if self.device["hp"] == 1:
            self.device["hp"] += 1
            # self.canvas.itemconfig(self.device["item"], fill="white")

    def hit(self):
        launch_pad_coordinates = self.canvas.coords(self.device["launch_pad"])

        Explosion(self.canvas).show(launch_pad_coordinates[0], launch_pad_coordinates[1])
        Damage(self.canvas).show(launch_pad_coordinates[0], launch_pad_coordinates[1])

    def destroy(self):
        self.canvas.delete(self.device["item"])
        self.canvas.delete(self.device["rocket"])