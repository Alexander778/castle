class RadarStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RadarStorage, cls).__new__(cls)
            cls._instance.data = []
        return cls._instance

    def append_range(self, value):
        self.data.extend(value)

    def remove(self, value):
        self.data.remove(value)

    def get_data(self):
        return self.data