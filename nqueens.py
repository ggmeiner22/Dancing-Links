#!/usr/bin/env python3
"""
Solving the n-Queens problem using Dancing Links (DLX / Algorithm X).

In the exact cover formulation for n-queens:
  - Each queen placement (at cell (i, j)) covers four constraints:
      • Row i (must have one queen)
      • Column j (must have one queen)
      • Main diagonal (i - j) – secondary constraint (at most one queen)
      • Anti-diagonal (i + j) – secondary constraint (at most one queen)
  - We require that every row and every column is covered exactly once.
  - Diagonals are treated as secondary: they are not forced to be covered,
    but if two queens share a diagonal, the conflict is avoided by DLX.
  
The Dancing Links structure below builds the matrix for these constraints
and then recursively searches for solutions.
"""

# DLX Nodes

class Node:
    def __init__(self):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.column = None  # Points to the column header.
        self.row_data = None  # Can store additional data (here, the cell (i, j)).

class ColumnNode(Node):
    def __init__(self, name, primary=True):
        super().__init__()
        self.name = name
        self.size = 0       # Number of nodes (1's) in this column.
        self.primary = primary  # True if this is a required (primary) column.
        # Initialize up and down pointers to self.
        self.up = self
        self.down = self

# Dancing Links structure and Algorithm X implementation

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

# Building the exact cover matrix for n-Queens

def solve_n_queens(n):
    """
    Constructs the exact cover matrix for the n-Queens problem and solves it.
    Returns a list of solutions; each solution is a list of nodes (each with row_data (i, j)).
    """
    columns = []
    # Primary columns: one per row and one per column.
    for i in range(n):
        columns.append((f"R{i}", True))
    for j in range(n):
        columns.append((f"C{j}", True))
    # Secondary columns: one for each main diagonal and anti-diagonal.
    # Main diagonals: indices from -(n-1) to (n-1)
    for d in range(-(n - 1), n):
        columns.append((f"D{d}", False))
    # Anti-diagonals: indices from 0 to 2*(n-1)
    for s in range(2 * n - 1):
        columns.append((f"A{s}", False))

    dlx = DancingLinks(columns)

    # For each cell (i, j), add a row corresponding to placing a queen there.
    # The row covers:
    #   - Row constraint: "R{i}"
    #   - Column constraint: "C{j}"
    #   - Main diagonal: "D{i - j}"
    #   - Anti-diagonal: "A{i + j}"
    for i in range(n):
        for j in range(n):
            row = [f"R{i}", f"C{j}", f"D{i - j}", f"A{i + j}"]
            dlx.add_row(row, row_data=(i, j))

    results = []
    solution = []
    dlx.search(solution, results)
    return results

def print_solution(n, solution):
    """Prints a board for a given solution (list of nodes with row_data (i, j))."""
    board = [["." for _ in range(n)] for _ in range(n)]
    for node in solution:
        i, j = node.row_data
        board[i][j] = "Q"
    for row in board:
        print(" ".join(row))
    print()

# Main execution: Solve and print one solution for n-Queens.

if __name__ == '__main__':
    n = 10  # Change n to solve a different board size.
    solutions = solve_n_queens(n)
    print(f"Found {len(solutions)} solutions for the {n}-queens problem.")
    if solutions:
        print("One of the solutions:")
        print_solution(n, solutions[0])
