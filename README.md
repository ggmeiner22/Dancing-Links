# N-Queens Problem using Dancing Links & Organ-Pipe Optimization

## Overview

This project solves the classical **n-Queens** problem using Donald Knuth’s **Dancing Links** (Algorithm X) in Python, and compares a standard row-column traversal against an **organ-pipe** ordering heuristic. For each board size you specify, it:

1. Builds an exact-cover matrix representation.
2. Runs the DLX search in **row-major order** (original).
3. Runs the DLX search in **organ-pipe** order (center-out).
4. Reports solution counts, individual runtimes, and relative speedup.

---

## File Structure

- **node.py**  
  Contains the base `Node` class that represents an element in the Dancing Links matrix.

- **column_node.py**  
  Defines the `ColumnNode` class, a subclass of `Node`, which represents column headers in the matrix and stores additional information like the size of the column and whether it is a primary column.

- **dancing_links.py**  
  Implements the `DancingLinks` class, which provides methods for manipulating the matrix ( adding rows, covering/uncovering columns) and performing the recursive search for solutions.

- **nqueens.py**  
  Builds the exact-cover matrix for the n-Queens problem in standard row-major order, runs Donald Knuth’s Dancing Links algorithm algorithm, measures its runtime, and provides `print_solution()`.

- **organpipe.py**  
  Generates an “organ-pipe” (center-out) ordering for rows and columns, builds the n-Queens matrix in that order, runs Donald Knuth’s Dancing Links algorithm algorithm, and times the optimized search.

- **gui.py**
  Generates a chess-like baord with n-queens, with teh ability to animate the steps the algorithm took, and a view of all boards of all solutions applicable with n. 

- **main.py**  
  Command-line entrypoint that accepts multiple board sizes, invokes both the original and organ-pipe solvers for each size, prints example solutions, and summarizes timing comparisons.

---

## Execution

To run the program use the following structure:
~~~
$ python3 main.py <board_size> [<board_size2> ...]
~~~
For example, the following will print board sizes of 4, 5, and 6:
~~~
$ python3 main.py 4 5 6
~~~
You can also run a graphical version of the program with:
~~~
$ python gui.py 6
~~~
