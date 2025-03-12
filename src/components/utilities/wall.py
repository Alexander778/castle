from src.states.state import State


class Wall:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        state = State()
        state.append_range("wall_cells", self.create_wall())

    def create_wall(self):
        cells = []

        max_x1 = self.screen_width - 10
        current_x0 = 5
        current_x1 = 20

        col_index = 0

        while current_x1 <= max_x1:
            col_index_tag = f"column_{col_index}"

            top_y0 = self.screen_height - 210
            middle_y0 = self.screen_height - 195
            bottom_y0 = self.screen_height - 180

            top_block = self.canvas.create_rectangle(current_x0, top_y0, current_x1, self.screen_height - 195,
                                                     fill='orange',
                                                     outline='black',
                                                     tags=("target", col_index_tag))
            middle_block = self.canvas.create_rectangle(current_x0, middle_y0, current_x1, self.screen_height - 180,
                                                        fill='orange',
                                                        outline='black',
                                                        tags=("target", col_index_tag))
            bottom_block = self.canvas.create_rectangle(current_x0, bottom_y0, current_x1, self.screen_height - 165,
                                                        fill='orange',
                                                        outline='black',
                                                        tags=("target", col_index_tag))
            cells.append(top_block)
            cells.append(middle_block)
            cells.append(bottom_block)

            current_x0 += 15
            current_x1 += 15
            col_index += 1
        return cells
