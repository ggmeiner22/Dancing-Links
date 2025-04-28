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
    """Print a fancy, realistic styled chessboard using ANSI and Unicode."""
    board = [[" " for _ in range(n)] for _ in range(n)]
    for node in solution:
        i, j = node.row_data
        board[i][j] = "♛"

    dark = "\033[48;5;240m"
    light = "\033[48;5;250m"
    reset = "\033[0m"
    border = "   " + "".join(f"  {chr(65 + c)} " for c in range(n))  # Column headers A, B, C...

    print("\n" + border)
    print("  +" + "---+" * n)
    for i in range(n):
        row = []
        for j in range(n):
            square_color = dark if (i + j) % 2 else light
            piece = board[i][j]
            row.append(f"{square_color} {piece} {reset}")
        print(f"{n - i} |" + "|".join(row) + f"| {n - i}")  # Row index (bottom to top)
        print("  +" + "---+" * n)
    print(border + "\n")

