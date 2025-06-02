# Task 6

class TictactoeException(Exception):
    """Custom exception for Tic-Tac-Toe errors."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    """Represents the Tic-Tac-Toe board."""
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [[" " for column_index in range(3)] for row_index in range(3)]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        """Returns a string representation of the board."""
        board_lines = []
        board_lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        board_lines.append("-----------\n")
        board_lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        board_lines.append("-----------\n")
        board_lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(board_lines)

    def move(self, move_string):
        """Handles a player's move."""
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3  # row
        column = move_index % 3  # column

        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][column] = self.turn
        self.last_move = move_string

        self.turn = "O" if self.turn == "X" else "X"

    def whats_next(self):
        """Checks the game state: win, draw, or next move."""
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                else:
                    continue
                break
            else:
                continue
            break
        if (cat):
            return (True, "Cat's Game.")
        win = False
        for i in range(3):  # check rows
            if self.board_array[i][0] != " ":
                if self.board_array[i][0] == self.board_array[i][1] and self.board_array[i][1] == self.board_array[i][
                    2]:
                    win = True
                    break
        if not win:
            for i in range(3):  # check columns
                if self.board_array[0][i] != " ":
                    if self.board_array[0][i] == self.board_array[1][i] and self.board_array[1][i] == \
                            self.board_array[2][i]:
                        win = True
                        break
        if not win:
            if self.board_array[1][1] != " ":  # check diagonals
                if self.board_array[0][0] == self.board_array[1][1] and self.board_array[2][2] == self.board_array[1][
                    1]:
                    win = True
                if self.board_array[0][2] == self.board_array[1][1] and self.board_array[2][0] == self.board_array[1][
                    1]:
                    win = True
        if not win:
            if self.turn == "X":
                return (False, "X's turn.")
            else:
                return (False, "O's turn.")
        else:
            if self.turn == "O":
                return (True, "X wins!")
            else:
                return (True, "O wins!")


# Game logic
if __name__ == "__main__":
    board = Board()
    print("Welcome to Tic-Tac-Toe!")

    while True:
        print(board)
        print(f"\n-> {board.turn}'s move.")
        move = input("Enter your move (e.g., 'upper left'): ").strip().lower()

        try:
            board.move(move)
        except TictactoeException as e:
            print(f"Error: {e.message}")
            continue

        print("\n" + str(board))

        done, msg = board.whats_next()
        if done:
            print(f"\nGame Over: {msg}")
            break