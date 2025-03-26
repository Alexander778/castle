from src.components.effects.damage import Damage
from src.components.effects.explosion import Explosion
from PIL import Image, ImageTk

class Radar:
    def __init__(self, canvas, screen_width, screen_height, radar_number):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radar_number = radar_number

        self.image = ImageTk.PhotoImage(Image.open("assets/radar.png"))
        self.radar = self.create()
        self.damage_image_id = None

    def create(self):
        radar_action_range = self.screen_width / 4

        distance_to_next_radar = radar_action_range * (self.radar_number - 1)

        initial_x0 = (radar_action_range / 2.5) + distance_to_next_radar

        radar = self.canvas.create_image(initial_x0, self.screen_height - 265, image=self.image, anchor="nw")

        range_x0 = distance_to_next_radar
        range_x1 = radar_action_range + range_x0

        # Todo remove ranges - testing purposes
        # self.canvas.create_text(range_x0, self.screen_height - 50, text=range_x0)
        # self.canvas.create_text(range_x1, self.screen_height - 50, text=range_x1)
        #

        return {
            "item": radar,
            "image": self.image,
            "action_range": [
                range_x0,
                range_x1
            ],
            "hp": 2
        }

    def heal(self):
        if self.radar["hp"] == 1:
            self.radar["hp"] += 1
            Damage(self.canvas).hide(self.damage_image_id)

    def hit(self, hit_place_x0, hit_place_y0):
        radar_coordinates = self.canvas.coords(self.radar["item"])

        Explosion(self.canvas).show(hit_place_x0, hit_place_y0)
        self.damage_image_id = Damage(self.canvas).show(radar_coordinates[0], radar_coordinates[1])

    def destroy(self):
        Damage(self.canvas).hide(self.damage_image_id)
        self.canvas.delete(self.radar["item"])

