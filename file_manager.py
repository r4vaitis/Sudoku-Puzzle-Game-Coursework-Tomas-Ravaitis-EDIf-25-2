class FileManager:
    def read_board(self, file_name):
        grid = []

        file = open(file_name, "r", encoding="utf-8")

        for line in file:
            numbers = line.split()
            row = []

            for number in numbers:
                row.append(int(number))

            grid.append(row)

        file.close()
        return grid

    def write_board(self, file_name, board):
        grid = board.get_grid()
        file = open(file_name, "w", encoding="utf-8")

        for row in grid:
            text_row = ""

            for number in row:
                text_row += str(number) + " "

            file.write(text_row.strip() + "\n")

        file.close()