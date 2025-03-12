import random
from src.states.state import State

class HugeRocket:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rocket = self.create()

    def create(self):
        launch_position = random.randrange(0, self.screen_width - 100)

        return self.canvas.create_rectangle(
            launch_position,
            0,
            launch_position + 5,
            25,
            fill='red')

    def move(self):
        if self.rocket is None:
            return
        _, _, _, rocket_y1 = self.canvas.coords(self.rocket)

        if abs(rocket_y1 - self.screen_height) < 100:
            self.destroy()
        else:
            self.canvas.move(self.rocket, 0, 10)
            self.canvas.after(50, self.move)

            self.__check_radars_for_damage()
            self.__check_air_defense_for_damage()
            self.__check_wall_for_damage()

    def destroy(self):
        self.canvas.delete(self.rocket)
        self.rocket = None

    def __check_radars_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0, rocket_x1, rocket_y1 = self.canvas.coords(self.rocket)
        potentially_damaged_radars = [
            radar for radar in State().get_data("radars")
            if len(self.canvas.coords(radar.radar["item"])) != 0
               and self.canvas.coords(radar.radar["item"])[0] <= rocket_x1 <=
                self.canvas.coords(radar.radar["item"])[2]
               and radar.radar["hp"] != 0
        ]

        for radar in potentially_damaged_radars:
            radar_item = radar.radar["item"]
            radar_x0, radar_y0, radar_x1, _ = self.canvas.coords(radar_item)

            if abs(rocket_y1 - radar_y0) < 15:
                radar.destroy()
                self.destroy()
                return

    def __check_air_defense_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0, rocket_x1, rocket_y1 = self.canvas.coords(self.rocket)
        potentially_damaged_air_defenses = [
            air_defense for air_defense in State().get_data("air_defense")
            if len(self.canvas.coords(air_defense.device["item"])) != 0
            and self.canvas.coords(air_defense.device["item"])[0] <= rocket_x0 <=
               self.canvas.coords(air_defense.device["item"])[2]
            and air_defense.device["hp"] != 0
        ]

        for air_defense in potentially_damaged_air_defenses:
            air_x0, air_y0, _, _ = self.canvas.coords(air_defense.device["item"])

            if abs(rocket_y1 - air_y0) < 15:
                air_defense.destroy()
                self.destroy()
                return

    def __check_wall_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0, rocket_x1, rocket_y1 = self.canvas.coords(self.rocket)
        potentially_damaged_cells = [
            cell for cell in State().get_data("wall_cells")
            if self.canvas.coords(cell)[0] <= rocket_x0
            and "hidden" not in self.canvas.itemcget(cell, "state")
        ]

        for cell in potentially_damaged_cells:
            cell_x0, cell_y0, _, _ = self.canvas.coords(cell)
            rocket_x0, rocket_y0, _, _ = self.canvas.coords(self.rocket)

            if abs(rocket_x0 - cell_x0) < 15 and abs(rocket_y0 - cell_y0) < 15:
                column_tag = self.canvas.gettags(cell)[1]

                cells_are_destroyed = 0
                for cell_in_col in self.canvas.find_withtag(column_tag):
                    current_state = self.canvas.itemcget(cell_in_col, "state")

                    if current_state == "":
                        cells_are_destroyed += 1

                    self.canvas.itemconfig(cell_in_col, state="hidden")

                if cells_are_destroyed == 3:
                    self.destroy()
                # else :GAME OVER
                return