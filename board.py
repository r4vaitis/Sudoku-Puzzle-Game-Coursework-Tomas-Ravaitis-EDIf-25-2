class Move:
    def __init__(self, row, column, value):
        self.row = row
        self.column = column
        self.value = value


class SudokuBoard:
    def __init__(self, grid):
        self._grid = [row.copy() for row in grid]
        self._start_grid = [row.copy() for row in grid]

    def get_grid(self):
        return [row.copy() for row in self._grid]

    def get_cell(self, row, column):
        return self._grid[row][column]

    def set_cell(self, row, column, value):
        self._grid[row][column] = value

    def is_fixed(self, row, column):
        return self._start_grid[row][column] != 0

    def clear_cell(self, row, column):
        if self.is_fixed(row, column):
            return False

        self._grid[row][column] = 0
        return True

    def is_valid_move(self, move):
        if self.is_fixed(move.row, move.column):
            return False

        return self.can_place(move.row, move.column, move.value)

    def can_place(self, row, column, value):
        if value < 1 or value > 9:
            return False

        for i in range(9):
            if i != column and self._grid[row][i] == value:
                return False

            if i != row and self._grid[i][column] == value:
                return False

        box_row = row // 3 * 3
        box_column = column // 3 * 3

        for i in range(box_row, box_row + 3):
            for j in range(box_column, box_column + 3):
                if i != row or j != column:
                    if self._grid[i][j] == value:
                        return False

        return True

    def find_empty(self):
        for row in range(9):
            for column in range(9):
                if self._grid[row][column] == 0:
                    return row, column

        return None

    def is_complete(self):
        return self.find_empty() is None

    def make_copy(self):
        return SudokuBoard(self.get_grid())