import time
from dancing_links import DancingLinks


def organ_pipe_order(n):
    """
    Generate an "organ-pipe" ordering of indices [0..n-1], starting from the center
    and alternately adding indices to the left and right.

    This heuristic often balances constraint coverage in DLX searches.

    Args:
        n (int): Length of the sequence.

    Returns:
        list[int]: Indices in center-out order.
    """
    # Determine center positions
    center = n // 2
    left = center - 1
    right = center + (n % 2)
    order = [center] if n % 2 else []

    # Expand outwards alternately to left and right
    while left >= 0 or right < n:
        if left >= 0:
            order.append(left)
            left -= 1
        if right < n:
            order.append(right)
            right += 1
    return order


def solve_nq_organ(n):
    """
    Solve the n-Queens problem using DLX with organ-pipe ordering.

    Args:
        n (int): Board size (n x n).

    Returns:
        tuple: (results, elapsed)
            results: list of solutions (each a list of DLX nodes with row_data).
            elapsed: float, time taken in seconds.
    """
    start = time.time()

    # Build column definitions using organ-pipe order for rows and columns
    columns = []
    row_order = organ_pipe_order(n)
    col_order = organ_pipe_order(n)

    # Primary constraints: rows then columns
    for i in row_order:
        columns.append((f"R{i}", True))
    for j in col_order:
        columns.append((f"C{j}", True))

    # Secondary constraints: main diagonals
    for d in range(-(n - 1), n):
        columns.append((f"D{d}", False))
    # Secondary constraints: anti-diagonals
    for s in range(2 * n - 1):
        columns.append((f"A{s}", False))

    # Initialize DLX
    dlx = DancingLinks(columns)

    # Add rows for each board cell (i, j)
    for i in range(n):
        for j in range(n):
            row = [f"R{i}", f"C{j}", f"D{i - j}", f"A{i + j}"]
            dlx.add_row(row, row_data=(i, j))

    # Search for all solutions
    results = []
    solution = []
    dlx.search(solution, results)

    elapsed = time.time() - start
    print(f"[Organ Pipe] Solved {n}-Queens in {elapsed:.4f} seconds with {len(results)} solutions.")

    return results, elapsed
