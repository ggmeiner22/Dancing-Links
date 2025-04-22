from dancing_links import DancingLinks
import time


def solve_n_queens(n):
    """
    Constructs the exact cover matrix for the n-Queens problem and solves it.
    Returns a list of solutions; each solution is a list of nodes (each with row_data (i, j)).
    """

    start = time.time()

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

    total_time = time.time() - start # Measure the run time of the original
    print(f"[Original] Solved {n}-Queens in {total_time:.4f} seconds with {len(results)} solutions.")

    return results, total_time


def print_solution(n, solution):
    """Prints a board for a given solution (list of nodes with row_data (i, j))."""
    board = [["." for _ in range(n)] for _ in range(n)]
    for node in solution:
        i, j = node.row_data
        board[i][j] = "Q"
    for row in board:
        print(" ".join(row))
    print()
