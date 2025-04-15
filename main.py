import sys
from nqueens import solve_n_queens, print_solution


def main():
    if len(sys.argv) < 2:
        print("Try the following: $ python3 main.py <board_size> [<board_size2> ...]")
        return
    # Process each board size provided as a command-line argument.
    for arg in sys.argv[1:]:
        try:
            n = int(arg)
        except ValueError:
            print(f"Board size '{arg}' is not an integer. Skipping.")
            continue

        print(f"Solving the {n}-queens problem...")
        solutions = solve_n_queens(n)
        print(f"Found {len(solutions)} solutions for the {n}-queens problem.")
        if solutions:
            print("One of the solutions:")
            print_solution(n, solutions[0])


main()
