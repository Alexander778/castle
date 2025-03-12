from src.components.utilities.huge_rocket import HugeRocket
from src.states.state import State


class UserTank:
    def __init__(self, canvas, screen_width, screen_height, missed_shots_sensor):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.missed_shots_sensor = missed_shots_sensor
        self.new_position_for_shot_x0 = 0

        self.tank = self.canvas.create_rectangle(
            screen_width / 2,
            screen_height - 130,
            screen_width / 2 + 100,
            screen_height - 85,
            fill='brown')

        self.sight = self.canvas.create_line(
            0, 10,
            100, 40,
            width=1,
            dash=(1, 1))
        self.canvas.itemconfig(self.sight, state="hidden")

    def move_tank_left(self, event):
        user_tank_x0 = self.canvas.coords(self.tank)[0]

        if user_tank_x0 > 0:
            self.canvas.move(self.tank, -10, 0)

    def move_tank_right(self, _):
        user_tank_x0 = self.canvas.coords(self.tank)[0]

        if user_tank_x0 < self.screen_width - 100:
            self.canvas.move(self.tank, 10, 0)

    def shot_letter(self, event):
        letter = event.char
        letter_symbol_color = "#0000FF"  # small letter color

        if letter.isupper():
            letter_symbol_color = "#FF0000"  # big letter color

        current_position = self.canvas.coords(self.tank)
        current_x0 = current_position[0]
        current_y0 = current_position[1]

        letter = self.canvas.create_text(current_x0 + 50, current_y0 - 10, text=letter, fill=letter_symbol_color)

        self.move_letter(letter)

    def move_letter(self, fired_letter):
        fired_letter_x0, fired_letter_y0 = self.canvas.coords(fired_letter)

        filtered_array = list(filter(lambda f_letter:
                                self.canvas.itemcget(fired_letter, "text") == self.canvas.itemcget(f_letter.letter_item, "text"),
                                State().get_data("letters")))

        for falling_letter in filtered_array:
            falling_x, falling_y = self.canvas.coords(falling_letter.letter_item)

            if abs(fired_letter_x0 - falling_x) < 20 and abs(fired_letter_y0 - falling_y) < 20:
                self.canvas.delete(fired_letter)
                falling_letter.destroy()
                return

        if fired_letter_y0 < 50:
            self.canvas.delete(fired_letter)
            self.__update_missed_shots_counter()
        else:
            self.canvas.move(fired_letter, 0, -10)
            self.canvas.after(100, self.move_letter, fired_letter)

    def show_sight(self, _):
        user_tank_x0, user_tank_y0, _, _ = self.canvas.coords(self.tank)

        line_length = self.__calculate_sight_length(user_tank_x0)
        if line_length == 0:
            self.canvas.itemconfig(self.sight, state="hidden")
            return

        self.canvas.coords(self.sight,
                           user_tank_x0 + 50, user_tank_y0 - 80,
                           user_tank_x0 + 50, self.__calculate_sight_length(user_tank_x0))

        self.canvas.itemconfig(self.sight, state="normal")

    def hide_sight(self, _):
        self.canvas.itemconfig(self.sight, state="hidden")

    def __calculate_sight_length(self, tank_x0):
        radars = State().get_data("radars")

        for radar in radars:
            radar_object = radar.radar
            radar_range_start, radar_range_end = radar_object["action_range"]

            if tank_x0 >= radar_range_start:
                radar_hp = radar_object["hp"]

                if radar_hp == 2:
                    return 55
                if radar_hp == 1:
                    return self.screen_height / 2
                else:
                    return 0

    def __update_missed_shots_counter(self):
        self.missed_shots_sensor.decrease()

        if self.missed_shots_sensor.counter == 0:
            self.missed_shots_sensor.reset()
            huge_rocket = HugeRocket(self.canvas,
                                     self.screen_width, self.screen_height)
            huge_rocket.move()

