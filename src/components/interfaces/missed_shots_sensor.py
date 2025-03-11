class MissedShotsSensor:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.counter = 5

        self.sensor = self.create()

    def create(self):
        return self.canvas.create_text(50, self.screen_height - 60,
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