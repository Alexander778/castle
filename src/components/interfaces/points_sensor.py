from PIL import Image, ImageTk

from src.states.state import State


class PointsSensor:
    _instance = None

    def __new__(cls, canvas, screen_width, screen_height):
        if cls._instance is None:
            cls._instance = super(PointsSensor, cls).__new__(cls)
        return cls._instance

    def __init__(self, canvas, screen_width, screen_height):
        if not hasattr(self, "initialized"):
            self.canvas = canvas
            self.screen_width = screen_width
            self.screen_height = screen_height

            self.coins_image = ImageTk.PhotoImage(Image.open("../assets/coins.png"))

            self.counter = 0
            self.letter_cost = State().get_data("difficulty")["letter_cost"]

            self.sensor = self.create()
            self.initialized = True

            self.repairing_key = None
            self.movable_wall = None
            self.anti_rocket = None

    def create(self):
        self.canvas.create_image(10, self.screen_height - 80, image=self.coins_image, anchor="nw")
        return self.canvas.create_text(75, self.screen_height - 50,
                                       text=str(self.counter),
                                       fill="red",
                                       font=("Arial", 20, "bold"))

    def decrease(self, points):
        if self.counter == 0:
            return
        self.counter -= points
        self.__update_counter_display()

    def increase(self):
        self.counter += self.letter_cost

        self.repairing_key.recalculate()
        self.movable_wall.recalculate()

        self.__update_counter_display()

    def __update_counter_display(self):
        self.canvas.itemconfig(self.sensor, text=str(self.counter))