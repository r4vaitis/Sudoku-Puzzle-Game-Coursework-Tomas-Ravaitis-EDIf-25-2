# Sudoku Puzzle Game with Automatic Solver

## 1. Introduction

The goal of this coursework is to create a simple Sudoku puzzle game using Python and Pygame. The application lets the user play Sudoku in a graphical window, select cells with the mouse, enter numbers from the keyboard, use hints, reset the game, and solve the whole puzzle automatically.

The topic of the project is a game, because the program has a playable graphical interface and the user interacts with the Sudoku board. The automatic solver is added as an extra function inside the game.

The program also demonstrates object-oriented programming principles, file reading and writing, unit testing, and one design pattern.

### How to run the program

First, install the required library:

```bash
pip install -r requirements.txt
```

Then run the game:

```bash
python main.py
```

### How to use the program

After starting the game, the user can click on an empty cell and press a number from 1 to 9. If the move follows Sudoku rules, the number is placed into the cell. If the move is wrong, the program shows a warning message.

The user can also press the Hint button to reveal one correct number. Only three hints can be used during one game. The Solve button solves the whole Sudoku automatically and saves the solved board to a file. The Reset button starts a new random puzzle.

## 2. Body / Analysis

### Main functionality

The main functionality of the program is split between several files. The file `main.py` starts the program. The file `game.py` contains the Pygame window and game loop. The file `board.py` contains the board logic. The file `solver.py` contains the automatic Sudoku solving algorithm. The file `file_manager.py` is used for reading and writing text files.

The application loads a Sudoku puzzle from `puzzle.txt`. After that, the program changes the numbers and removes random cells, so the game does not always start with exactly the same board. The player can solve the Sudoku manually, use hints, reset the game, or solve it automatically.

### Encapsulation

Encapsulation means that data is stored inside a class, and other parts of the program work with that data through methods. In this project, the Sudoku grid is stored inside the `SudokuBoard` class.

```python
class SudokuBoard:
    def __init__(self, grid):
        self._grid = []
        self._start_grid = []
```

The grid is not supposed to be edited directly from other classes. Instead, the program uses methods such as `get_cell`, `set_cell`, `clear_cell`, and `can_place`.

```python
def get_cell(self, row, column):
    return self._grid[row][column]


def set_cell(self, row, column, value):
    self._grid[row][column] = value
```

This makes the board logic easier to control, because all operations with the board are inside one class.

### Inheritance

Inheritance means that one class can be based on another class. In this project, `BacktrackingSolver` inherits from the abstract class `SudokuSolver`.

```python
class BacktrackingSolver(SudokuSolver):
    def solve(self, board):
```

The class `SudokuSolver` describes the basic structure for a solver, and `BacktrackingSolver` is a specific solver that actually solves the Sudoku puzzle.

### Abstraction

Abstraction means showing only the important structure and hiding the implementation details. In this project, `SudokuSolver` is an abstract class.

```python
class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, board):
        pass
```

This means that every solver class must have a `solve()` method. The game does not need to know every small detail of the solving algorithm. It only calls the solver when it needs to solve the puzzle.

### Polymorphism

Polymorphism means that different classes can use the same method name, but the method can work differently depending on the object. In this project, the game calls the solver using the same method name:

```python
self.solver.solve(self.board)
```

At the moment, the program uses `BacktrackingSolver`. In the future, another solver class could be created, for example `SmartSolver`, and the game could still call the same `solve()` method.

### Design pattern

The project uses the Factory Method design pattern. It is implemented in `solver_factory.py`.

```python
class SolverFactory:
    def create_solver(self, solver_type):
        if solver_type == "backtracking":
            return BacktrackingSolver()

        return None
```

This pattern is suitable for this project because the game does not create the solver directly. Instead, it asks the factory to create the needed solver. This makes the code easier to extend later if more Sudoku solving methods are added.

