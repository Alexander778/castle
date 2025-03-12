class AirDefenseState:
    def __init__(self):
        self.air_defense_devices = []

    def append(self, device):
        self.air_defense_devices.append(device)

    def append_range(self, devices):
        self.air_defense_devices.extend(devices)

    def remove(self, device):
        self.air_defense_devices.remove(device)

    def get_data(self):
        return self.air_defense_devices.copy()