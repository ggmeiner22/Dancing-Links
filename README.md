# N-Queens Problem using Dancing Links

## Overview

This project provides a solution to the classic n‑Queens problem using Donald Knuth’s Dancing Links algorithm (Algorithm X) in Python.

## File Structure

- **node.py**  
  Contains the base `Node` class that represents an element in the Dancing Links matrix.

- **column_node.py**  
  Defines the `ColumnNode` class, a subclass of `Node`, which represents column headers in the matrix and stores additional information like the size of the column and whether it is a primary column.

- **dancing_links.py**  
  Implements the `DancingLinks` class, which provides methods for manipulating the matrix ( adding rows, covering/uncovering columns) and performing the recursive search for solutions.

- **nqueens.py**  
  Contains functions for building the exact cover matrix representation of the n‑Queens problem, solving it using the Donald Knuth’s Dancing Links algorithm algorithm, and printing a textual representation of a solution.

- **main.py**  
  The main entry point of the application. It reads one or more board sizes as command-line arguments, executes the solver for each board size, and prints out the number of solutions along with one sample solution for each.

## Execution

To run the program use the following structure:
~~~
$ python3 main.py <board_size> [<board_size2> ...]
~~~
For example, the following will print board sizes of 4, 5, and 6:
~~~
$ python3 main.py 4 5 6
~~~