For this project, Factory Method is more suitable than Singleton or Builder. Singleton is not really needed because the game does not need one global object for the whole application. Builder is also not necessary because solver objects are simple. Factory Method fits better because the application may need different types of solvers.

### Composition and aggregation

Composition means that one class contains objects of other classes. In this project, the `SudokuGame` class contains objects such as `FileManager`, `SudokuBoard`, and the solver.

```python
self.file_manager = FileManager()
self.board = SudokuBoard(grid)
self.solver = factory.create_solver("backtracking")
```

This shows that the game is built from smaller parts. Each part has its own responsibility. The board controls Sudoku rules, the solver solves the puzzle, the file manager works with files, and the game class connects everything with the Pygame interface.

### File reading and writing

The program reads the starting Sudoku puzzle from the file `puzzle.txt`.

```python
grid = self.file_manager.read_board("puzzle.txt")
```

The program also writes the solved board to `solved_puzzle.txt` after the user presses the Solve button.

```python
self.file_manager.write_board("solved_puzzle.txt", self.board)
```

This satisfies the requirement for reading from a file and writing to a file.

### Sudoku solving algorithm

The automatic solver uses the backtracking algorithm. The algorithm finds an empty cell, tries numbers from 1 to 9, and checks if the number can be placed there. If the number works, the algorithm continues. If it later reaches a wrong path, it goes back and tries another number.

```python
for number in range(1, 10):
    if board.can_place(row, column, number):
        board.set_cell(row, column, number)

        if self.solve(board):
            return True

        board.set_cell(row, column, 0)
```

This algorithm is useful for Sudoku because it can search through possible solutions until it finds the correct one.

### Pygame interface

The graphical part of the game is made with Pygame. The program draws the Sudoku grid, numbers, selected cell, buttons, and messages.

The player uses the mouse to select a cell and the keyboard to enter a number. The buttons are also handled with mouse clicks.

```python
if self.solve_button.collidepoint(position):
    self.solve_game()

if self.hint_button.collidepoint(position):
    self.give_hint()

if self.reset_button.collidepoint(position):
    self.reset_game()
```

### Hint system

The game allows only three hints during one game. When the user presses the Hint button, the program solves a copy of the current board and then reveals one random empty cell.

```python
if self.hints_left <= 0:
    self.message = "No hints left."
    return
```

This makes the game more balanced, because the user cannot use unlimited hints.

### Testing

The project uses the `unittest` framework. The tests check the main functionality of the application.

The test files are:

- `test_board.py`
- `test_solver.py`
- `test_file_manager.py`
- `test_game.py`

The tests check board logic, valid and invalid moves, fixed cells, the solving algorithm, file reading and writing, hints, reset, and solving the game.

Tests can be run with this command:

```bash
python -m unittest
```

## 3. Results and Summary

- The final result is a playable Sudoku puzzle game with a graphical interface made in Pygame.
- The program can read a Sudoku puzzle from a text file and save the solved puzzle to another text file.
- The user can select cells, enter numbers, use three hints, reset the puzzle, and solve the puzzle automatically.
- The project uses object-oriented programming, including encapsulation, inheritance, abstraction, and polymorphism.
- One of the main challenges was connecting the Sudoku solving logic with the Pygame interface.

## 4. Conclusions

This coursework achieved the goal of creating a simple Sudoku puzzle game using Python and Pygame. The final program is not only a solver, but also a playable game where the user can interact with the board.

The project helped demonstrate how object-oriented programming can be used in a real application. The code includes classes for the board, game, solver, factory, and file manager. The Factory Method pattern was used to create the solver object.

The program also includes file input and output, because it reads the starting puzzle from `puzzle.txt` and saves the solved puzzle to `solved_puzzle.txt`. Unit tests were created to check the core functionality.

In the future, this application could be improved by adding difficulty levels, a timer, a score system, a main menu, better graphics, and more solving algorithms.

## 5. Resources

- Python documentation
- Pygame documentation
- Python unittest documentation
