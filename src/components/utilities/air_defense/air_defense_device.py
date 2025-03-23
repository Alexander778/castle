from src.components.effects.explosion import Explosion
from PIL import Image, ImageTk

class AirDefenseDevice:
    def __init__(self, canvas, coordinates, colors, position):
        self.canvas = canvas

        self.coordinates = coordinates
        self.colors = colors
        self.position = position

        self.launch_pad_img = ImageTk.PhotoImage(
            Image.open(f"C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/launch-pad-{position}.png")
            # TODO replace with relative path
        )

        self.inactive_rocket_img = ImageTk.PhotoImage(
            Image.open(f"C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/air-defense-rocket-{position}-inactive.png")
            # TODO replace with relative path
        )

        self.device = self.create_device()

    def create_device(self):
        # device = self.canvas.create_rectangle(self.coordinates,
        #                                       fill=self.colors["fill"],
        #                                       outline=self.colors["outline"])

        device = self.canvas.create_image(self.coordinates[0], self.coordinates[1], image=self.launch_pad_img, anchor="nw")

        device_x0 = self.coordinates[0]
        device_y0 = self.coordinates[1]
        device_x1 = self.coordinates[2]
        device_y1 = self.coordinates[3]

        rocket_width = 5
        rocket_height = 10

        align_x_by_position = 25
        if self.position == "right":
            align_x_by_position = -10

        rocket_x0 = device_x0 + align_x_by_position

        rocket_y0 = device_y0
        rocket_x1 = rocket_x0 + rocket_width
        rocket_y1 = rocket_y0 + rocket_height

        rocket = self.canvas.create_image(rocket_x0, rocket_y0, image=self.inactive_rocket_img,
                                          anchor="nw")

        # rocket = self.canvas.create_rectangle(rocket_x0, rocket_y0,
        #                                             rocket_x1, rocket_y1,
        #                                             fill=self.colors["outline"],
        #                                             outline="black")
        return {
            "item": device,
            "rocket": rocket,
            "launch-pad-image": self.launch_pad_img,
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
            self.canvas.itemconfig(self.device["item"], fill="white")

    def hit(self):
        self.canvas.itemconfig(self.device["item"], fill="yellow")

        device_coordinates = self.canvas.coords(self.device["item"])
        Explosion(self.canvas).show(device_coordinates[0], device_coordinates[1])

    def destroy(self):
        self.canvas.delete(self.device["item"])
        self.canvas.delete(self.device["rocket"])