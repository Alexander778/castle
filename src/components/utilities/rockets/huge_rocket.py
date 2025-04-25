import random

from src.components.effects.big_explosion import BigExplosion
from src.states.state import State
from PIL import Image, ImageTk

class HugeRocket:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.huge_rocket_image = ImageTk.PhotoImage(Image.open("../assets/huge_rocket.png"))
        self.image_width = self.huge_rocket_image.width()
        self.image_height = self.huge_rocket_image.height()

        self.rocket = self.create()

    def create(self):
        launch_position = random.randrange(0, self.screen_width - 100)

        return self.canvas.create_image(
            launch_position, 0,
            image=self.huge_rocket_image, anchor="nw")

    def move(self):
        if State().get_data("pause_game"):
            self.canvas.after(100, self.move)
            return

        if self.rocket is None or len(self.canvas.coords(self.rocket)) == 0:
            return
        _, rocket_y0 = self.canvas.coords(self.rocket)

        if abs(rocket_y0 + self.image_height - self.screen_height) < 100:
            self.destroy()
        else:
            self.canvas.move(self.rocket, 0, 10)
            self.canvas.after(100, self.move)

            self.__check_radars_for_damage()
            self.__check_air_defense_for_damage()
            self.__check_wall_for_damage()

    def destroy(self):
        rocket_coordinates = self.canvas.coords(self.rocket)
        BigExplosion(self.canvas).show(
            rocket_coordinates[0] + self.image_width / 2,
            rocket_coordinates[1] + self.image_height + 25,
            500)

        self.canvas.delete(self.rocket)
        State().remove("huge_rocket", self)
        self.rocket = None

    def __check_radars_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0 = self.canvas.coords(self.rocket)
        rocket_x1 = rocket_x0 + self.image_width
        rocket_y1 = rocket_y0 + self.image_height

        potentially_damaged_radars = [
            radar for radar in State().get_data("radars")
            if len(self.canvas.coords(radar.radar["item"])) != 0
               and self.canvas.coords(radar.radar["item"])[0] <= rocket_x1 <=
                self.canvas.coords(radar.radar["item"])[0] + radar.radar["image"].width()
               and radar.radar["hp"] != 0
        ]

        for radar in potentially_damaged_radars:
            radar_item = radar.radar["item"]
            radar_x0, radar_y0 = self.canvas.coords(radar_item)

            if abs(rocket_y1 - radar_y0) < 15:
                radar.destroy()
                self.destroy()
                return

    def __check_air_defense_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0 = self.canvas.coords(self.rocket)
        rocket_y1 = rocket_y0 + self.image_height

        potentially_damaged_air_defenses = [
            air_defense for air_defense in State().get_data("air_defense")
            if len(self.canvas.coords(air_defense.rocket["rocket"])) != 0
            and self.canvas.coords(air_defense.rocket["rocket"])[0] <= rocket_x0 <=
               self.canvas.coords(air_defense.rocket["rocket"])[0] + self.image_width
            and air_defense.rocket["hp"] != 0
        ]

        for air_defense in potentially_damaged_air_defenses:
            air_x0, air_y0 = self.canvas.coords(air_defense.rocket["rocket"])

            if abs(rocket_y1 - air_y0) < 15:
                air_defense.destroy()
                self.destroy()
                return

    def __check_wall_for_damage(self):
        if not self.rocket:
            return

        rocket_x0, rocket_y0 = self.canvas.coords(self.rocket)

        potentially_damaged_cells = [
            cell for cell in State().get_data("wall_cells")
            if self.canvas.coords(cell)[0] <= rocket_x0
            and "hidden" not in self.canvas.itemcget(cell, "state")
        ]

        for cell in potentially_damaged_cells:
            cell_x0, cell_y0 = self.canvas.coords(cell)
            rocket_x0, rocket_y0 = self.canvas.coords(self.rocket)

            rocket_x1 = rocket_x0 + self.image_width
            rocket_y1 = rocket_y0 + self.image_height

            if abs(rocket_x1 - cell_x0) <= 40 and abs(rocket_y1 - cell_y0) < 15:
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