class WallCellsState:
    def __init__(self):
        self.cells = []

    def append(self, cell):
        self.cells.append(cell)

    def append_range(self, cells):
        self.cells.extend(cells)

    def remove(self, item):
        self.cells.remove(item)

    def get_data(self):
        return self.cells.copy()