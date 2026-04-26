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
        self.game.give_hint()
        self.game.give_hint()
        self.game.give_hint()
        self.game.give_hint()

        self.assertEqual(self.game.hints_left, 0)
        self.assertEqual(self.game.message, "No hints left.")

    def test_hint_adds_number(self):
        empty_before = self.count_empty_cells()

        self.game.give_hint()

        empty_after = self.count_empty_cells()

        self.assertEqual(empty_after, empty_before - 1)

    def test_reset_game_restores_hints(self):
        self.game.give_hint()

        self.assertEqual(self.game.hints_left, 2)

        self.game.reset_game()

        self.assertEqual(self.game.hints_left, 3)

    def test_solve_game_completes_board(self):
        self.game.solve_game()

        self.assertTrue(self.game.board.is_complete())

    def count_empty_cells(self):
        count = 0

        for row in range(9):
            for column in range(9):
                if self.game.board.get_cell(row, column) == 0:
                    count += 1

        return count


if __name__ == "__main__":
    unittest.main()