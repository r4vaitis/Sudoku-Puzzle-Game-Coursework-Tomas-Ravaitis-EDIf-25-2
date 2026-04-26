import unittest

from board import Move, SudokuBoard


class TestSudokuBoard(unittest.TestCase):
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

    def test_get_cell(self):
        self.assertEqual(self.board.get_cell(0, 0), 5)

    def test_set_cell(self):
        self.board.set_cell(0, 2, 4)
        self.assertEqual(self.board.get_cell(0, 2), 4)

    def test_fixed_cell(self):
        self.assertTrue(self.board.is_fixed(0, 0))
        self.assertFalse(self.board.is_fixed(0, 2))

    def test_valid_move(self):
        move = Move(0, 2, 4)
        self.assertTrue(self.board.is_valid_move(move))

    def test_invalid_move_same_row(self):
        move = Move(0, 2, 5)
        self.assertFalse(self.board.is_valid_move(move))

    def test_invalid_move_fixed_cell(self):
        move = Move(0, 0, 1)
        self.assertFalse(self.board.is_valid_move(move))

    def test_clear_cell(self):
        self.board.set_cell(0, 2, 4)
        result = self.board.clear_cell(0, 2)

        self.assertTrue(result)
        self.assertEqual(self.board.get_cell(0, 2), 0)

    def test_cannot_clear_fixed_cell(self):
        result = self.board.clear_cell(0, 0)

        self.assertFalse(result)
        self.assertEqual(self.board.get_cell(0, 0), 5)

    def test_find_empty(self):
        self.assertEqual(self.board.find_empty(), (0, 2))


if __name__ == "__main__":
    unittest.main()