class Game:
    def __init__(self, player_1_id, player_2_id, game_id):
        self.ROW_NUMBER = 6
        self.COLUMN_NUMBER = 7
        self.board = [[0 for j in range(self.COLUMN_NUMBER)] for i in range(self.ROW_NUMBER)]
        self.game_over = False
        self.turn = player_1_id
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.game_id = game_id

    def is_valid_move(self, col):
        if col < 0:
            return False
        if col > self.COLUMN_NUMBER - 1:
            return False
        return self.board[self.ROW_NUMBER - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_NUMBER):
            if self.board[r][col] == 0:
                return r

    def drop_chip(self, row, col, chip):
        self.board[row][col] = chip

    def winning_move(self, chip) -> bool:
        # Вертикали
        for c in range(self.COLUMN_NUMBER):
            for r in range(self.ROW_NUMBER - 3):
                if self.board[r][c] == chip and self.board[r + 1][c] == chip and self.board[r + 2][c] == chip and \
                        self.board[r + 3][c] == chip:
                    return True

        # Горизонтали
        for c in range(self.COLUMN_NUMBER - 3):
            for r in range(self.ROW_NUMBER):
                if self.board[r][c] == chip and self.board[r][c + 1] == chip and self.board[r][c + 2] == chip and \
                        self.board[r][c + 3] == chip:
                    return True

        # Главные диагонали
        for c in range(self.COLUMN_NUMBER - 3):
            for r in range(self.ROW_NUMBER - 3):
                if self.board[r][c] == chip and self.board[r + 1][c + 1] == chip and \
                        self.board[r + 2][c + 2] == chip and self.board[r + 3][c + 3] == chip:
                    return True

        # Побочные диагонали
        for c in range(self.COLUMN_NUMBER - 3):
            for r in range(3, self.ROW_NUMBER):
                if self.board[r][c] == chip and self.board[r - 1][c + 1] == chip and \
                        self.board[r - 2][c + 2] == chip and self.board[r - 3][c + 3] == chip:
                    return True

    def get_board(self):
        b = ""
        for r in range(self.ROW_NUMBER - 1, -1, -1):
            for c in range(self.COLUMN_NUMBER):
                b += str(self.board[r][c])
                b += " "
            b += "\n"
        return b

    def make_a_move(self, wanted_column, player_id):
        if player_id != self.turn:
            return 'Сейчас ход соперника...'

        if self.is_valid_move(wanted_column):
            row = self.get_next_open_row(wanted_column)
            chip = 0
            if self.turn == self.player_1_id:
                chip = 1
                self.turn = self.player_2_id
            else:
                chip = 2
                self.turn = self.player_1_id
            self.drop_chip(row, wanted_column, chip)
            ans = "Сделан ход\n\n"
            ans += self.get_board()
            if self.winning_move(chip):
                ans += f"\n\nИгрок {chip} победил!"
                self.game_over = True
            return ans
        else:
            return 'Невозможный ход. Попробуйте другой.'
