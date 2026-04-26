import os
import unittest

from board import SudokuBoard
from file_manager import FileManager


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager()
        self.file_name = "test_puzzle.txt"
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

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_write_and_read_board(self):
        board = SudokuBoard(self.grid)

        self.file_manager.write_board(self.file_name, board)
        loaded_grid = self.file_manager.read_board(self.file_name)

        self.assertEqual(loaded_grid, self.grid)


if __name__ == "__main__":
    unittest.main()