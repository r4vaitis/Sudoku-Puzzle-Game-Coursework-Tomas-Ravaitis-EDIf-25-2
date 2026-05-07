import os
import random
import pygame

from board import Move, SudokuBoard
from file_manager import FileManager
from solver_factory import SolverFactory


class SudokuGame:
    def __init__(self):
        pygame.init()
        self.width = 540
        self.height = 670
        self.cell = 60
        self.board_y = 20

        self.white = (250, 250, 250)
        self.black = (30, 30, 30)
        self.gray = (225, 225, 225)
        self.blue = (50, 100, 200)
        self.light_blue = (210, 230, 255)
        self.light_green = (210, 245, 215)
        self.red = (180, 50, 50)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku Game")
        self.font = pygame.font.SysFont("arial", 34)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.message_font = pygame.font.SysFont("arial", 20)

        self.file_manager = FileManager()
        self.solver = SolverFactory().create_solver("backtracking")
        self.board = SudokuBoard(self.create_grid())

        self.selected = None
        self.hovered = None
        self.hints_left = 3
        self.message = "Choose a cell and press number 1-9."
        self.running = True
        self.clock = pygame.time.Clock()

        self.buttons = {
            "solve": pygame.Rect(10, 595, 96, 40),
            "hint": pygame.Rect(116, 595, 96, 40),
            "save": pygame.Rect(222, 595, 96, 40),
            "load": pygame.Rect(328, 595, 96, 40),
            "reset": pygame.Rect(434, 595, 96, 40),
        }

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
                number = grid[row][column]
                if number != 0:
                    grid[row][column] = numbers[number - 1]

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
            elif event.type == pygame.MOUSEMOTION:
                self.hovered = self.get_cell(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.key_press(event.key)

    def get_cell(self, position):
        x, y = position

        if 0 <= x < 540 and self.board_y <= y < self.board_y + 540:
            return (y - self.board_y) // self.cell, x // self.cell

        return None

    def mouse_click(self, position):
        cell = self.get_cell(position)

        if cell is not None:
            self.selected = cell
            self.message = "Cell selected."
            return

        for name in self.buttons:
            if self.buttons[name].collidepoint(position):
                if name == "solve":
                    self.solve()
                elif name == "hint":
                    self.hint()
                elif name == "save":
                    self.save()
                elif name == "load":
                    self.load()
                elif name == "reset":
                    self.reset()

    def key_press(self, key):
        if self.selected is None:
            return

        row, column = self.selected

        if pygame.K_1 <= key <= pygame.K_9:
            self.make_move(row, column, key - pygame.K_0)
        elif pygame.K_KP1 <= key <= pygame.K_KP9:
            self.make_move(row, column, key - pygame.K_KP0)
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
                self.message = "Congratulations! Sudoku is completed."
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

        if len(empty) == 0:
            self.message = "Board is already completed."
            return

        row, column = random.choice(empty)
        value = board_copy.get_cell(row, column)
        self.board.set_cell(row, column, value)
        self.hints_left -= 1
        self.message = "Hint used. Hints left: " + str(self.hints_left)

    def save(self):
        self.file_manager.write_board("saved_puzzle.txt", self.board)
        self.message = "Game saved."

    def load(self):
        if not os.path.exists("saved_puzzle.txt"):
            self.message = "No saved puzzle found."
            return

        grid = self.file_manager.read_board("saved_puzzle.txt")
        self.board = SudokuBoard(grid)
        self.selected = None
        self.hovered = None
        self.message = "Saved puzzle loaded."

    def reset(self):
        self.board = SudokuBoard(self.create_grid())
        self.selected = None
        self.hovered = None
        self.hints_left = 3
        self.message = "New game started."

    def draw(self):
        self.screen.fill(self.white)
        self.draw_highlight()

        for row in range(9):
            for column in range(9):
                x = column * self.cell
                y = self.board_y + row * self.cell
                number = self.board.get_cell(row, column)

                if self.board.is_fixed(row, column):
                    pygame.draw.rect(
                        self.screen,
                        self.gray,
                        (x, y, self.cell, self.cell)
                    )

                if number != 0:
                    color = self.black
                    if not self.board.is_fixed(row, column):
                        color = self.blue

                    text = self.font.render(str(number), True, color)
                    rect = text.get_rect(center=(x + 30, y + 30))
                    self.screen.blit(text, rect)

        self.draw_grid()
        self.draw_buttons()
        self.draw_message()
        pygame.display.flip()

    def draw_highlight(self):
        cell = self.hovered

        if cell is None:
            cell = self.selected

        if cell is None:
            return

        row, column = cell
        box_row = row // 3 * 3
        box_column = column // 3 * 3

        pygame.draw.rect(
            self.screen,
            self.light_blue,
            (0, self.board_y + row * self.cell, 540, self.cell)
        )
        pygame.draw.rect(
            self.screen,
            self.light_blue,
            (column * self.cell, self.board_y, self.cell, 540)
        )
        pygame.draw.rect(
            self.screen,
            self.light_green,
            (
                box_column * self.cell,
                self.board_y + box_row * self.cell,
                self.cell * 3,
                self.cell * 3
            )
        )

    def draw_grid(self):
        for i in range(10):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen,
                self.black,
                (i * self.cell, self.board_y),
                (i * self.cell, self.board_y + 540),
                width
            )
            pygame.draw.line(
                self.screen,
                self.black,
                (0, self.board_y + i * self.cell),
                (540, self.board_y + i * self.cell),
                width
            )

    def draw_buttons(self):
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, self.gray, rect, border_radius=7)
            pygame.draw.rect(self.screen, self.black, rect, 2, border_radius=7)

            text = self.small_font.render(name.capitalize(), True, self.black)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_message(self):
        text = self.message_font.render(self.message, True, self.red)
        rect = text.get_rect(center=(self.width // 2, 650))
        self.screen.blit(text, rect)