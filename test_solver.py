import unittest

from board import SudokuBoard
from solver import BacktrackingSolver


class TestBacktrackingSolver(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        self.board = SudokuBoard(self.grid)
        self.solver = BacktrackingSolver()

    def test_solver_solves_board(self):
        result = self.solver.solve(self.board)

        self.assertTrue(result)
        self.assertTrue(self.board.is_complete())

    def test_solved_rows_are_correct(self):
        self.solver.solve(self.board)
        grid = self.board.get_grid()

        for row in grid:
            self.assertEqual(sorted(row), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_solved_columns_are_correct(self):
        self.solver.solve(self.board)
        grid = self.board.get_grid()

        for column in range(9):
            numbers = []

            for row in range(9):
                numbers.append(grid[row][column])

            self.assertEqual(sorted(numbers), [1, 2, 3, 4, 5, 6, 7, 8, 9])


if __name__ == "__main__":
    unittest.main()