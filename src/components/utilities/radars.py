from src.components.utilities.radar import Radar
from src.states.state import State

class Radars:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas

        State().append_range("radars", [
            Radar(canvas, screen_width, screen_height, 1),
            Radar(canvas, screen_width, screen_height, 2),
            Radar(canvas, screen_width, screen_height, 3),
            Radar(canvas, screen_width, screen_height, 4)
        ])