from PIL import Image, ImageTk
from src.components.interfaces.points_sensor import PointsSensor
from src.constants import anti_rocket_cost
from src.states.state import State

class AntiRocket:
    def __init__(self, canvas, screen_width, screen_height, tool_panel, rocket_platform):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tool_panel = tool_panel
        self.rocket_platform = rocket_platform

        self.is_disabled = True

        self.point_sensor = PointsSensor(canvas, screen_width, screen_height)
        self.point_sensor.anti_rocket = self

        self.key_start_x0 = 0
        self.key_start_y0 = 0

        self.disabled_img = ImageTk.PhotoImage(Image.open("assets/anti_rocket/anti_rocket_disabled.png"))
        self.inactive_img = ImageTk.PhotoImage(Image.open("assets/anti_rocket/anti_rocket_inactive.png"))
        self.active_img = ImageTk.PhotoImage(Image.open("assets/anti_rocket/anti_rocket_active.png"))

        self.img_width = self.disabled_img.width()
        self.img_height  = self.disabled_img.height()

        self.anti_rocket = self.create()

    def create(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        anti_rocket = self.canvas.create_image(
            tp_x0 + 160, tp_y0 + 5,
            image=self.disabled_img, anchor="nw",
            tags="draggable_rocket")

        if not self.is_disabled:
            self.canvas.itemconfig(anti_rocket, image=self.inactive_img)

        return anti_rocket

    def on_drag_start(self, event):
        if self.is_disabled:
            return

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        if self.is_disabled:
            return

        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.anti_rocket, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, event):
        if self.is_disabled:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.rocket_platform)

        platform_center_y = (y1 + y2) / 2

        ax1, _ = self.canvas.coords(self.anti_rocket)
        ax2 = ax1 + self.img_width

        self.canvas.coords(
            self.anti_rocket,
            ax1,
            platform_center_y - 7.5
        )
        self.point_sensor.decrease(anti_rocket_cost)
        self.recalculate()

    def launch_rocket(self, event):
        self.move()

    def move(self):
        if self.anti_rocket is None:
            return
        _, rocket_y0 = self.canvas.coords(self.anti_rocket)

        if rocket_y0 < 5:
            self.destroy()
        else:
            self.canvas.move(self.anti_rocket, 0, -10)
            self.canvas.after(40, self.move)

            # TODO check if user hit the tank
            self.__check_huge_rockets_for_damage()

    def destroy(self):
        self.__reset_position()

    def recalculate(self):
        self.is_disabled = self.point_sensor.counter < anti_rocket_cost
        if not self.is_disabled:
            self.canvas.itemconfig(self.anti_rocket, image=self.inactive_img)
        else:
            self.canvas.itemconfig(self.anti_rocket, image=self.disabled_img)

    def __check_huge_rockets_for_damage(self):
        if not self.anti_rocket:
            return

        a_rocket_x0, a_rocket_y0 = self.canvas.coords(self.anti_rocket)

        potentially_damaged_huge_rockets = [
            h_rocket for h_rocket in State().get_data("huge_rocket")
            if len(self.canvas.coords(h_rocket.rocket)) != 0
        ]

        for huge_rocket in potentially_damaged_huge_rockets:
            h_rocket_x0, h_rocket_y0 = self.canvas.coords(huge_rocket.rocket)
            h_rocket_y1 = h_rocket_y0 + 34 # TODO huge_rocket width replace 34

            if abs(a_rocket_y0 - h_rocket_y1) < 3:
                self.destroy()
                huge_rocket.destroy()
                return

    def __reset_position(self):
        tp_x0, tp_y0, _, _ = self.canvas.coords(self.tool_panel)

        self.recalculate()
        self.canvas.coords(self.anti_rocket, tp_x0 + 160, tp_y0 + 5)