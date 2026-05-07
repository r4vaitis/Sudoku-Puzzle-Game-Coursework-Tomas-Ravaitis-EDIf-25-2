# Sudoku Puzzle Game with Automatic Solver

## 1. Introduction

The goal of this coursework is to create a simple Sudoku puzzle game using Python and Pygame. The project topic is **Sudoku Solver**, but because it belongs to the **Games** category, the program was implemented as a playable Sudoku game with an automatic solving function.

The player can select cells with the mouse, enter numbers from the keyboard, use hints, save and load the game, reset the board, and solve the Sudoku automatically. The program also demonstrates object-oriented programming principles, file reading and writing, unit testing, and the Factory Method design pattern.

To run the program, the user needs to install the required library:

```bash
pip install -r requirements.txt
```

Then the game can be started with:

```bash
python main.py
```

The player clicks on an empty cell and presses a number from 1 to 9. If the move is valid, the number is placed on the board. If the move is invalid, the game shows a warning message. The game also includes buttons for solving, hints, saving, loading, and resetting.

## 2. Body / Analysis

### Main program structure

The project is divided into several Python files. Each file has its own purpose:

- `main.py` starts the program.
- `game.py` contains the main Pygame game loop, event handling, drawing, buttons, and game actions.
- `board.py` contains the Sudoku board logic.
- `solver.py` contains the abstract solver class and the backtracking solving algorithm.
- `solver_factory.py` creates solver objects using the Factory Method pattern.
- `file_manager.py` reads and writes Sudoku boards from and to text files.
- `puzzle.txt` stores the base Sudoku puzzle.
- `saved_puzzle.txt` stores the saved game.
- `solved_puzzle.txt` stores the solved puzzle.
- Test files check the main program functionality using `unittest`.

### How the game works

When the program starts, `SudokuGame` creates the Pygame window and loads a base puzzle from `puzzle.txt`. The program does not use this puzzle directly every time. Instead, it changes the numbers randomly, solves the board, and then removes random cells. Because of this, every new game looks different.

The player can choose a cell with the mouse. When the mouse is moved over the board, the program highlights the row, column, and 3x3 box of the current cell. This helps the player see the Sudoku structure more clearly.

The player can use the keyboard to enter numbers. The program checks if the move follows Sudoku rules. It checks the row, column, and 3x3 box before accepting the number.

### Encapsulation

Encapsulation means keeping data inside a class and using methods to work with it. In this project, encapsulation is shown in the `SudokuBoard` class.

The board data is stored in private-style variables:

```python
self._grid = []
self._start_grid = []
```

Other parts of the program do not need to work with the board list directly. Instead, they use methods such as:

```python
def get_cell(self, row, column):
    return self._grid[row][column]

def set_cell(self, row, column, value):
    self._grid[row][column] = value
```

The method `is_fixed()` checks if a cell was part of the original puzzle. This prevents the player from changing the starting numbers:

```python
def is_fixed(self, row, column):
    return self._start_grid[row][column] != 0
```

This keeps the board logic inside one class and makes the program easier to understand.

### Abstraction

Abstraction means creating a general structure and hiding unnecessary details. In this project, abstraction is used in `solver.py`.

The class `SudokuSolver` is an abstract class:

```python
class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, board):
        pass

    @abstractmethod
    def get_hint(self, board):
        pass
```

This means that every solver must have a `solve()` method and a `get_hint()` method. The abstract class does not describe the full solving process. It only defines what every solver should be able to do.

### Inheritance

Inheritance means creating a class based on another class. In this project, `BacktrackingSolver` inherits from `SudokuSolver`:

```python
class BacktrackingSolver(SudokuSolver):
```

`SudokuSolver` is the parent class, and `BacktrackingSolver` is the child class. The child class provides the actual implementation of the solving algorithm.

### Polymorphism

Polymorphism means that different classes can have the same method name and be used in the same way. In this project, the game uses the solver through the same `solve()` method:

```python
self.solver.solve(self.board)
```

At the moment, the project uses `BacktrackingSolver`. In the future, another solver could be added, for example `SmartSolver`, and the game could still call the same `solve()` method.

### Backtracking algorithm

The automatic solver uses the backtracking algorithm. Backtracking is a recursive trial-and-error method.

The algorithm works like this:

1. Find an empty cell.
2. Try numbers from 1 to 9.
3. Check if the number can be placed according to Sudoku rules.
4. If the number is valid, place it on the board.
5. Continue solving the next empty cell.
6. If the solution becomes impossible, remove the number and try another one.

The main part of the algorithm is in the `solve()` method:

```python
for number in range(1, 10):
    if board.can_place(row, column, number):
        board.set_cell(row, column, number)

        if self.solve(board):
            return True

        board.set_cell(row, column, 0)
```

