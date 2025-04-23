from src.constants import difficulty_levels


class DifficultyState:
    def __init__(self):
        self._difficulty_config = {}

    def append(self, name):
        self._difficulty_config = difficulty_levels[name]

    def get_data(self):
        return self._difficulty_config.copy()