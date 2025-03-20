from src.states.state import State
from PIL import Image, ImageTk

class Wall:
    def __init__(self, canvas, screen_width, screen_height):
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.image = ImageTk.PhotoImage(
            Image.open("C:/Users/Oleksandr-O.Kuzmenko/PycharmProjects/castle/assets/wall_cell.png")
            # TODO replace with relative path
        )

        state = State()
        state.append_range("wall_cells", self.create_wall())

    def create_wall(self):
        cells = []

        max_x1 = self.screen_width - 5
        current_x0 = 5
        current_x1 = 26

        col_index = 0

        while current_x1 <= max_x1:
            col_index_tag = f"column_{col_index}"

            top_y0 = self.screen_height - 210
            middle_y0 = self.screen_height - 195
            bottom_y0 = self.screen_height - 180

            top_block = self.canvas.create_image(current_x0, top_y0, tags=("target", col_index_tag), image=self.image, anchor="nw")
            middle_block = self.canvas.create_image(current_x0, middle_y0, tags=("target", col_index_tag), image=self.image, anchor="nw")
            bottom_block = self.canvas.create_image(current_x0, bottom_y0, tags=("target", col_index_tag), image=self.image, anchor="nw")

            cells.append(top_block)
            cells.append(middle_block)
            cells.append(bottom_block)

            current_x0 += 26
            current_x1 += 26
            col_index += 1
        return cells
