import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 8

class KonaneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Konane (Hawaiian Checkers)")
        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack()

        self.status_label = tk.Label(root, text="Turn: Black (Remove a piece)")
        self.status_label.pack()

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game, state=tk.DISABLED)
        self.restart_button.pack()

        self.pass_button = tk.Button(root, text="Pass", command=self.pass_turn, state=tk.DISABLED)
        self.pass_button.pack()

        self.board = []
        self.turn = 'B'
        self.selected = None
        self.phase = "opening"
        self.removed_black = None
        self.hint_moves = []
        self.multi_jump_active = False
        self.game_over = False  

        self.init_board()
        self.highlight_starting_moves()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_board()
        self.show_start_popup()

    def show_start_popup(self):
        messagebox.showinfo("Konane", "Welcome to Konane!\n\nBlack removes a corner or center piece to start.")

    def init_board(self):
        self.board = [['B' if (i + j) % 2 == 0 else 'W' for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    def highlight_starting_moves(self):
        """Highlights the valid starting moves for Black (corners and center pieces)."""
        self.hint_moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.is_corner_or_center(r, c) and self.board[r][c] == 'B']

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 60
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x0, y0, x1, y1 = j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size
                fill = "white" if (i + j) % 2 == 0 else "lightgray"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill)

                if (i, j) in self.hint_moves:
                    highlight_color = "blue" if self.phase == "opening" and self.turn == "B" else "green"
                    self.canvas.create_rectangle(x0 + 5, y0 + 5, x1 - 5, y1 - 5, outline=highlight_color, width=3)

                if self.selected == (i, j):
                    self.canvas.create_rectangle(x0 + 5, y0 + 5, x1 - 5, y1 - 5, outline="red", width=3)

                piece = self.board[i][j]
                if piece:
                    color = "black" if piece == 'B' else "white"
                    self.canvas.create_oval(x0 + 10, y0 + 10, x1 - 10, y1 - 10, fill=color)

    def on_click(self, event):
        if self.game_over:
            return

        row, col = event.y // 60, event.x // 60

        if self.phase == "opening":
            self.handle_opening_phase(row, col)
        else:
            self.handle_play_phase(row, col)

        self.draw_board()

    def handle_opening_phase(self, row, col):
        piece = self.board[row][col]

        if self.turn == 'B':
            if piece != 'B' or not self.is_corner_or_center(row, col):
                return
            self.board[row][col] = ''
            self.removed_black = (row, col)
            self.turn = 'W'
            self.status_label.config(text="Turn: White (Remove adjacent piece)")
            self.hint_moves = self.get_adjacent_white(row, col)

        elif self.turn == 'W':
            if piece != 'W' or (row, col) not in self.hint_moves:
                return
            self.board[row][col] = ''
            self.turn = 'B'
            self.phase = "play"
            self.status_label.config(text="Turn: Black (Play)")
            self.hint_moves = []

    def is_corner_or_center(self, row, col):
        return (row, col) in [(0, 0), (0, BOARD_SIZE - 1), (BOARD_SIZE - 1, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1),
                              (BOARD_SIZE // 2, BOARD_SIZE // 2), (BOARD_SIZE // 2 - 1, BOARD_SIZE // 2 - 1)]

    def get_adjacent_white(self, row, col):
        return [(r, c) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if 0 <= (r := row + dr) < BOARD_SIZE and 0 <= (c := col + dc) < BOARD_SIZE and self.board[r][c] == 'W']

    def get_valid_jumps(self, row, col):
        moves = []
        opponent = 'W' if self.turn == 'B' else 'B'

        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            r, c, mid_r, mid_c = row + dr, col + dc, row + dr // 2, col + dc // 2
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[mid_r][mid_c] == opponent and self.board[r][c] == '':
                moves.append((r, c))

        return moves

    def handle_play_phase(self, row, col):
        piece = self.board[row][col]

        if self.selected is None:
            if piece == self.turn and not self.multi_jump_active:
                self.selected = (row, col)
                self.hint_moves = self.get_valid_jumps(row, col)
        else:
            if (row, col) in self.hint_moves:
                self.make_jump(self.selected, (row, col))
            elif (row, col) == self.selected:
                if self.multi_jump_active:  
                    return
                self.selected, self.hint_moves = None, []

            elif piece == self.turn and not self.multi_jump_active:
                self.selected = (row, col)
                self.hint_moves = self.get_valid_jumps(row, col)

        self.draw_board()

    def make_jump(self, start, end):
        sr, sc, er, ec = *start, *end
        mid_r, mid_c = (sr + er) // 2, (sc + ec) // 2

        self.board[er][ec], self.board[sr][sc], self.board[mid_r][mid_c] = self.board[sr][sc], '', ''

        self.selected = end
        self.hint_moves = self.get_valid_jumps(er, ec)

        if self.hint_moves:
            self.multi_jump_active = True
            self.pass_button.config(state=tk.NORMAL)
        else:
            self.multi_jump_active = False
            self.pass_button.config(state=tk.DISABLED)
            self.end_turn()

    def pass_turn(self):
        self.multi_jump_active = False
        self.pass_button.config(state=tk.DISABLED)
        self.end_turn()

    def end_turn(self):
        self.selected, self.hint_moves = None, []
        self.turn = 'W' if self.turn == 'B' else 'B'
        self.status_label.config(text=f"Turn: {'Black' if self.turn == 'B' else 'White'}")
        
        if not self.has_valid_move(self.turn):
            opponent = 'W' if self.turn == 'B' else 'B'
            
            if not self.has_valid_move(opponent):
                # If neither player has a move, announce winner
                self.turn = opponent  # Allow the opponent to make their last move
                self.draw_board()  # Ensure the last move is reflected visually
                self.root.after(500, self.declare_winner)  # Delay to show the last move

    def declare_winner(self):
        winner = "Black" if self.turn == "B" else "White"
        messagebox.showinfo("Game Over", f"{winner} Wins!")
        self.restart_button.config(state=tk.NORMAL)



    def has_valid_move(self, player):
        return any(self.get_valid_jumps(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == player)

    def restart_game(self):
        """Resets the game state without closing the window."""
        self.canvas.delete("all")  # Clear the canvas
        self.status_label.config(text="Turn: Black (Remove a piece)")
        self.restart_button.config(state=tk.DISABLED)
        self.pass_button.config(state=tk.DISABLED)

        self.board = []
        self.turn = 'B'
        self.selected = None
        self.phase = "opening"
        self.removed_black = None
        self.hint_moves = []
        self.multi_jump_active = False
        self.game_over = False  

        self.init_board()
        self.highlight_starting_moves()
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    game = KonaneGame(root)
    root.mainloop()

