import sys
from nqueens import solve_n_queens, print_solution
from organpipe import solve_nq_organ

def main():
    if len(sys.argv) < 2:
        print("Try the following: $ python3 main.py <board_size> [<board_size2> ...]")
        return

    summary = []

    for arg in sys.argv[1:]:
        try:
            n = int(arg)
        except ValueError:
            print(f"Board size '{arg}' is not an integer. Skipping.")
            continue

        print(f"\nSolving the {n}-queens problem using original algorithm...")
        original_solutions, original_time = solve_n_queens(n)

        print(f"\nSolving the {n}-queens problem using organ pipe ordering...")
        organ_solutions, organ_time = solve_nq_organ(n)

        summary.append((n, original_time, organ_time))

        # Optional: show a solution from each
        if original_solutions:
            print("\nOne of the original solutions:")
            print_solution(n, original_solutions[0])
        if organ_solutions:
            print("\nOne of the organ pipe solutions:")
            print_solution(n, organ_solutions[0])

    # Final comparison summary
    print("\n=== Runtime Comparison Summary ===")
    print(f"{'N':>3} | {'Original (s)':>14} | {'Organ Pipe (s)':>15} | {'Speedup':>8}")
    print("-" * 50)
    for n, t1, t2 in summary:
        speedup = t1 / t2 if t2 > 0 else float('inf')
        print(f"{n:>3} | {t1:>14.6f} | {t2:>15.6f} | {speedup:>8.2f}x")

main()
