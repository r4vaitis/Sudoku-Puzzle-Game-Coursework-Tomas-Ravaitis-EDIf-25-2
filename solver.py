from abc import ABC, abstractmethod


class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, board):
        pass


class BacktrackingSolver(SudokuSolver):
    def solve(self, board):
        empty = board.find_empty()

        if empty is None:
            return True

        row, column = empty

        for number in range(1, 10):
            if board.can_place(row, column, number):
                board.set_cell(row, column, number)

                if self.solve(board):
                    return True

                board.set_cell(row, column, 0)

        return False