class PauseGameState:
    def __init__(self):
        self.is_pause = False

    def append(self, value):
        self.is_pause = value

    def get_data(self):
        return self.is_pause