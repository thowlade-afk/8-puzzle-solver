import random
import tkinter as tk
from tkinter import messagebox

GOAL = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# --- look and feel -------------------------------------------------------
TILE = 100
GAP = 8
PAD = 12
BOARD_PX = PAD * 2 + TILE * 3 + GAP * 2
BG = "#f3f1ec"
BOARD_BG = "#3b4a54"
TILE_BG = "#e8b84a"
TILE_FG = "#2a2a2a"
BLANK_BG = "#2e3a42"
FONT_TILE = ("Helvetica", 36, "bold")
FONT_UI = ("Helvetica", 12)
STEP_DELAY_MS = 600


def neighbors_of_blank(state):
    """Return board indexes the blank can swap with (used only to shuffle)."""
    b = state.index(0)
    r, c = divmod(b, 3)
    out = []
    if r > 0:
        out.append(b - 3)
    if r < 2:
        out.append(b + 3)
    if c > 0:
        out.append(b - 1)
    if c < 2:
        out.append(b + 1)
    return out


def random_board(moves=60):
    """Shuffle by making legal moves from the goal, so it is always solvable."""
    while True:
        state = GOAL[:]
        prev_blank = None
        for _ in range(moves):
            b = state.index(0)
            options = [n for n in neighbors_of_blank(state) if n != prev_blank]
            n = random.choice(options)
            state[b], state[n] = state[n], state[b]
            prev_blank = b
        if state != GOAL:
            return state


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        root.title("8-Puzzle Solver")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.board = random_board()
        self.solution = []
        self.step = 0
        self.animating = False
        self.after_id = None

        self.canvas = tk.Canvas(
            root, width=BOARD_PX, height=BOARD_PX, bg=BOARD_BG, highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        self.status = tk.Label(
            root, text="Press Solve to run A*.", bg=BG, font=FONT_UI, height=2
        )
        self.status.grid(row=1, column=0, columnspan=2)

        self.rand_btn = tk.Button(
            root, text="Randomize", font=FONT_UI, width=12, command=self.randomize
        )
        self.rand_btn.grid(row=2, column=0, padx=10, pady=(5, 20))

        self.solve_btn = tk.Button(
            root, text="Solve", font=FONT_UI, width=12, command=self.solve
        )
        self.solve_btn.grid(row=2, column=1, padx=10, pady=(5, 20))

        self.draw(self.board)

    # ---- drawing --------------------------------------------------------
    def draw(self, state):
        self.canvas.delete("all")
        for i, value in enumerate(state):
            r, c = divmod(i, 3)
            x = PAD + c * (TILE + GAP)
            y = PAD + r * (TILE + GAP)
            if value == 0:
                self.canvas.create_rectangle(
                    x, y, x + TILE, y + TILE, fill=BLANK_BG, outline=""
                )
            else:
                self.canvas.create_rectangle(
                    x, y, x + TILE, y + TILE, fill=TILE_BG, outline=""
                )
                self.canvas.create_text(
                    x + TILE / 2,
                    y + TILE / 2,
                    text=str(value),
                    font=FONT_TILE,
                    fill=TILE_FG,
                )

    # ---- buttons --------------------------------------------------------
    def set_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        self.rand_btn.config(state=state)
        self.solve_btn.config(state=state)

    def randomize(self):
        self.board = random_board()
        self.solution = []
        self.draw(self.board)
        self.status.config(text="New board. Press Solve to run A*.")

    def solve(self):
        if self.animating:
            return

        if self.board == GOAL:
            self.status.config(text="The board is already solved. Press Randomize.")
            return

        # Import here so the window still opens if solver.py has an error.
        try:
            import solver
        except ImportError:
            messagebox.showerror(
                "Solver not found",
                "Could not import solver.py.\n"
                "Make sure solver.py is in the same folder as app.py.",
            )
            return

        self.status.config(text="Solving...")
        self.root.update_idletasks()

        try:
            result = solver.solve(self.board[:])
        except Exception as e:  # show solver bugs instead of crashing silently
            messagebox.showerror("Solver error", f"solver.solve() raised:\n{e}")
            self.status.config(text="Solver error.")
            return

        if not result:
            self.status.config(text="No solution found for this board.")
            return

        self.solution = [list(s) for s in result]
        self.step = 0
        self.animating = True
        self.set_buttons(False)
        self.play_step()

    # ---- animation ------------------------------------------------------
    def play_step(self):
        state = self.solution[self.step]
        self.draw(state)
        last = len(self.solution) - 1
        self.status.config(text=f"Move {self.step} of {last}")

        if self.step < last:
            self.step += 1
            self.after_id = self.root.after(STEP_DELAY_MS, self.play_step)
        else:
            self.board = state[:]
            self.animating = False
            self.set_buttons(True)
            self.status.config(text=f"Solved in {last} moves.")


def main():
    root = tk.Tk()
    PuzzleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
