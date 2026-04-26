import math
import os
import random

import pygame

from board import Move, SudokuBoard
from file_manager import FileManager
from solver_factory import SolverFactory
from ui import SudokuUI


class SudokuGame:
    def __init__(self):
        pygame.init()

        self.width = 540
        self.height = 670
        self.cell_size = 60
        self.board_y = 20

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku Game")

        self.file_manager = FileManager()

        factory = SolverFactory()
        self.solver = factory.create_solver("backtracking")

        grid = self.create_random_grid()
        self.board = SudokuBoard(grid)
        self.start_grid = grid

        self.ui = SudokuUI(
            self.screen,
            self.width,
            self.height,
            self.cell_size,
            self.board_y
        )

        self.state = "menu"
        self.language = "English"
        self.languages = ["English", "Lietuviu", "Русский", "Polski"]

        self.selected = None
        self.hovered = None
        self.hints_left = 3
        self.message = self.get_text("choose")
        self.running = True
        self.clock = pygame.time.Clock()

        self.game_alpha = 0
        self.pulse_time = 0
        self.polish_flags = []

        self.menu_buttons = {
            "play": pygame.Rect(170, 235, 200, 50),
            "settings": pygame.Rect(170, 305, 200, 50),
            "about": pygame.Rect(170, 375, 200, 50)
        }

        self.settings_buttons = {
            "English": pygame.Rect(170, 210, 200, 42),
            "Lietuviu": pygame.Rect(170, 265, 200, 42),
            "Русский": pygame.Rect(170, 320, 200, 42),
            "Polski": pygame.Rect(170, 375, 200, 42),
            "back": pygame.Rect(170, 500, 200, 42)
        }

        self.about_buttons = {
            "back": pygame.Rect(170, 550, 200, 42)
        }

        self.game_buttons = {
            "solve": pygame.Rect(10, 595, 96, 40),
            "hint": pygame.Rect(116, 595, 96, 40),
            "save": pygame.Rect(222, 595, 96, 40),
            "load": pygame.Rect(328, 595, 96, 40),
            "reset": pygame.Rect(434, 595, 96, 40)
        }

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def get_texts(self):
        texts = {
            "English": {
                "play": "Play",
                "settings": "Settings",
                "about": "About",
                "back": "Back",
                "choose_language": "Choose language",
                "choose": "Choose a cell and press number 1-9.",
                "cell_selected": "Cell selected.",
                "accepted": "Move accepted.",
                "wrong": "Wrong move.",
                "completed": "Congratulations! You completed Sudoku.",
                "cleared": "Cell cleared.",
                "cannot_clear": "You cannot clear original cells.",
                "solved": "Sudoku solved and saved to file.",
                "cannot_solve": "Sudoku cannot be solved.",
                "no_hints": "No hints left.",
                "no_hint": "No hint available.",
                "already_done": "Board is already completed.",
                "hint_used": "Hint used. Hints left: ",
                "saved": "Game saved to saved_puzzle.txt.",
                "no_save": "No saved puzzle found.",
                "loaded": "Saved puzzle loaded.",
                "new_game": "New random game started.",
                "about_lines": [
                    "This is a Sudoku puzzle game made with Python.",
                    "The game uses Pygame for the graphical interface.",
                    "The player can enter numbers, use hints, save, load,",
                    "reset the game and solve the puzzle automatically.",
                    "Author: Tomas Ravaitis"
                ]
            },
            "Lietuviu": {
                "play": "Zaisti",
                "settings": "Nustatymai",
                "about": "Apie",
                "back": "Atgal",
                "choose_language": "Pasirinkite kalba",
                "choose": "Pasirinkite langeli ir spauskite 1-9.",
                "cell_selected": "Langelis pasirinktas.",
                "accepted": "Ejimas priimtas.",
                "wrong": "Neteisingas ejimas.",
                "completed": "Sveikiname! Sudoku uzbaigtas.",
                "cleared": "Langelis isvalytas.",
                "cannot_clear": "Pradiniu langeliu keisti negalima.",
                "solved": "Sudoku isspriestas ir issaugotas.",
                "cannot_solve": "Sudoku negali buti isspriestas.",
                "no_hints": "Pagalbu nebeliko.",
                "no_hint": "Pagalba negalima.",
                "already_done": "Lenta jau uzpildyta.",
                "hint_used": "Pagalba panaudota. Liko: ",
                "saved": "Zaidimas issaugotas i saved_puzzle.txt.",
                "no_save": "Issaugoto zaidimo nera.",
                "loaded": "Issaugotas zaidimas ikeltas.",
                "new_game": "Pradetas naujas atsitiktinis zaidimas.",
                "about_lines": [
                    "Tai Sudoku zaidimas, sukurtas su Python.",
                    "Grafinei sasajai naudojama Pygame biblioteka.",
                    "Zaidejas gali rasyti skaicius, naudoti pagalbas,",
                    "issaugoti, ikelti, pradeti is naujo ir spresti automatiskai.",
                    "Autorius: Tomas Ravaitis"
                ]
            },
            "Русский": {
                "play": "Играть",
                "settings": "Настройки",
                "about": "Об игре",
                "back": "Назад",
                "choose_language": "Выберите язык",
                "choose": "Выберите клетку и нажмите число 1-9.",
                "cell_selected": "Клетка выбрана.",
                "accepted": "Ход принят.",
                "wrong": "Неверный ход.",
                "completed": "Поздравляю! Судоку завершено.",
                "cleared": "Клетка очищена.",
                "cannot_clear": "Начальные клетки нельзя менять.",
                "solved": "Судоку решено и сохранено в файл.",
                "cannot_solve": "Судоку невозможно решить.",
                "no_hints": "Подсказок больше нет.",
                "no_hint": "Подсказка недоступна.",
                "already_done": "Поле уже заполнено.",
                "hint_used": "Подсказка использована. Осталось: ",
                "saved": "Игра сохранена в saved_puzzle.txt.",
                "no_save": "Сохранения нет.",
                "loaded": "Сохранённая игра загружена.",
                "new_game": "Начата новая случайная игра.",
                "about_lines": [
                    "Это игра Судоку, созданная на Python.",
                    "Для графического интерфейса используется Pygame.",
                    "Игрок может вводить числа, использовать подсказки,",
                    "сохранять, загружать, сбрасывать и решать судоку.",
                    "Автор: Tomas Ravaitis"
                ]
            },
            "Polski": {
                "play": "Graj",
                "settings": "Ustawienia",
                "about": "O grze",
                "back": "Wroc",
                "choose_language": "Wybierz jezyk",
                "choose": "Wybierz pole i nacisnij liczbe 1-9.",
                "cell_selected": "Pole wybrane.",
                "accepted": "Ruch przyjety.",
                "wrong": "Zly ruch.",
                "completed": "Gratulacje! Sudoku zakonczone.",
                "cleared": "Pole wyczyszczone.",
                "cannot_clear": "Poczatkowych pol nie mozna zmieniac.",
                "solved": "Sudoku rozwiazane i zapisane do pliku.",
                "cannot_solve": "Sudoku nie moze byc rozwiazane.",
                "no_hints": "Brak podpowiedzi.",
                "no_hint": "Podpowiedz niedostepna.",
                "already_done": "Plansza jest juz ukonczona.",
                "hint_used": "Podpowiedz uzyta. Zostalo: ",
                "saved": "Gra zapisana do saved_puzzle.txt.",
                "no_save": "Brak zapisanego sudoku.",
                "loaded": "Zapisane sudoku wczytane.",
                "new_game": "Nowa losowa gra rozpoczeta.",
                "about_lines": [
                    "To jest gra Sudoku stworzona w Pythonie.",
                    "Interfejs graficzny zostal wykonany w Pygame.",
                    "Gracz moze wpisywac liczby, uzywac podpowiedzi,",
                    "zapisywac, wczytywac, resetowac i rozwiazac sudoku.",
                    "Autor: Tomas Ravaitis"
                ]
            }
        }

        return texts[self.language]

    def get_text(self, key):
        return self.get_texts()[key]

    def update(self):
        if self.state == "game" and self.game_alpha < 255:
            self.game_alpha += 5

            if self.game_alpha > 255:
                self.game_alpha = 255

        if self.state == "settings" and self.language == "Polski":
            self.update_polish_flags()
            self.pulse_time += 0.05

    def create_random_grid(self):
        grid = self.file_manager.read_board("puzzle.txt")
        grid = self.change_numbers(grid)

        board = SudokuBoard(grid)
        self.solver.solve(board)

        full_grid = board.get_grid()
        cells = []

        for row in range(9):
            for column in range(9):
                cells.append((row, column))

        random.shuffle(cells)

        for i in range(45):
            row = cells[i][0]
            column = cells[i][1]
            full_grid[row][column] = 0

        return full_grid

    def change_numbers(self, grid):
        old_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        new_numbers = old_numbers.copy()
        random.shuffle(new_numbers)

        new_grid = []

        for row in grid:
            new_row = []

            for number in row:
                if number == 0:
                    new_row.append(0)
                else:
                    new_row.append(new_numbers[number - 1])

            new_grid.append(new_row)

        return new_grid

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                self.check_menu_events(event)

            elif self.state == "settings":
                self.check_settings_events(event)

            elif self.state == "about":
                self.check_about_events(event)

            elif self.state == "game":
                self.check_game_events(event)

    def check_menu_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_buttons["play"].collidepoint(event.pos):
                self.state = "game"
                self.game_alpha = 0
                self.message = self.get_text("choose")

            if self.menu_buttons["settings"].collidepoint(event.pos):
                self.state = "settings"

            if self.menu_buttons["about"].collidepoint(event.pos):
                self.state = "about"

    def check_settings_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for language in self.languages:
                if self.settings_buttons[language].collidepoint(event.pos):
                    self.language = language
                    self.message = self.get_text("choose")

                    if language == "Polski":
                        self.create_polish_flags()
                    else:
                        self.polish_flags = []

            if self.settings_buttons["back"].collidepoint(event.pos):
                self.state = "menu"

    def check_about_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.about_buttons["back"].collidepoint(event.pos):
                self.state = "menu"

    def check_game_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_hover(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_game_mouse(event.pos)

        if event.type == pygame.KEYDOWN:
            self.handle_keyboard(event.key)

    def create_polish_flags(self):
        self.polish_flags = []

        for i in range(20):
            width = random.randint(35, 90)
            height = int(width * 0.6)

            flag = {
                "x": random.randint(0, self.width - width),
                "y": random.randint(-700, -50),
                "width": width,
                "height": height,
                "speed": random.uniform(0.6, 2.0),
                "alpha": random.randint(70, 140)
            }

            self.polish_flags.append(flag)

    def update_polish_flags(self):
        if len(self.polish_flags) == 0:
            self.create_polish_flags()

        for flag in self.polish_flags:
            flag["y"] += flag["speed"]

            if flag["y"] > self.height:
                width = random.randint(35, 90)
                height = int(width * 0.6)

                flag["x"] = random.randint(0, self.width - width)
                flag["y"] = random.randint(-250, -50)
                flag["width"] = width
                flag["height"] = height
                flag["speed"] = random.uniform(0.6, 2.0)
                flag["alpha"] = random.randint(70, 140)

    def handle_hover(self, position):
        x = position[0]
        y = position[1]

        if 0 <= x < 540 and self.board_y <= y < self.board_y + 540:
            row = (y - self.board_y) // self.cell_size
            column = x // self.cell_size
            self.hovered = (row, column)
        else:
            self.hovered = None

    def handle_game_mouse(self, position):
        x = position[0]
        y = position[1]

        if 0 <= x < 540 and self.board_y <= y < self.board_y + 540:
            row = (y - self.board_y) // self.cell_size
            column = x // self.cell_size
            self.selected = (row, column)
            self.message = self.get_text("cell_selected")
            return

        if self.game_buttons["solve"].collidepoint(position):
            self.solve_game()

        if self.game_buttons["hint"].collidepoint(position):
            self.give_hint()

        if self.game_buttons["save"].collidepoint(position):
            self.save_game()

        if self.game_buttons["load"].collidepoint(position):
            self.load_game()

        if self.game_buttons["reset"].collidepoint(position):
            self.reset_game()

    def handle_keyboard(self, key):
        if self.selected is None:
            return

        row = self.selected[0]
        column = self.selected[1]

        if pygame.K_1 <= key <= pygame.K_9:
            number = key - pygame.K_0
            self.make_move(row, column, number)

        if pygame.K_KP1 <= key <= pygame.K_KP9:
            number = key - pygame.K_KP0
            self.make_move(row, column, number)

        if key == pygame.K_BACKSPACE or key == pygame.K_DELETE:
            if self.board.clear_cell(row, column):
                self.message = self.get_text("cleared")
            else:
                self.message = self.get_text("cannot_clear")

    def make_move(self, row, column, number):
        move = Move(row, column, number)

        if self.board.is_valid_move(move):
            self.board.set_cell(row, column, number)

            if self.board.is_complete():
                self.message = self.get_text("completed")
            else:
                self.message = self.get_text("accepted")
        else:
            self.message = self.get_text("wrong")

    def solve_game(self):
        if self.solver.solve(self.board):
            self.file_manager.write_board("solved_puzzle.txt", self.board)
            self.message = self.get_text("solved")
        else:
            self.message = self.get_text("cannot_solve")

    def give_hint(self):
        if self.hints_left <= 0:
            self.message = self.get_text("no_hints")
            return

        board_copy = self.board.make_copy()

        if not self.solver.solve(board_copy):
            self.message = self.get_text("no_hint")
            return

        empty_cells = []

        for row in range(9):
            for column in range(9):
                if self.board.get_cell(row, column) == 0:
                    empty_cells.append((row, column))

        if len(empty_cells) == 0:
            self.message = self.get_text("already_done")
            return

        random_cell = random.choice(empty_cells)

        row = random_cell[0]
        column = random_cell[1]
        value = board_copy.get_cell(row, column)

        self.board.set_cell(row, column, value)
        self.hints_left -= 1
        self.message = self.get_text("hint_used") + str(self.hints_left)

    def save_game(self):
        self.file_manager.write_board("saved_puzzle.txt", self.board)
        self.message = self.get_text("saved")

    def load_game(self):
        if not os.path.exists("saved_puzzle.txt"):
            self.message = self.get_text("no_save")
            return

        grid = self.file_manager.read_board("saved_puzzle.txt")
        self.board = SudokuBoard(grid)
        self.start_grid = grid
        self.selected = None
        self.hovered = None
        self.message = self.get_text("loaded")

    def reset_game(self):
        grid = self.create_random_grid()
        self.board = SudokuBoard(grid)
        self.start_grid = grid
        self.selected = None
        self.hovered = None
        self.hints_left = 3
        self.message = self.get_text("new_game")

    def draw(self):
        if self.state == "menu":
            self.ui.draw_menu(
                self.menu_buttons,
                self.get_texts(),
                self.language
            )

        elif self.state == "settings":
            pulse = math.sin(self.pulse_time) * 6

            self.ui.draw_settings(
                self.settings_buttons,
                self.languages,
                self.language,
                self.get_texts(),
                self.polish_flags,
                pulse
            )

        elif self.state == "about":
            self.ui.draw_about(
                self.about_buttons,
                self.get_texts()
            )

        elif self.state == "game":
            self.ui.draw_game(
                self.board,
                self.game_buttons,
                self.message,
                self.selected,
                self.hovered,
                self.game_alpha
            )