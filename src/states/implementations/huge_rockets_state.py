class HugeRocketsState:
    def __init__(self):
        self.huge_rockets = []

    def append(self, rocket):
        self.huge_rockets.append(rocket)

    def append_range(self, rocket):
        self.huge_rockets.extend(rocket)

    def remove(self, rocket):
        self.huge_rockets.remove(rocket)

    def get_data(self):
        return self.huge_rockets.copy()