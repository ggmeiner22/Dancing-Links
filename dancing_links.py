from node import Node
from column_node import ColumnNode


class DancingLinks:
    def __init__(self, columns):
        """
        columns: list of tuples (col_name, is_primary)
        """
        # Create the header node.
        self.header = ColumnNode("header")
        self.columns = {}  # Map from column name to ColumnNode.
        last = self.header
        # Create column headers and add them to the doubly linked list.
        for name, is_primary in columns:
            col = ColumnNode(name, primary=is_primary)
            self.columns[name] = col
            # Insert col into the header's list.
            col.left = last
            col.right = self.header
            last.right = col
            self.header.left = col
            last = col

    def add_row(self, row, row_data=None):
        """
        Add a row to the DLX matrix.
          row: list of column names where the row has a 1.
          row_data: optional data associated with the row (e.g. (i, j)).
        """
        first_node = None
        for col_name in row:
            col = self.columns[col_name]
            new_node = Node()
            new_node.column = col
            new_node.row_data = row_data
            # Link the new node into the bottom of the column.
            new_node.down = col
            new_node.up = col.up
            col.up.down = new_node
            col.up = new_node
            col.size += 1
            # Link the new node into the row.
            if first_node is None:
                first_node = new_node
                new_node.left = new_node
                new_node.right = new_node
            else:
                new_node.left = first_node.left
                new_node.right = first_node
                first_node.left.right = new_node
                first_node.left = new_node

    def cover(self, col):
        """Covers a column (removes it from the header list) and all rows that use it."""
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        """Uncovers a column (restores it into the header list) and all rows that use it."""
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def search(self, solution, results):
        """
        Recursively search for solutions.
        'solution' is the partial solution (list of nodes corresponding to chosen rows).
        'results' collects complete solutions.
        """
        # Check if all primary columns are covered.
        all_covered = True
        j = self.header.right
        while j != self.header:
            if j.primary:
                all_covered = False
                break
            j = j.right
        if all_covered:
            results.append(solution.copy())
            return

        # Choose the primary column with the fewest nodes.
        c = None
        j = self.header.right
        while j != self.header:
            if j.primary:
                if c is None or j.size < c.size:
                    c = j
            j = j.right
        if c is None or c.size == 0:
            return

        self.cover(c)
        r = c.down
        while r != c:
            solution.append(r)
            j = r.right
            while j != r:
                self.cover(j.column)
                j = j.right
            self.search(solution, results)
            solution.pop()
            j = r.left
            while j != r:
                self.uncover(j.column)
                j = j.left
            r = r.down
        self.uncover(c)
