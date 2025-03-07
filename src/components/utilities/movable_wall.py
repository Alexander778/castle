from src.components.storage.falling_letter_storage import FallingLetterStorage


class MovableWall:
    def __init__(self, canvas, tool_panel):
        self.canvas = canvas

        self._letter_storage = FallingLetterStorage()

        tp_x0, tp_y0, _, _ = self.canvas.coords(tool_panel)

        self.movable_wall = canvas.create_rectangle(
            tp_x0 + 80, tp_y0 + 10,
            tp_x0 + 150, tp_y0 + 30,
            fill="coral",
            tags="drag_movable_wall")

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def on_drag_start(self, event):
        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.movable_wall, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        self.move_to_new_position()

    def move_to_new_position(self):
        w_x0, w_y0, w_x1, w_y1 = self.canvas.coords(self.movable_wall)

        falling_letters = [
            l for l in self._letter_storage.get_data()
            if self.canvas.coords(l.letter_item)[1] < w_y1
        ]

        closest_letter = self.__find_closest_number(falling_letters, w_y1)

        if not closest_letter:
            self.canvas.after(100, self.move_to_new_position)
            return

        cl_x0, cl_y0 = self.canvas.coords(closest_letter.letter_item)

        wall_center_distance = (w_x1 - w_x0) / 2
        w_x0 += wall_center_distance

        if abs(w_y1 - cl_y0) < 20 and w_x0 <= cl_x0 <= w_x1:
            closest_letter.destroy()

        step_size = min(10, abs(w_x0 - cl_x0))
        if w_x0 < cl_x0:
            self.canvas.move(self.movable_wall, step_size, 0)
        elif w_x0 > cl_x0:
            self.canvas.move(self.movable_wall, -step_size, 0)

        self.canvas.after(50, self.move_to_new_position)

    def __find_closest_number(self, arr, target):
        return min(arr, key=lambda x: abs(self.canvas.coords(x.letter_item)[1] - target))


