from node import Node


class ColumnNode(Node):
    def __init__(self, name, primary=True):
        super().__init__()
        self.name = name
        self.size = 0       # Number of nodes (1's) in this column.
        self.primary = primary  # True if this is a required (primary) column.
        # Initialize up and down pointers to self.
        self.up = self
        self.down = self
