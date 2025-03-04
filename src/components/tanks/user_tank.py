from src.components.storage.falling_letter_storage import FallingLetterStorage


class UserTank:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.new_position_for_shot_x0 = 0
        self.is_damaged = False

        self.letter_storage = FallingLetterStorage()

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
                                self.letter_storage.get_data()))

        for falling_letter in filtered_array:
            falling_x, falling_y = self.canvas.coords(falling_letter.letter_item)

            if abs(fired_letter_x0 - falling_x) < 20 and abs(fired_letter_y0 - falling_y) < 20:
                self.canvas.delete(fired_letter)
                falling_letter.destroy()
                return

        if fired_letter_y0 < 10:
            self.canvas.delete(fired_letter)
        else:
            self.canvas.move(fired_letter, 0, -10)
            self.canvas.after(100, self.move_letter, fired_letter)

    def show_sight(self, _):
        user_tank_x0, user_tank_y0, user_tank_x1, _ = self.canvas.coords(self.tank)

        line_top_y1 = self.screen_height * 0.09

        # check status of the nearest radar
        # for radar in radars:
        #     radar_range_start, radar_range_end = radar["action_range"]
        #
        #     if user_tank_x0 >= radar_range_start and user_tank_x1 <= radar_range_end:
        #         radar_hp = radar["hp"]
        #
        #         if radar_hp == 2:
        #             print("full line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))
        #
        #         elif radar_hp == 1:
        #             line_top_y1 = screen_height / 2
        #             print("divided line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))
        #         else:
        #             print("no line", (user_tank_x0, user_tank_x1), (radar_range_start, radar_range_end))
        #             return

        self.canvas.coords(self.sight,
                          user_tank_x0 + 50, user_tank_y0 - 60,
                          user_tank_x0 + 50, line_top_y1)
        self.canvas.itemconfig(self.sight, state="normal")

    def hide_sight(self, _):
        self.canvas.itemconfig(self.sight, state="hidden")