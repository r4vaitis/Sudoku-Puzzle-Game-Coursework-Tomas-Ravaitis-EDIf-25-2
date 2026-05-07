import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

from game import SudokuGame


class TestSudokuGame(unittest.TestCase):
    def setUp(self):
        self.game = SudokuGame()

    def tearDown(self):
        pygame.quit()

    def test_hint_can_be_used_three_times(self):
        self.game.hint()
        self.game.hint()
        self.game.hint()
        self.game.hint()

        self.assertEqual(self.game.hints_left, 0)
        self.assertEqual(self.game.message, "No hints left.")

    def test_hint_adds_number(self):
        empty_before = self.count_empty_cells()

        self.game.hint()

        empty_after = self.count_empty_cells()

        self.assertEqual(empty_after, empty_before - 1)

    def test_reset_restores_hints(self):
        self.game.hint()

        self.assertEqual(self.game.hints_left, 2)

        self.game.reset()

        self.assertEqual(self.game.hints_left, 3)
        self.assertEqual(self.game.message, "New game started.")

    def test_solve_completes_board(self):
        self.game.solve()

        self.assertTrue(self.game.board.is_complete())
        self.assertEqual(self.game.message, "Sudoku solved and saved.")

    def test_save_creates_file(self):
        self.game.save()

        self.assertTrue(os.path.exists("saved_puzzle.txt"))
        self.assertEqual(self.game.message, "Game saved.")

    def test_load_saved_game(self):
        self.game.save()
        self.game.reset()
        self.game.load()

        self.assertEqual(self.game.message, "Saved puzzle loaded.")

    def count_empty_cells(self):
        count = 0

        for row in range(9):
            for column in range(9):
                if self.game.board.get_cell(row, column) == 0:
                    count += 1

        return count


if __name__ == "__main__":
    unittest.main()