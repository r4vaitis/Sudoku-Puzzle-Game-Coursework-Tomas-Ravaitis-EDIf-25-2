import random

import pygame

from board import Move, SudokuBoard
from file_manager import FileManager
from solver_factory import SolverFactory


class SudokuGame:
    def __init__(self):
        pygame.init()

        self.cell = 60
        self.board_y = 20
        self.screen = pygame.display.set_mode((540, 650))
        pygame.display.set_caption("Sudoku Game")

        self.font = pygame.font.SysFont("arial", 34)
        self.small_font = pygame.font.SysFont("arial", 20)

        self.white = (250, 250, 250)
        self.black = (30, 30, 30)
        self.gray = (225, 225, 225)
        self.blue = (50, 100, 200)
        self.red = (180, 50, 50)
        self.light_blue = (210, 230, 255)

        self.file_manager = FileManager()
        self.solver = SolverFactory().create_solver("backtracking")
        self.board = SudokuBoard(self.create_grid())

        self.selected = None
        self.hints_left = 3
        self.message = "Choose a cell and press number 1-9."
        self.running = True
        self.clock = pygame.time.Clock()

        self.solve_button = pygame.Rect(65, 585, 120, 40)
        self.hint_button = pygame.Rect(210, 585, 120, 40)
        self.reset_button = pygame.Rect(355, 585, 120, 40)

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def create_grid(self):
        grid = self.file_manager.read_board("puzzle.txt")
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(numbers)

        for row in range(9):
            for column in range(9):
                value = grid[row][column]

                if value != 0:
                    grid[row][column] = numbers[value - 1]

        board = SudokuBoard(grid)
        self.solver.solve(board)
        grid = board.get_grid()

        cells = []

        for row in range(9):
            for column in range(9):
                cells.append((row, column))

        random.shuffle(cells)

        for row, column in cells[:45]:
            grid[row][column] = 0

        return grid

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                self.key_press(event.key)

    def mouse_click(self, position):
        x, y = position

        if 0 <= x < 540 and self.board_y <= y < 560:
            row = (y - self.board_y) // self.cell
            column = x // self.cell
            self.selected = (row, column)
            self.message = "Cell selected."
            return

        if self.solve_button.collidepoint(position):
            self.solve()
        elif self.hint_button.collidepoint(position):
            self.hint()
        elif self.reset_button.collidepoint(position):
            self.reset()

    def key_press(self, key):
        if self.selected is None:
            return

        row, column = self.selected

        if pygame.K_1 <= key <= pygame.K_9:
            self.make_move(row, column, key - pygame.K_0)

        elif key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            if self.board.clear_cell(row, column):
                self.message = "Cell cleared."
            else:
                self.message = "You cannot clear original cells."

    def make_move(self, row, column, number):
        move = Move(row, column, number)

        if self.board.is_valid_move(move):
            self.board.set_cell(row, column, number)
            self.message = "Move accepted."

            if self.board.is_complete():
                self.message = "Sudoku completed."
        else:
            self.message = "Wrong move."

    def solve(self):
        if self.solver.solve(self.board):
            self.file_manager.write_board("solved_puzzle.txt", self.board)
            self.message = "Sudoku solved and saved."
        else:
            self.message = "Sudoku cannot be solved."

    def hint(self):
        if self.hints_left <= 0:
            self.message = "No hints left."
            return

        board_copy = self.board.make_copy()

        if not self.solver.solve(board_copy):
            self.message = "No hint available."
            return

        empty = []

        for row in range(9):
            for column in range(9):
                if self.board.get_cell(row, column) == 0:
                    empty.append((row, column))

        if not empty:
            self.message = "Board is already completed."
            return

        row, column = random.choice(empty)
        value = board_copy.get_cell(row, column)

        self.board.set_cell(row, column, value)
        self.hints_left -= 1
        self.message = "Hints left: " + str(self.hints_left)

    def reset(self):
        self.board = SudokuBoard(self.create_grid())
        self.selected = None
        self.hints_left = 3
        self.message = "New game started."

    def draw(self):
        self.screen.fill(self.white)

        if self.selected is not None:
            row, column = self.selected
            pygame.draw.rect(
                self.screen,
                self.light_blue,
                (
                    column * self.cell,
                    self.board_y + row * self.cell,
                    self.cell,
                    self.cell,
                ),
            )

        for row in range(9):
            for column in range(9):
                self.draw_cell(row, column)

        self.draw_grid()
        self.draw_button(self.solve_button, "Solve")
        self.draw_button(self.hint_button, "Hint")
        self.draw_button(self.reset_button, "Reset")
        self.draw_message()

        pygame.display.flip()

    def draw_cell(self, row, column):
        x = column * self.cell
        y = self.board_y + row * self.cell
        value = self.board.get_cell(row, column)

        if self.board.is_fixed(row, column):
            pygame.draw.rect(
                self.screen,
                self.gray,
                (x, y, self.cell, self.cell),
            )

        if value == 0:
            return

        color = self.black

        if not self.board.is_fixed(row, column):
            color = self.blue

        text = self.font.render(str(value), True, color)
        rect = text.get_rect(center=(x + 30, y + 30))
        self.screen.blit(text, rect)

    def draw_grid(self):
        for i in range(10):
            width = 4 if i % 3 == 0 else 1

            pygame.draw.line(
                self.screen,
                self.black,
                (i * self.cell, self.board_y),
                (i * self.cell, self.board_y + 540),
                width,
            )

            pygame.draw.line(
                self.screen,
                self.black,
                (0, self.board_y + i * self.cell),
                (540, self.board_y + i * self.cell),
                width,
            )

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, self.gray, rect)
        pygame.draw.rect(self.screen, self.black, rect, 2)

        button_text = self.small_font.render(text, True, self.black)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def draw_message(self):
        text = self.small_font.render(self.message, True, self.red)
        rect = text.get_rect(center=(270, 635))
        self.screen.blit(text, rect)