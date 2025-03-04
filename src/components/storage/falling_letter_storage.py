class FallingLetterStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FallingLetterStorage, cls).__new__(cls)
            cls._instance.data = []
        return cls._instance

    def append(self, value):
        self.data.append(value)

    def remove(self, value):
        self.data.remove(value)

    def get_data(self):
        return self.data