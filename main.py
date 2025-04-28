import sys
from nqueens import solve_n_queens, print_solution
from organpipe import solve_nq_organ


def main():
    """
    Parses command-line arguments (board sizes), invoke solvers for each board size,
    and display solution examples and timing comparison.
    """
    # Ensure at least one board size is provided
    if len(sys.argv) < 2:
        print("Try the following: $ python3 main.py <board_size> [<board_size2> ...]")
        return

    # Store (n, original_time, organ_time) tuples for summary
    summary = []

    # Process each provided board size
    for arg in sys.argv[1:]:
        # Convert argument to integer, skip invalid inputs
        try:
            n = int(arg)
        except ValueError:
            print(f"Board size '{arg}' is not an integer. Skipping.")
            continue

        # Run original DLX algorithm in row-major order
        print(f"\nSolving the {n}-queens problem using original algorithm...")
        original_solutions, original_time = solve_n_queens(n)

        # Run DLX with organ-pipe (center-out) ordering
        print(f"\nSolving the {n}-queens problem using organ pipe ordering...")
        organ_solutions, organ_time = solve_nq_organ(n)

        # Collect timings for final comparison
        summary.append((n, original_time, organ_time))

        # Displays one solution from each method
        if original_solutions:
            print("\nOne of the original solutions:")
            print_solution(n, original_solutions[0])
        if organ_solutions:
            print("\nOne of the organ pipe solutions:")
            print_solution(n, organ_solutions[0])

    # After processing all sizes, print a runtime comparison table
    print("\n=== Runtime Comparison Summary ===")
    print(f"{'N':>3} | {'Original (s)':>14} | {'Organ Pipe (s)':>15} | {'Speedup':>8}")
    print("-" * 50)
    for n, t1, t2 in summary:
        # Calculate speedup; guard against zero-time
        speedup = t1 / t2 if t2 > 0 else float('inf')
        print(f"{n:>3} | {t1:>14.6f} | {t2:>15.6f} | {speedup:>8.2f}x")


main()
