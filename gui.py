import tkinter as tk
import sys
from organpipe import solve_nq_organ

# Constants for board rendering and colors
CELL_SIZE = 60  # Size (in pixels) of each cell on the chessboard
BOARD_COLOR_1 = "#EEEED2"  # Light-colored square
BOARD_COLOR_2 = "#769656"  # Dark-colored square
HIGHLIGHT_COLOR = "#FFD700"  # Color for highlighting threatened squares
QUEEN_COLOR = "black"  # Color to draw the queen symbol
ERROR_COLOR = "red"  # Color for drawing conflict markers

ANIMATION_DELAY = 200  # Delay in milliseconds between animation steps


class NQueensGUI:
    def __init__(self, root, n, solutions):
        """
        Initialize the n-Queens GUI.

        Args:
            root (tk.Tk): The main Tkinter window.
            n (int): Board size (number of rows/columns).
            solutions (list): List of solution node lists from DLX solver.
        """
        self.root = root  # Store reference to the main window
        self.n = n  # Store board size
        self.solutions = solutions  # Store all found solutions
        self.current_index = 0  # Index of the currently displayed solution
        self.selected_queen = None  # Coordinates of a selected queen (for threat checking)
        self.temp_queen = None  # Coordinates of a temporarily placed queen by user
        self.conflict_pair = None  # Pairs of coordinates in conflict
        self.animating = False  # Flag to indicate if animation is running

        # Create and pack the drawing canvas
        self.canvas = tk.Canvas(root, width=n * CELL_SIZE, height=n * CELL_SIZE)
        self.canvas.pack()

        # Create a frame for control buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        # Previous button to step backwards through solutions
        self.prev_btn = tk.Button(btn_frame, text="⏮ Previous", command=self.show_prev)
        self.prev_btn.grid(row=0, column=0)

        # Next button to step forwards through solutions
        self.next_btn = tk.Button(btn_frame, text="Next ⏭", command=self.show_next)
        self.next_btn.grid(row=0, column=1)

        # Button to animate the solution placement
        self.animate_btn = tk.Button(btn_frame, text="▶ Animate Solution", command=self.start_animation)
        self.animate_btn.grid(row=0, column=2)

        # Bind mouse click for selecting queens
        self.canvas.bind("<Button-1>", self.on_click)
        # Bind double-click for placing a temporary queen
        self.canvas.bind("<Double-1>", self.on_double_click)

        # Initialize positions from the first solution in list
        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()  # Draw the initial board and queens

    def draw_board(self):
        """
        Render the chessboard, queens, highlights, and any temporary markers.
        """
        self.canvas.delete("all")  # Clear existing drawings
        # Draw board squares
        for i in range(self.n):
            for j in range(self.n):
                # Choose base color based on checker pattern
                base_color = BOARD_COLOR_1 if (i + j) % 2 == 0 else BOARD_COLOR_2
                # Highlight if selected queen threatens this square
                if self.selected_queen and self.threatens(self.selected_queen, (i, j)):
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = base_color

                # Draw the square rectangle
                self.canvas.create_rectangle(
                    j * CELL_SIZE, i * CELL_SIZE,
                    (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                    fill=fill, outline="black"
                )

        # Draw the actual queens for current solution
        for r, c in self.positions:
            x = c * CELL_SIZE + CELL_SIZE // 2  # Center x-coordinate
            y = r * CELL_SIZE + CELL_SIZE // 2  # Center y-coordinate
            self.canvas.create_text(x, y, text="♛", font=("Arial", 30), fill=QUEEN_COLOR)

        # Draw a temporary queen if user placed one
        if self.temp_queen:
            r, c = self.temp_queen
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", 30), fill="blue")

        # Draw conflict markers if any conflicts detected
        if self.conflict_pair:
            for r, c in self.conflict_pair:
                x = c * CELL_SIZE + CELL_SIZE // 2
                y = r * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_text(x, y, text="❌", font=("Arial", 30), fill=ERROR_COLOR)

    def show_next(self):
        """
        Advance to the next solution, wrapping around if at end.
        """
        # Do nothing if animation is in progress
        if self.animating:
            return
        # Move index forward and wrap
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.reset_temp()  # Clear any temporary markers
        # Update positions for the new solution
        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()  # Redraw board

    def show_prev(self):
        """
        Go to the previous solution, wrapping around if at start.
        """
        # Do nothing if animation is in progress
        if self.animating:
            return
        # Move index forward and wrap
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.reset_temp()  # Clear any temporary markers
        # Update positions for the new solution
        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()  # Redraw board

    def reset_temp(self):
        """
        Reset any user interactions: selected, temporary, or conflict markers.
        """
        self.selected_queen = None
        self.temp_queen = None
        self.conflict_pair = None

    def on_click(self, event):
        """
        Handle single-click: select or deselect a queen.
        """
        # Do nothing if animation is in progress
        if self.animating:
            return
        col = event.x // CELL_SIZE  # Compute board column from x-coordinate
        row = event.y // CELL_SIZE  # Compute board row from y-coordinate

        # Toggle selection if clicking on an existing queen
        if (row, col) in self.positions:
            self.selected_queen = (row, col)
        else:
            self.selected_queen = None
        self.draw_board()  # Redraw to show highlights

    def on_double_click(self, event):
        """
        Handle double-click: place a temporary queen and highlight conflicts.
        """
        # Do nothing if animation is in progress
        if self.animating:
            return
        col = event.x // CELL_SIZE  # Compute board column from x-coordinate
        row = event.y // CELL_SIZE  # Compute board row from y-coordinate
        self.temp_queen = (row, col)  # Place temp queen at clicked cell
        self.conflict_pair = []  # Prepare list for any conflicts

        # Check every real queen for conflicts with the temp queen
        for real_r, real_c in self.positions:
            if self.threatens((row, col), (real_r, real_c)):
                # Record both temp and real queen in conflict
                self.conflict_pair.append((row, col))
                self.conflict_pair.append((real_r, real_c))

        self.conflict_pair = list(set(self.conflict_pair))  # Remove duplicates
        self.draw_board()  # Show conflict markers

    def threatens(self, q1, q2):
        """
        Determine if two queens threaten each other.

        Args:
            q1, q2 (tuple[int,int]): Coordinates (row, col) of two queens.

        Returns:
            bool: True if same row, same column, or same diagonal.
        """
        r1, c1 = q1
        r2, c2 = q2
        # Check row, column, or diagonal threat
        return (
            r1 == r2 or  # same row
            c1 == c2 or  # same column
            abs(r1 - r2) == abs(c1 - c2)  # same diagonal
        )

    def start_animation(self):
        """
        Begin animating the placement of queens in sequence.
        """
        # Do nothing if animation is in progress
        if self.animating:
            return
        self.animating = True
        self.positions = []  # Clear positions to animate from empty board
        # Extract steps from the current solution
        self.solution_steps = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.step_index = 0  # Start at first queen
        self.animate_step()  # Kick off recursive animation

    def animate_step(self):
        """
        Show the next queen in the animation sequence.
        """
        # If there are more queens to place...
        if self.step_index < len(self.solution_steps):
            r, c = self.solution_steps[self.step_index]
            self.positions.append((r, c))  # Add next queen
            self.step_index += 1
            self.draw_board()  # Redraw board with new queen
            # Schedule next step after a delay
            self.root.after(ANIMATION_DELAY, self.animate_step)
        else:
            self.animating = False  # The animation is complete


def main():
    # Parse board size from command-line arguments
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python3 gui.py <board_size>")
        sys.exit(1)

    # Generate solutions via organ-pipe DLX solver
    solutions, _ = solve_nq_organ(n)
    if not solutions:
        print(f"No solutions found for {n}-Queens.")
        sys.exit(1)

    # Initialize and run the Tkinter GUI
    root = tk.Tk()
    root.title(f"{n}-Queens Visualizer")
    gui = NQueensGUI(root, n, solutions)
    root.mainloop()


main()
