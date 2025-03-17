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

            self.counter = 0
            self.sensor = self.create()
            self.initialized = True

            self.repairing_key = None

    def create(self):
        return self.canvas.create_text(50, self.screen_height - 60,
                                       text=str(self.counter),
                                       fill="red",
                                       font=("Arial", 20, "bold"))

    def decrease(self, points):
        if self.counter == 0:
            return
        self.counter -= points
        self.__update_counter_display()

    def increase(self):
        self.counter += 5 # user can get points only for hitting letter using tank
        self.repairing_key.recalculate_properties()
        self.__update_counter_display()

    def __update_counter_display(self):
        self.canvas.itemconfig(self.sensor, text=str(self.counter))