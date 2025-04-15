class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = None  # Points to the column header.
        self.row_data = None  # Can store additional data (here, the cell (i, j)).
