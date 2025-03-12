class FallingLettersState:
    def __init__(self):
        self.letters = []

    def append(self, letter):
        self.letters.append(letter)

    def append_range(self, letters):
        self.letters.extend(letters)

    def remove(self, item):
        self.letters.remove(item)

    def get_data(self):
        return self.letters.copy()