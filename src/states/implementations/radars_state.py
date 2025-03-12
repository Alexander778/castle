class RadarsState:
    def __init__(self):
        self.radars = []

    def append(self, radar):
        self.radars.append(radar)

    def append_range(self, radars):
        self.radars.extend(radars)

    def remove(self, radar):
        self.radars.remove(radar)

    def get_data(self):
        return self.radars.copy()