# Konane (Hawaiian Checkers) Game

This is a Python implementation of Konane, a traditional Hawaiian board game, built using the Tkinter library for a graphical user interface (GUI).

## Game Overview

Konane is similar to checkers, where two players (Black and White) take turns to remove pieces from the board. The goal is to be the last player who can make a move. Players remove one piece at a time by jumping over an opponent's piece, with the jumped piece being removed from the board. The game starts with Black removing a corner or center piece, followed by White removing an adjacent piece, and then the game proceeds to the main playing phase.

### Features:
- **Opening Phase:** Black starts by removing a corner or center piece. White removes an adjacent piece.
- **Play Phase:** Players take turns jumping over opponent pieces, with multiple jumps allowed on a single turn.
- **Game End:** The game ends when no player has a valid move. The player who cannot make a move loses, and the opponent wins.

## Installation

To run this game, you need to have Python installed on your computer. This implementation uses the Tkinter library, which is included with Python, so there are no external dependencies to install.

1. Make sure you have Python 3.x installed. You can check by running:
    ```bash
    python --version
    ```

2. Download or clone this repository to your local machine.

## Running the Game

To start the game:

1. Navigate to the directory where the `konane.py` file is located.
2. Run the following command:
    ```bash
    python konane.py
    ```

This will open a window displaying the Konane board, where you can start playing.

## Game Controls

- **Left Click:** Select a piece to move or jump.
- **Pass Turn Button:** When no valid moves are available for a player, they can pass their turn.
- **Restart Button:** After a game is over, the "Restart" button will become available to restart the game.

### Starting the Game:
- The game will show a popup message to welcome you and explain the opening phase of the game.
- Black will be the first player to make a move by removing a corner or center piece.

### During the Game:
- Players take turns removing pieces by jumping over an opponent's piece.
- The board will highlight the available moves in blue or green during the opening phase and during play.
- The turn will automatically switch after a valid move or when the "Pass" button is pressed.

### End of the Game:
- The game ends when neither player has a valid move left.
- A message box will pop up, announcing the winner.

## Functions

### `KonaneGame.__init__(self, root)`
Initializes the game window, board, and game settings.

### `KonaneGame.show_start_popup(self)`
Displays a welcome popup at the start of the game.

### `KonaneGame.init_board(self)`
Sets up the initial board configuration.

### `KonaneGame.highlight_starting_moves(self)`
Highlights the valid starting moves for the Black player during the opening phase.

### `KonaneGame.draw_board(self)`
Draws the game board and updates the visual state.

### `KonaneGame.on_click(self, event)`
Handles mouse click events for selecting and moving pieces.

### `KonaneGame.handle_opening_phase(self, row, col)`
Handles the opening phase of the game (Black and White removing pieces).

### `KonaneGame.handle_play_phase(self, row, col)`
Handles the play phase where players make moves by jumping over pieces.

### `KonaneGame.make_jump(self, start, end)`
Handles the logic for jumping over an opponent's piece and updating the board.

### `KonaneGame.pass_turn(self)`
Allows the current player to pass their turn when no valid move is available.

### `KonaneGame.end_turn(self)`
Ends the current player's turn and switches to the opponent.

### `KonaneGame.has_valid_move(self, player)`
Checks if the given player has any valid moves left.

### `KonaneGame.declare_winner(self)`
Declares the winner when the game ends.

### `KonaneGame.restart_game(self)`
Restarts the game, resetting all game states and variables.



## Acknowledgments

- Tkinter documentation for GUI creation.
- The game logic is inspired by the traditional Hawaiian game of Konane.

