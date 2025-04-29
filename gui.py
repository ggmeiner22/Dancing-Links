import tkinter as tk
import sys
import time
from organpipe import solve_nq_organ  # you can swap with solve_nq_organ if you want

CELL_SIZE = 60
BOARD_COLOR_1 = "#EEEED2"
BOARD_COLOR_2 = "#769656"
HIGHLIGHT_COLOR = "#FFD700"
QUEEN_COLOR = "black"
ERROR_COLOR = "red"

ANIMATION_DELAY = 200  # Milliseconds between moves during solving

class NQueensGUI:
    def __init__(self, root, n, solutions):
        self.root = root
        self.n = n
        self.solutions = solutions
        self.current_index = 0
        self.selected_queen = None
        self.temp_queen = None
        self.conflict_pair = None
        self.animating = False

        self.canvas = tk.Canvas(root, width=n * CELL_SIZE, height=n * CELL_SIZE)
        self.canvas.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.prev_btn = tk.Button(btn_frame, text="⏮ Previous", command=self.show_prev)
        self.prev_btn.grid(row=0, column=0)

        self.next_btn = tk.Button(btn_frame, text="Next ⏭", command=self.show_next)
        self.next_btn.grid(row=0, column=1)

        self.animate_btn = tk.Button(btn_frame, text="▶ Animate Solution", command=self.start_animation)
        self.animate_btn.grid(row=0, column=2)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Double-1>", self.on_double_click)

        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.n):
            for j in range(self.n):
                base_color = BOARD_COLOR_1 if (i + j) % 2 == 0 else BOARD_COLOR_2
                if self.selected_queen and self.threatens(self.selected_queen, (i, j)):
                    fill = HIGHLIGHT_COLOR
                else:
                    fill = base_color

                self.canvas.create_rectangle(
                    j * CELL_SIZE, i * CELL_SIZE,
                    (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE,
                    fill=fill, outline="black"
                )

        # Draw real queens
        for r, c in self.positions:
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", 30), fill=QUEEN_COLOR)

        # Draw temp queen if user placed one
        if self.temp_queen:
            r, c = self.temp_queen
            x = c * CELL_SIZE + CELL_SIZE // 2
            y = r * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_text(x, y, text="♛", font=("Arial", 30), fill="blue")

        # Draw conflicts
        if self.conflict_pair:
            for r, c in self.conflict_pair:
                x = c * CELL_SIZE + CELL_SIZE // 2
                y = r * CELL_SIZE + CELL_SIZE // 2
                self.canvas.create_text(x, y, text="❌", font=("Arial", 30), fill=ERROR_COLOR)

    def show_next(self):
        if self.animating:
            return
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.reset_temp()
        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()

    def show_prev(self):
        if self.animating:
            return
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.reset_temp()
        self.positions = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.draw_board()

    def reset_temp(self):
        self.selected_queen = None
        self.temp_queen = None
        self.conflict_pair = None

    def on_click(self, event):
        if self.animating:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if (row, col) in self.positions:
            self.selected_queen = (row, col)
        else:
            self.selected_queen = None
        self.draw_board()

    def on_double_click(self, event):
        if self.animating:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        self.temp_queen = (row, col)
        self.conflict_pair = []

        for real_r, real_c in self.positions:
            if self.threatens((row, col), (real_r, real_c)):
                self.conflict_pair.append((row, col))
                self.conflict_pair.append((real_r, real_c))

        self.conflict_pair = list(set(self.conflict_pair))
        self.draw_board()

    def threatens(self, q1, q2):
        r1, c1 = q1
        r2, c2 = q2
        return (
            r1 == r2 or
            c1 == c2 or
            abs(r1 - r2) == abs(c1 - c2)
        )

    def start_animation(self):
        if self.animating:
            return
        self.animating = True
        self.positions = []
        self.solution_steps = [(node.row_data[0], node.row_data[1]) for node in self.solutions[self.current_index]]
        self.step_index = 0
        self.animate_step()

    def animate_step(self):
        if self.step_index < len(self.solution_steps):
            r, c = self.solution_steps[self.step_index]
            self.positions.append((r, c))
            self.step_index += 1
            self.draw_board()
            self.root.after(ANIMATION_DELAY, self.animate_step)
        else:
            self.animating = False  # Animation complete

def main():
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        print("Usage: python3 gui.py <board_size>")
        sys.exit(1)

    solutions, _ = solve_nq_organ(n)  # you can swap with organpipe if you want
    if not solutions:
        print(f"No solutions found for {n}-Queens.")
        sys.exit(1)

    root = tk.Tk()
    root.title(f"{n}-Queens Visualizer")
    gui = NQueensGUI(root, n, solutions)
    root.mainloop()

main()