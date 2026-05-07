# Sudoku Puzzle Game with Automatic Solver

## 1. Introduction

The goal of this coursework is to create a simple Sudoku puzzle game using
Python and Pygame. The coursework topic is **Sudoku Solver**, but because the
topic belongs to the **Games** category, the application was implemented as a
playable Sudoku game with an automatic solving function.

The application allows the player to select cells with the mouse, enter numbers
from the keyboard, use hints, reset the board, and solve the Sudoku
automatically. The program also demonstrates object-oriented programming
principles, file reading and writing, unit testing, and the Factory Method
design pattern.

To run the program, the user needs to install the required library:

```bash
pip install -r requirements.txt
```

Then the game can be started with:

```bash
python main.py
```

If `python` does not work on Windows, the program can be started with:

```bash
py main.py
```

The player clicks on a cell and presses a number from 1 to 9. The program checks
whether the move is valid according to Sudoku rules. The player can also use
the **Hint**, **Solve**, and **Reset** buttons.

## 2. Body / Analysis

### Project structure

The project is divided into several files:

- `main.py` starts the program.
- `game.py` contains the main Pygame game logic.
- `board.py` contains the Sudoku board logic.
- `solver.py` contains the solving algorithm.
- `solver_factory.py` contains the Factory Method pattern.
- `file_manager.py` reads and writes Sudoku boards.
- `puzzle.txt` contains the base Sudoku puzzle.
- `solved_puzzle.txt` stores the solved board after pressing Solve.
- Test files check the main logic using the `unittest` framework.

### Main application logic

The main game logic is located in `game.py`. The class `SudokuGame` creates the
Pygame window, draws the board, handles mouse clicks and keyboard input, and
controls the game buttons.

At the start of the game, the program reads a base Sudoku puzzle from
`puzzle.txt`. Then the numbers are changed randomly, the board is solved, and
45 random cells are removed. Because of this, the board is different when the
game starts again.

The player can select a cell with the mouse and enter a number using the
keyboard. The program checks if the move is valid before placing the number on
the board.

The game has three main buttons:

- **Solve** - solves the Sudoku and saves the result to `solved_puzzle.txt`.
- **Hint** - reveals one correct value in a random empty cell.
- **Reset** - creates a new randomized game.

### Encapsulation

Encapsulation means keeping data inside a class and using methods to work with
it. In this project, encapsulation is used in the `SudokuBoard` class.

The board is stored in private-style attributes:

```python
self._grid = [row.copy() for row in grid]
self._start_grid = [row.copy() for row in grid]
```

The game does not work with these lists directly. Instead, it uses methods such
as:

```python
def get_cell(self, row, column):
    return self._grid[row][column]

def set_cell(self, row, column, value):
    self._grid[row][column] = value
```

This keeps the Sudoku board logic inside one class.

### Abstraction

Abstraction means defining only the important structure and hiding unnecessary
details. In this project, abstraction is used in `solver.py`.

The class `SudokuSolver` is an abstract class:

```python
class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, board):
        pass
```

It defines that every solver must have a `solve()` method. The real solving
logic is implemented in the child class `BacktrackingSolver`.

### Inheritance

Inheritance means creating a class based on another class. In this project,
`BacktrackingSolver` inherits from `SudokuSolver`:

```python
class BacktrackingSolver(SudokuSolver):
```

`SudokuSolver` is the parent class, and `BacktrackingSolver` is the child class.
The child class provides the actual backtracking algorithm.

### Polymorphism

Polymorphism means that different classes can use the same method name and be
used in the same way. In this project, the game calls the solver through the
same method:

```python
self.solver.solve(self.board)
```

At the moment, the program uses `BacktrackingSolver`. In the future, another
solver class could be added with the same `solve()` method, and the game logic
would still work.

### Backtracking algorithm

The automatic solver uses the backtracking algorithm. Backtracking is a
recursive trial-and-error method.

The algorithm works like this:

