# Sudoku Puzzle Game

This is a simple Sudoku puzzle game created with Python and Pygame.

The player can play Sudoku in a graphical window, select cells with the mouse, enter numbers from the keyboard, use hints, reset the game, and solve the puzzle automatically.

## Main Features

- Graphical Sudoku board made with Pygame
- Mouse cell selection
- Keyboard number input
- Move validation according to Sudoku rules
- 3 available hints per game
- Automatic Sudoku solver
- Randomized puzzle generation
- Reset button
- Reading puzzle data from a text file
- Saving solved puzzle to a text file
- Unit tests with unittest

## How to Run the Program

First, install the required library:

```bash
pip install -r requirements.txt
```

Then run the program:

```bash
python main.py
```

## How to Play

1. Start the game.
2. Click on an empty cell.
3. Press a number from 1 to 9 on the keyboard.
4. If the move is valid, the number will appear in the cell.
5. If the move is wrong, the game will show a warning message.
6. Press Hint to reveal one correct number.
7. Only 3 hints can be used during one game.
8. Press Solve to solve the whole puzzle automatically.
9. Press Reset to start a new random game.

## Project Files

- main.py - starts the game
- game.py - contains the main Pygame game logic
- board.py - contains SudokuBoard and Move classes
- solver.py - contains the abstract solver and backtracking solver
- solver_factory.py - creates solver objects using Factory Method
- file_manager.py - reads and writes Sudoku boards from and to files
- puzzle.txt - contains the starting Sudoku puzzle
- solved_puzzle.txt - stores the solved Sudoku after pressing Solve
- test_board.py - tests Sudoku board logic
- test_solver.py - tests the solving algorithm
- test_file_manager.py - tests file reading and writing
- test_game.py - tests some game functions
- requirements.txt - contains required libraries

## How to Run Tests

To run all unit tests, use:

```bash
python -m unittest
```

The tests check the main functionality of the program, such as board validation, solving, file reading and writing, hints, and reset logic.

## Technologies Used

- Python
- Pygame
- unittest
- TXT files for data storage

## Author

Tomas Ravaitis
