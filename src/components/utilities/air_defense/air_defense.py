from src.components.utilities.air_defense.air_defense_device import AirDefenseDevice
from src.constants import small_letter_color, big_letter_color
from src.states.state import State

class AirDefense:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas

        right_device = AirDefenseDevice(canvas,
                         coordinates=(screen_width - 65, screen_height - 270, screen_width - 70, screen_height - 240),
                         colors={"fill": "white", "outline": big_letter_color}, position="right")

        left_device = AirDefenseDevice(canvas,
                         coordinates=(35, screen_height - 270, 75, screen_height - 240),
                         colors={"fill": "white", "outline": small_letter_color}, position="left")

        State().append("air_defense", right_device)
        State().append("air_defense", left_device)