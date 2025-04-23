from node import Node


class ColumnNode(Node):
    def __init__(self, name, primary=True):
        """
        Initialize a column header node in the DLX structure.

        Args:
            name (str): Identifier for this column (e.g., 'R0', 'C1', 'D-2').
            primary (bool): True if this is a primary (required) constraint.
        """
        super().__init__()
        self.name = name  # Descriptive name for debugging and constraint identification
        self.size = 0  # Tracks how many data nodes are linked under this column
        self.primary = primary  # Indicates if the constraint is mandatory (rows/columns) or optional (diagonals)
        # Initialize up and down pointers to self.
        self.up = self
        self.down = self