1. Find an empty cell.
2. Try numbers from 1 to 9.
3. Check if the number follows Sudoku rules.
4. If the number is valid, place it on the board.
5. Continue solving the next empty cell.
6. If the solution becomes impossible, remove the number and try another one.

The main part of the algorithm is:

```python
for number in range(1, 10):
    if board.can_place(row, column, number):
        board.set_cell(row, column, number)

        if self.solve(board):
            return True

        board.set_cell(row, column, 0)
```

This algorithm is suitable for Sudoku because every cell has a limited number of
possible values.

### Factory Method design pattern

The project uses the Factory Method design pattern in `solver_factory.py`.

```python
class SolverFactory:
    def create_solver(self, solver_type):
        if solver_type == "backtracking":
            return BacktrackingSolver()

        return None
```

The game does not create the solver directly. It asks the factory to create it:

```python
self.solver = SolverFactory().create_solver("backtracking")
```

This pattern is suitable because different solving algorithms could be added in
the future. For example, the program could later include another solver type.

### Composition

Composition means that one class contains objects of other classes. In this
project, `SudokuGame` contains several objects:

```python
self.file_manager = FileManager()
self.solver = SolverFactory().create_solver("backtracking")
self.board = SudokuBoard(self.create_grid())
```

This means that the game is built from smaller parts. `SudokuGame` controls the
game process, `SudokuBoard` manages the board, `FileManager` works with files,
and `BacktrackingSolver` solves the puzzle.

### Reading from file

The program reads the base puzzle from `puzzle.txt`:

```python
grid = self.file_manager.read_board("puzzle.txt")
```

The file is read in `file_manager.py`:

```python
def read_board(self, file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return [
            [int(number) for number in line.split()]
            for line in file
        ]
```

This satisfies the file reading requirement.

### Writing to file

The program writes the solved board to `solved_puzzle.txt` when the player
presses the Solve button:

```python
self.file_manager.write_board("solved_puzzle.txt", self.board)
```

The writing logic is located in `file_manager.py`:

```python
def write_board(self, file_name, board):
    with open(file_name, "w", encoding="utf-8") as file:
        for row in board.get_grid():
            file.write(" ".join(str(number) for number in row) + "\n")
```

This satisfies the file writing requirement.

### Testing

The project uses the `unittest` framework. The tests check the main logic of the
program.

The test files are:

- `test_board.py`
- `test_solver.py`
- `test_file_manager.py`
- `test_game.py`

`test_board.py` checks board functions, fixed cells, valid moves, clearing
cells, and finding an empty cell.

`test_solver.py` checks if the backtracking solver can solve the Sudoku puzzle.

`test_file_manager.py` checks writing and reading a board from a file.

`test_game.py` checks important game functions such as hints, reset, and solve.

Tests can be run with:

```bash
python -m unittest
```

The Pygame window itself is not tested directly. Instead, the tests check the
logic behind the game.

## 3. Results and Summary

- The project successfully implements a playable Sudoku game using Python and
  Pygame.
- The player can select cells, enter numbers, use hints, reset the game, and
  solve the Sudoku automatically.
- The program reads a base puzzle from `puzzle.txt` and writes the solved puzzle
  to `solved_puzzle.txt`.
- Unit tests were created to check the main functionality of the program.
- One challenge was connecting the Sudoku solving algorithm with the Pygame game
  interface.

## Conclusions

This coursework achieved the goal of creating a Sudoku puzzle game with an
automatic solver. The final program is simple, but it is functional and follows
the main coursework requirements.

The project demonstrates object-oriented programming principles, including
encapsulation, abstraction, inheritance, and polymorphism. It also uses
composition, the Factory Method design pattern, file input and output, and unit
testing.

In the future, the program could be improved by adding difficulty levels, a
timer, a score system, save and load buttons, a better visual design, and a menu
screen.

## 4. Resources

- Python documentation
- Pygame documentation
- Python unittest documentation
