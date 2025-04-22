import time
from dancing_links import DancingLinks

def organ_pipe_order(n):

    # Generate an organ-pipe ordering of indices, which go from center on out

    center = n // 2
    left = center - 1
    right = center + (n % 2)
    order = [center] if n % 2 else []

    while left >= 0 or right < n:
        if left >= 0:
            order.append(left)
            left -= 1
        if right < n:
            order.append(right)
            right += 1
    return order
    
def solve_nq_organ(n):
    start = time.time()

    columns = []
    row_order = organ_pipe_order(n)
    col_order = organ_pipe_order(n)

    for i in row_order:
        columns.append((f"R{i}", True))
    for j in col_order:
        columns.append((f"C{j}", True))

    for d in range(-(n - 1), n):
        columns.append((f"D{d}", False))
    for s in range(2 * n - 1):
        columns.append((f"A{s}", False))

    dlx = DancingLinks(columns)

    for i in range(n):
        for j in range(n):
            row = [f"R{i}", f"C{j}", f"D{i - j}", f"A{i + j}"]
            dlx.add_row(row, row_data=(i, j))

    results = []
    solution = []
    dlx.search(solution, results)

    elapsed = time.time() - start
    print(f"[Organ Pipe] Solved {n}-Queens in {elapsed:.4f} seconds with {len(results)} solutions.")

    return results, elapsed