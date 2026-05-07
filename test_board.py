import unittest

from board import Move, SudokuBoard


class TestSudokuBoard(unittest.TestCase):
    def setUp(self):
        grid = [
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
        self.board = SudokuBoard(grid)

    def test_get_and_set_cell(self):
        self.assertEqual(self.board.get_cell(0, 0), 5)

        self.board.set_cell(0, 2, 4)

        self.assertEqual(self.board.get_cell(0, 2), 4)

    def test_fixed_cell(self):
        self.assertTrue(self.board.is_fixed(0, 0))
        self.assertFalse(self.board.is_fixed(0, 2))

    def test_valid_and_invalid_move(self):
        valid_move = Move(0, 2, 4)
        invalid_move = Move(0, 2, 5)

        self.assertTrue(self.board.is_valid_move(valid_move))
        self.assertFalse(self.board.is_valid_move(invalid_move))

    def test_clear_cell(self):
        self.board.set_cell(0, 2, 4)

        self.assertTrue(self.board.clear_cell(0, 2))
        self.assertEqual(self.board.get_cell(0, 2), 0)
        self.assertFalse(self.board.clear_cell(0, 0))

    def test_find_empty(self):
        self.assertEqual(self.board.find_empty(), (0, 2))


if __name__ == "__main__":
    unittest.main()