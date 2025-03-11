class MovableWall:
    def __init__(self, canvas, tool_panel, falling_letters):
        self.canvas = canvas
        self.tool_panel = tool_panel

        self.falling_letters = falling_letters

        self.key_start_x0 = 0
        self.key_start_y0 = 0
        self.is_active = False

        self.wall_object = self.create()

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        movable_wall = self.canvas.create_rectangle(
            tp_x0 + 50, tp_y0 + 5,
            tp_x0 + 150, tp_y0 + 20,
            fill="coral",
            tags="drag_movable_wall")

        return {
            "item": movable_wall,
            "hp": 9
        }

    def on_drag_start(self, event):
        if self.is_active is True:
            return

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        if self.is_active is True:
            return

        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.wall_object["item"], dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        if self.is_active is True:
            return
        self.move_to_new_position()

    def move_to_new_position(self):
        self.is_active = True

        wall_item = self.wall_object["item"]
        w_x0, w_y0, w_x1, w_y1 = self.canvas.coords(wall_item)

        # do not move wall if it's on start position
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)
        if w_x0 > tp_x0 and w_y0 > tp_y0:
            self.is_active = False
            return

        move_after_timeout = self.__get_move_timeout()

        closest_letter = self.__find_closest_letter_to_catch(w_y1, w_x0, move_after_timeout)
        if not closest_letter:
            self.canvas.after(move_after_timeout, self.move_to_new_position)
            return

        cl_x0, cl_y0 = self.canvas.coords(closest_letter.letter_item)

        wall_center_distance = (w_x1 - w_x0) / 2
        w_x0 += wall_center_distance

        if abs(w_y1 - cl_y0) < 20 and w_x0 <= cl_x0 <= w_x1:
            closest_letter.destroy()
            self.wall_object["hp"] -= 1

            if self.wall_object["hp"] == 0:
                self.__reset_position_key()

        step_size = min(10, abs(w_x0 - cl_x0))
        if w_x0 < cl_x0:
            self.canvas.move(wall_item, step_size, 0)
        elif w_x0 > cl_x0:
            self.canvas.move(wall_item, -step_size, 0)

        self.canvas.after(move_after_timeout, self.move_to_new_position)

    def __get_move_timeout(self):
        wall_hp = self.wall_object["hp"]

        if 9 >= wall_hp >= 6:
            return 50
        elif 6 > wall_hp >= 3:
            return 100
        else:
            return 150

    def __find_closest_letter_to_catch(self, wall_y0, wall_x0, wall_move_timeout):
        letters = [
            l for l in self.falling_letters
            if self.canvas.coords(l.letter_item)[1] < wall_y0
        ]

        if not letters:
            return None

        # Find the closest letter in terms of vertical distance
        closest_letter = min(
            letters,
            key=lambda l: (
                abs(self.canvas.coords(l.letter_item)[1] - wall_y0),  # Primary: Y-distance
                abs(self.canvas.coords(l.letter_item)[0] - wall_x0)  # Secondary: X-distance
            )
        )

        l_x0, l_y0 = self.canvas.coords(closest_letter.letter_item)

        letter_to_wall_by_y_distance = wall_y0 - l_y0
        wall_to_reach_letter_by_x_distance = abs(wall_x0 - l_x0)

        # Falling speed of letter: 10 pixels per 500ms → 0.02 pixels/ms
        letter_to_reach_wall_line_time = letter_to_wall_by_y_distance / (10 / 500)
        wall_to_reach_letter_line_time = wall_to_reach_letter_by_x_distance / (10 / wall_move_timeout)

        # Introduce a tolerance factor (e.g., 5% margin)
        if letter_to_reach_wall_line_time > wall_to_reach_letter_line_time:
            return closest_letter
        else:
            return None

    def __reset_position_key(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        self.is_active = False
        self.wall_object["hp"] = 9
        self.canvas.coords(self.wall_object["item"],
                           tp_x0 + 80, tp_y0 + 10,
                           tp_x0 + 150, tp_y0 + 30)


