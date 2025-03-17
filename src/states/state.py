from src.states.implementations.air_defense_state import AirDefenseState
from src.states.implementations.falling_letters_state import FallingLettersState
from src.states.implementations.huge_rockets_state import HugeRocketsState
from src.states.implementations.radars_state import RadarsState
from src.states.implementations.wall_cells_state import WallCellsState

class State:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)

            cls._instance.__letters_state = FallingLettersState()
            cls._instance.__wall_cell_state = WallCellsState()
            cls._instance.__air_defense_state = AirDefenseState()
            cls._instance.__radars_state = RadarsState()
            cls._instance.__huge_rocket_state = HugeRocketsState()

        return cls._instance
    
    def append(self, instance_type, item):
        instance = self.__get_instance(instance_type)
        instance.append(item)

    def append_range(self, instance_type, items):
        instance = self.__get_instance(instance_type)
        instance.append_range(items)

    def get_data(self, instance_type):
        instance = self.__get_instance(instance_type)
        return instance.get_data()

    def remove(self, instance_type, item):
        instance = self.__get_instance(instance_type)
        instance.remove(item)

    def __get_instance(self, instance_type):
        instance_mapping = {
            "letters": self._instance.__letters_state,
            "wall_cells": self._instance.__wall_cell_state,
            "air_defense": self._instance.__air_defense_state,
            "radars": self._instance.__radars_state,
            "huge_rocket": self._instance.__huge_rocket_state
        }

        if instance_type in instance_mapping:
            return instance_mapping[instance_type]

        raise ValueError(f"Invalid instance type: {instance_type}")