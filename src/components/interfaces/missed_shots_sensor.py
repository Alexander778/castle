from PIL import Image, ImageTk

class MissedShotsSensor:
    _instance = None

    def __new__(cls, canvas, screen_width, screen_height):
        if cls._instance is None:
            cls._instance = super(MissedShotsSensor, cls).__new__(cls)
        return cls._instance

    def __init__(self, canvas, screen_width, screen_height):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.canvas = canvas
            self.screen_width = screen_width
            self.screen_height = screen_height

            self.target_image = ImageTk.PhotoImage(Image.open("assets/target_sensor.png"))

            self.counter = 5
            self.sensor = self.create()
            self.initialized = True


    def create(self):
        self.canvas.create_image(150, self.screen_height - 75, image=self.target_image, anchor="nw")
        return self.canvas.create_text(205, self.screen_height - 50,
                                       text=str(self.counter),
                                       font=("Arial", 20, "bold"))

    def decrease(self):
        self.counter -= 1
        self.__update_counter_display()

    def reset(self):
        self.counter = 5
        self.__update_counter_display()

    def __update_counter_display(self):
        self.canvas.itemconfig(self.sensor, text=str(self.counter))