import random
from src.states.state import State

class AntiRocket:
    def __init__(self, canvas, screen_width, screen_height, tool_panel, rocket_platform):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tool_panel = tool_panel
        self.rocket_platform = rocket_platform

        self.anti_rocket = self.create()

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        return self.canvas.create_rectangle(
            tp_x0 + 160, tp_y0 + 5,
            tp_x0 + 180, tp_y0 + 20,
            fill="blue",
            tags="draggable_rocket")

    def on_drag_start(self, event):
        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.anti_rocket, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        x1, y1, x2, y2 = self.canvas.coords(self.rocket_platform)

        platform_center_y = (y1 + y2) / 2

        ax1, _, ax2, _ = self.canvas.coords(self.anti_rocket)

        self.canvas.coords(
            self.anti_rocket,
            ax1,
            platform_center_y - 7.5,
            ax2,
            platform_center_y + 7.5
        )

    def launch_rocket(self, event):
        self.move()

    def move(self):
        if self.anti_rocket is None:
            return
        _, rocket_y0, _, _ = self.canvas.coords(self.anti_rocket)

        if rocket_y0 < 10:
            self.destroy()
        else:
            self.canvas.move(self.anti_rocket, 0, -10)
            self.canvas.after(40, self.move)

            # TODO check if user hit the tank
            self.__check_huge_rockets_for_damage()

    def destroy(self):
        self.canvas.delete(self.anti_rocket)
        self.anti_rocket = None

    def __check_huge_rockets_for_damage(self):
        if not self.anti_rocket:
            return

        a_rocket_x0, a_rocket_y0, a_rocket_x1, a_rocket_y1 = self.canvas.coords(self.anti_rocket)
        potentially_damaged_huge_rockets = [
            h_rocket for h_rocket in State().get_data("huge_rocket")
            if len(self.canvas.coords(h_rocket.rocket)) != 0
            and self.canvas.coords(h_rocket.rocket)[0] >= a_rocket_x0 and
               self.canvas.coords(h_rocket.rocket)[2] <= a_rocket_x1
        ]

        for huge_rocket in potentially_damaged_huge_rockets:
            h_rocket_x0, h_rocket_y0, _, h_rocket_y1 = self.canvas.coords(huge_rocket.rocket)

            if abs(a_rocket_y0 - h_rocket_y1) < 10:
                self.destroy()
                huge_rocket.destroy()
                return