This algorithm is suitable for Sudoku because Sudoku has a clear set of rules and a limited number of possible values in each cell.

### Factory Method design pattern

The project uses the Factory Method design pattern in `solver_factory.py`.

```python
class SolverFactory:
    def create_solver(self, solver_type):
        if solver_type == "backtracking":
            return BacktrackingSolver()

        return None
```

The game does not create the solver directly. Instead, it asks the factory to create the solver:

```python
self.solver = SolverFactory().create_solver("backtracking")
```

This pattern is suitable because different solving algorithms could be added later. For example, the program could have more than one solver type, and the factory would decide which solver object to create.

### Composition and aggregation

Composition means that one class contains objects of other classes. In this project, the `SudokuGame` class contains several objects:

```python
self.file_manager = FileManager()
self.solver = SolverFactory().create_solver("backtracking")
self.board = SudokuBoard(self.create_grid())
```

This means that the game is built from smaller parts. `SudokuGame` controls the game, `SudokuBoard` controls the board, `FileManager` works with files, and `BacktrackingSolver` solves the puzzle.

This makes the project more organized because every class has its own responsibility.

### Reading from file

The program reads the base Sudoku puzzle from `puzzle.txt`:

```python
grid = self.file_manager.read_board("puzzle.txt")
```

The file is read by the `FileManager` class:

```python
def read_board(self, file_name):
    grid = []
    file = open(file_name, "r", encoding="utf-8")
```

The program uses `puzzle.txt` as a base puzzle. After reading it, the program changes the numbers randomly and removes random cells. This gives the player a different board when starting or resetting the game.

### Writing to file

The program writes data to files in two cases.

When the player presses **Save**, the current board is saved to `saved_puzzle.txt`:

```python
self.file_manager.write_board("saved_puzzle.txt", self.board)
```

When the player presses **Solve**, the solved board is saved to `solved_puzzle.txt`:

```python
self.file_manager.write_board("solved_puzzle.txt", self.board)
```

The `FileManager` class writes the board row by row into a text file:

```python
def write_board(self, file_name, board):
    grid = board.get_grid()
    file = open(file_name, "w", encoding="utf-8")
```

This satisfies the requirement for writing to file.

### Main game functions

The main game functionality is located in `game.py`.

The `run()` method keeps the game running:

```python
def run(self):
    while self.running:
        self.events()
        self.draw()
        self.clock.tick(60)
```

The `events()` method checks mouse and keyboard events:

```python
def events(self):
    for event in pygame.event.get():
```

The `make_move()` method places a number only if the move is valid:

```python
if self.board.is_valid_move(move):
    self.board.set_cell(row, column, number)
```

The `hint()` method gives the player a correct number in a random empty cell. The player can use only three hints per game:

```python
if self.hints_left <= 0:
    self.message = "No hints left."
    return
```

The `reset()` method creates a new random board and restores the number of hints:

```python
self.board = SudokuBoard(self.create_grid())
self.hints_left = 3
```

### Testing

The project uses the `unittest` framework. The tests check the main functionality of the program.

The test files are:

- `test_board.py`
- `test_solver.py`
- `test_file_manager.py`
- `test_game.py`

`test_board.py` checks board methods, valid moves, fixed cells, and clearing cells.

`test_solver.py` checks if the backtracking solver can solve the Sudoku board and if the solved rows and columns contain numbers from 1 to 9.

`test_file_manager.py` checks reading and writing Sudoku boards to files.

`test_game.py` checks game functions such as hints, reset, and solving the board.

Tests can be run with:

```bash
python -m unittest
```

The tests focus on the core logic of the program. The Pygame window itself is not tested directly, because testing graphical interfaces is more complicated. Instead, the tests check the logic behind the game.

## 3. Results and Summary

- The project successfully implements a playable Sudoku game using Python and Pygame.
- The player can select cells, enter numbers, use hints, save, load, reset, and solve the puzzle automatically.
- The program reads the base puzzle from `puzzle.txt` and saves game data to text files.
- The project demonstrates encapsulation, abstraction, inheritance, polymorphism, composition, and the Factory Method design pattern.
- One challenge was connecting the Sudoku solving logic with the graphical Pygame interface.

## Conclusions

This coursework achieved the goal of creating a Sudoku puzzle game with an automatic solver. The final program is a simple but functional game where the player can solve Sudoku manually or use the automatic solver.

The project shows how object-oriented programming can be used to separate responsibilities between different classes. `SudokuBoard` manages the board, `BacktrackingSolver` solves the puzzle, `FileManager` works with files, and `SudokuGame` controls the game process.

In the future, the project could be improved by adding difficulty levels, a timer, a score system, a better visual design, and a menu screen. Another possible improvement would be adding more solving algorithms and using the Factory Method to choose between them.

## 4. Resources

- Python documentation
- Pygame documentation
- Python unittest documentation
