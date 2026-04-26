import pygame


class SudokuUI:
    def __init__(self, screen, width, height, cell_size, board_y):
        self.screen = screen
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.board_y = board_y
        self.board_size = 540

        self.white = (250, 251, 253)
        self.black = (40, 55, 80)
        self.gray = (232, 236, 242)
        self.line_light = (190, 200, 214)
        self.line_dark = (70, 95, 130)

        self.fixed_number = (55, 75, 105)
        self.user_number = (45, 100, 190)

        self.row_column_color = (120, 170, 230, 60)
        self.box_color = (120, 220, 140, 70)
        self.active_cell_color = (100, 170, 255, 120)

        self.button_color = (230, 235, 243)
        self.button_border = (90, 110, 140)
        self.button_text = (45, 60, 85)
        self.selected_button = (195, 225, 205)

        self.message_color = (180, 60, 60)

        self.title_font = pygame.font.SysFont("arial", 46)
        self.big_font = pygame.font.SysFont("arial", 34)
        self.font = pygame.font.SysFont("arial", 34)
        self.button_font = pygame.font.SysFont("arial", 19)
        self.message_font = pygame.font.SysFont("arial", 20)
        self.small_font = pygame.font.SysFont("arial", 18)

    def draw_menu(self, buttons, texts, language):
        self.screen.fill(self.white)

        title = self.title_font.render("Sudoku Game", True, self.black)
        title_rect = title.get_rect(center=(self.width // 2, 135))
        self.screen.blit(title, title_rect)

        subtitle = self.small_font.render(
            "Python Pygame Coursework",
            True,
            self.line_dark
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, 180))
        self.screen.blit(subtitle, subtitle_rect)

        self.draw_button(buttons["play"], texts["play"])
        self.draw_button(buttons["settings"], texts["settings"])
        self.draw_button(buttons["about"], texts["about"])

        lang_text = self.small_font.render(
            "Language: " + language,
            True,
            self.line_dark
        )
        self.screen.blit(lang_text, (20, 620))

        pygame.display.flip()

    def draw_settings(self, buttons, languages, language, texts, flags, pulse):
        self.screen.fill(self.white)

        if language == "Polski":
            self.draw_polish_flags(flags, pulse)
            title_y = 135
        else:
            title_y = 90

        title = self.big_font.render(texts["settings"], True, self.black)
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        self.screen.blit(title, title_rect)

        y_text = title_y + 50
        info = self.small_font.render(texts["choose_language"], True, self.black)
        info_rect = info.get_rect(center=(self.width // 2, y_text))
        self.screen.blit(info, info_rect)

        for lang in languages:
            selected = lang == language
            self.draw_button(buttons[lang], lang, selected=selected)

        self.draw_button(buttons["back"], texts["back"])

        pygame.display.flip()

    def draw_about(self, buttons, texts):
        self.screen.fill(self.white)

        title = self.big_font.render(texts["about"], True, self.black)
        title_rect = title.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title, title_rect)

        y = 145

        for line in texts["about_lines"]:
            text = self.small_font.render(line, True, self.black)
            text_rect = text.get_rect(center=(self.width // 2, y))
            self.screen.blit(text, text_rect)
            y += 32

        self.draw_button(buttons["back"], texts["back"])

        pygame.display.flip()

    def draw_game(self, board, buttons, message, selected, hovered, alpha):
        self.screen.fill(self.white)

        self.draw_base_cells(board)

        active_cell = hovered

        if active_cell is None:
            active_cell = selected

        if active_cell is not None:
            self.draw_row_and_column(active_cell)
            self.draw_box(active_cell)
            self.draw_active_cell(active_cell)

        self.draw_grid()
        self.draw_numbers(board, alpha)
        self.draw_game_buttons(buttons, alpha)
        self.draw_message(message)

        pygame.display.flip()

    def draw_polish_flags(self, flags, pulse):
        for flag in flags:
            width = flag["width"]
            height = flag["height"]
            alpha = flag["alpha"]

            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            pygame.draw.rect(
                surface,
                (255, 255, 255, alpha),
                (0, 0, width, height // 2)
            )

            pygame.draw.rect(
                surface,
                (220, 0, 0, alpha),
                (0, height // 2, width, height // 2)
            )

            self.screen.blit(surface, (flag["x"], flag["y"]))

        size = int(34 + pulse)
        font = pygame.font.SysFont("arial", size, bold=True)
        text = font.render("Polska Gurom", True, (210, 30, 30))
        text_rect = text.get_rect(center=(self.width // 2, 55))
        self.screen.blit(text, text_rect)

    def draw_base_cells(self, board):
        for row in range(9):
            for column in range(9):
                x = column * self.cell_size
                y = self.board_y + row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if board.is_fixed(row, column):
                    pygame.draw.rect(self.screen, self.gray, rect)
                else:
                    pygame.draw.rect(self.screen, self.white, rect)

    def draw_row_and_column(self, cell):
        row = cell[0]
        column = cell[1]

        row_rect = pygame.Rect(
            0,
            self.board_y + row * self.cell_size,
            self.board_size,
            self.cell_size
        )

        column_rect = pygame.Rect(
            column * self.cell_size,
            self.board_y,
            self.cell_size,
            self.board_size
        )

        self.draw_transparent_rect(row_rect, self.row_column_color)
        self.draw_transparent_rect(column_rect, self.row_column_color)

    def draw_box(self, cell):
        row = cell[0]
        column = cell[1]

        start_row = row // 3 * 3
        start_column = column // 3 * 3

        rect = pygame.Rect(
            start_column * self.cell_size,
            self.board_y + start_row * self.cell_size,
            self.cell_size * 3,
            self.cell_size * 3
        )

        self.draw_transparent_rect(rect, self.box_color)
        pygame.draw.rect(self.screen, (90, 170, 110), rect, 2)

    def draw_active_cell(self, cell):
        row = cell[0]
        column = cell[1]

        rect = pygame.Rect(
            column * self.cell_size,
            self.board_y + row * self.cell_size,
            self.cell_size,
            self.cell_size
        )

        self.draw_transparent_rect(rect, self.active_cell_color)
        pygame.draw.rect(self.screen, (70, 130, 220), rect, 2)

    def draw_transparent_rect(self, rect, color):
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surface.fill(color)
        self.screen.blit(surface, (rect.x, rect.y))

    def draw_grid(self):
        for i in range(10):
            if i % 3 == 0:
                line_width = 3
                color = self.line_dark
            else:
                line_width = 1
                color = self.line_light

            pygame.draw.line(
                self.screen,
                color,
                (i * self.cell_size, self.board_y),
                (i * self.cell_size, self.board_y + self.board_size),
                line_width
            )

            pygame.draw.line(
                self.screen,
                color,
                (0, self.board_y + i * self.cell_size),
                (self.board_size, self.board_y + i * self.cell_size),
                line_width
            )

    def draw_numbers(self, board, alpha):
        for row in range(9):
            for column in range(9):
                number = board.get_cell(row, column)

                if number != 0:
                    if board.is_fixed(row, column):
                        color = self.fixed_number
                    else:
                        color = self.user_number

                    text = self.font.render(str(number), True, color)
                    text.set_alpha(alpha)

                    x = column * self.cell_size + self.cell_size // 2
                    y = self.board_y + row * self.cell_size
                    y += self.cell_size // 2

                    text_rect = text.get_rect(center=(x, y))
                    self.screen.blit(text, text_rect)

    def draw_game_buttons(self, buttons, alpha):
        self.draw_button(buttons["solve"], "Solve", alpha)
        self.draw_button(buttons["hint"], "Hint", alpha)
        self.draw_button(buttons["save"], "Save", alpha)
        self.draw_button(buttons["load"], "Load", alpha)
        self.draw_button(buttons["reset"], "Reset", alpha)

    def draw_button(self, rect, text, alpha=255, selected=False):
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        if selected:
            color = self.selected_button
        else:
            color = self.button_color

        pygame.draw.rect(
            surface,
            (color[0], color[1], color[2], alpha),
            (0, 0, rect.width, rect.height),
            border_radius=8
        )

        pygame.draw.rect(
            surface,
            (
                self.button_border[0],
                self.button_border[1],
                self.button_border[2],
                alpha
            ),
            (0, 0, rect.width, rect.height),
            2,
            border_radius=8
        )

        self.screen.blit(surface, (rect.x, rect.y))

        button_text = self.button_font.render(text, True, self.button_text)
        button_text.set_alpha(alpha)
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)

    def draw_message(self, message):
        text = self.message_font.render(message, True, self.message_color)
        text_rect = text.get_rect(center=(self.width // 2, 645))
        self.screen.blit(text, text_rect)