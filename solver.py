import random
from abc import ABC, abstractmethod

from board import Move


class SudokuSolver(ABC):
    @abstractmethod
    def solve(self, board):
        pass

    @abstractmethod
    def get_hint(self, board):
        pass


class BacktrackingSolver(SudokuSolver):
    def solve(self, board):
        empty = board.find_empty()

        if empty is None:
            return True

        row = empty[0]
        column = empty[1]

        for number in range(1, 10):
            if board.can_place(row, column, number):
                board.set_cell(row, column, number)

                if self.solve(board):
                    return True

                board.set_cell(row, column, 0)

        return False

    def get_hint(self, board):
        board_copy = board.make_copy()

        if not self.solve(board_copy):
            return None

        empty_cells = []

        for row in range(9):
            for column in range(9):
                if board.get_cell(row, column) == 0:
                    empty_cells.append((row, column))

        if len(empty_cells) == 0:
            return None

        cell = random.choice(empty_cells)
        row = cell[0]
        column = cell[1]
        value = board_copy.get_cell(row, column)

        return Move(row, column, value)