from src.components.effects.explosion import Explosion


class Radar:
    def __init__(self, canvas, screen_width, screen_height, radar_number):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radar_number = radar_number

        self.radar = self.create()

    def create(self):
        radar_action_range = self.screen_width / 4

        distance_to_next_radar = radar_action_range * (self.radar_number - 1)

        initial_x0 = (radar_action_range / 2.5) + distance_to_next_radar
        initial_x1 = initial_x0 + 100

        radar = self.canvas.create_rectangle(initial_x0, self.screen_height - 240,
                                                 initial_x1, self.screen_height - 215,
                                                 fill="lightgreen",
                                                 tags="target")

        range_x0 = distance_to_next_radar
        range_x1 = radar_action_range + range_x0

        # Todo remove ranges - testing purposes
        # self.canvas.create_text(range_x0, self.screen_height - 50, text=range_x0)
        # self.canvas.create_text(range_x1, self.screen_height - 50, text=range_x1)
        #

        return {
            "item": radar,
            "action_range": [
                range_x0,
                range_x1
            ],
            "hp": 2
        }

    def heal(self):
        if self.radar["hp"] == 1:
            self.radar["hp"] += 1
            self.canvas.itemconfig(self.radar["item"], fill="lightgreen")

    def hit(self):
        self.canvas.itemconfig(self.radar["item"], fill="yellow")

        radar_coordinates = self.canvas.coords(self.radar["item"])
        Explosion(self.canvas).show(radar_coordinates[0], radar_coordinates[1])

    def destroy(self):
        self.canvas.delete(self.radar["item"])

