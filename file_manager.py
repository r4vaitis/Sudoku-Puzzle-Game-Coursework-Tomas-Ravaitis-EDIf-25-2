class FileManager:
    def read_board(self, file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return [
                [int(number) for number in line.split()]
                for line in file
            ]

    def write_board(self, file_name, board):
        with open(file_name, "w", encoding="utf-8") as file:
            for row in board.get_grid():
                file.write(" ".join(str(number) for number in row) + "\n")