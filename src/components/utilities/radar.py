class Radar:
    def __init__(self, canvas, screen_width, screen_height, radar_number):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radar_number = radar_number

        self.radar = self.create_radar()

    def create_radar(self):
        radar_action_range = self.screen_width / 4

        distance_to_next_radar = radar_action_range * (self.radar_number - 1)

        initial_x0 = (radar_action_range / 2.5) + distance_to_next_radar
        initial_x1 = initial_x0 + 100

        radar = self.canvas.create_rectangle(initial_x0, self.screen_height - 200,
                                                 initial_x1, self.screen_height - 185,
                                                 fill="lightgreen",
                                                 tags="target")

        print(initial_x0, self.screen_height - 200, initial_x1, self.screen_height - 185)

        range_x0 = distance_to_next_radar
        range_x1 = radar_action_range + range_x0

        # Todo remove ranges - testing purposes
        self.canvas.create_text(range_x0, self.screen_height - 50, text=range_x0)
        self.canvas.create_text(range_x1, self.screen_height - 50, text=range_x1)
        #

        return {
            "item": radar,
            "action_range": [
                range_x0,
                range_x1
            ],
            "hp": 2
        }