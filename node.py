class Node:
    def __init__(self):
        """
        Initialize a DLX node and link it to itself in all four directions.
        """
        # Self-links form a circular list for both row and column traversals
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        # Column header node for this data node
        self.column = None  # Set when the node is added to a column
        self.row_data = None  # User-defined payload, such as coordinates for a queen placement
