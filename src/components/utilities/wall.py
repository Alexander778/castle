class Wall:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.cells = self.create_wall()

    def create_wall(self):
        cells = []

        max_x1 = self.screen_width - 10
        current_x0 = 5
        current_x1 = 20

        while current_x1 <= max_x1:
            top_y0 = self.screen_height - 180
            middle_y0 = self.screen_height - 165
            bottom_y0 = self.screen_height - 150

            top_block = self.canvas.create_rectangle(current_x0, top_y0, current_x1, self.screen_height - 165,
                                                     fill='orange',
                                                     outline='black',
                                                     tags="target")
            middle_block = self.canvas.create_rectangle(current_x0, middle_y0, current_x1, self.screen_height - 150,
                                                        fill='orange',
                                                        outline='black',
                                                        tags="target")
            bottom_block = self.canvas.create_rectangle(current_x0, bottom_y0, current_x1, self.screen_height - 135,
                                                        fill='orange',
                                                        outline='black',
                                                        tags="target")
            cells.append(top_block)
            cells.append(middle_block)
            cells.append(bottom_block)

            current_x0 += 15
            current_x1 += 15
        return cells
