class RepairingKey:
    def __init__(self, canvas, screen_width, screen_height, wall_cells):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.wall_cells = wall_cells

        self.repair_key = canvas.create_rectangle(
                screen_width / 2 - 80, screen_height - 65,
                screen_width / 2 - 60, screen_height - 50,
                fill="yellow",
                tags="draggable")

        self.key_start_x0 = 0
        self.key_start_y0 = 0

    def on_drag_start(self, event):
        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_move(self, event):
        dx = event.x - self.key_start_x0
        dy = event.y - self.key_start_y0

        self.canvas.move(self.repair_key, dx, dy)

        self.key_start_x0 = event.x
        self.key_start_y0 = event.y

    def on_drag_release(self, _):
        x1, y1, x2, y2 = self.canvas.coords(self.repair_key)

        for cell in self.wall_cells:
            tx1, ty1, tx2, ty2 = self.canvas.coords(cell)
            if x1 < tx2 and x2 > tx1 and y1 < ty2 and y2 > ty1:
                self.canvas.itemconfig(cell, state="normal")
                self.canvas.coords(self.repair_key,
                                   self.screen_width / 2 - 80, self.screen_height - 65,
                                   self.screen_width / 2 - 60, self.screen_height - 50)
                return

        # for radar in radars:
        #     rx1, ry1, rx2, ry2 = canvas.coords(radar["radar"])
        #     if x1 < rx1 and x2 > ry1 and y1 < rx2 and y2 > ry2:
        #         if radar["hp"] == 1:
        #             radar["hp"] += 1
        #
        #         canvas.coords(repair_key, screen_width / 2 - 80, screen_height - 65, screen_width / 2 - 60,
        #                       screen_height - 50)
        #         return

        self.canvas.coords(self.repair_key, self.screen_width / 2 - 80, self.screen_height - 65,
                           self.screen_width / 2 - 60, self.screen_height - 50)