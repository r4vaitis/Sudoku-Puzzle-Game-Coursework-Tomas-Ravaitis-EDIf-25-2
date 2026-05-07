# Sudoku Puzzle Game with Automatic Solver

This is a simple Sudoku puzzle game created with Python and Pygame.

The project topic is **Sudoku Solver**, but because it belongs to the **Games**
category, the program was made as a playable Sudoku game. The player can play
Sudoku manually, use hints, reset the game, and solve the puzzle automatically.

## Main Features

- Graphical Sudoku board made with Pygame
- Mouse cell selection
- Keyboard number input
- Move validation according to Sudoku rules
- 3 hints available per game
- Automatic Sudoku solver
- Randomized Sudoku board generation
- Reset button for a new game
- Reading a base puzzle from `puzzle.txt`
- Saving the solved puzzle to `solved_puzzle.txt`
- Unit tests using `unittest`

## How to Run the Program

Install the required library:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python main.py
```

If `python` does not work on Windows, use:

```bash
py main.py
```

## How to Play

1. Start the program.
2. Click on an empty cell.
3. Press a number from 1 to 9 on the keyboard.
4. If the move is correct, the number appears on the board.
5. If the move is incorrect, the game shows a warning message.
6. Press **Hint** to reveal one correct number.
7. Only 3 hints can be used in one game.
8. Press **Solve** to solve the whole puzzle automatically.
9. Press **Reset** to start a new randomized game.

## Project Files

- `main.py` - starts the program
- `game.py` - contains the main Pygame game logic
- `board.py` - contains `SudokuBoard` and `Move` classes
- `solver.py` - contains the abstract solver and backtracking solver
- `solver_factory.py` - creates solver objects using Factory Method
- `file_manager.py` - reads and writes Sudoku boards
- `puzzle.txt` - stores the base Sudoku puzzle
- `solved_puzzle.txt` - stores the solved Sudoku after pressing Solve
- `test_board.py` - tests the board logic
- `test_solver.py` - tests the solving algorithm
- `test_file_manager.py` - tests file reading and writing
- `test_game.py` - tests main game functions
- `requirements.txt` - contains required libraries

## How to Run Tests

Run all tests:

```bash
python -m unittest
```

On Windows, if `python` does not work, use:

```bash
py -m unittest
```

## Technologies Used

- Python
- Pygame
- unittest
- TXT files

## Author

Tomas Ravaitis
