class SudokuSolver:

    @staticmethod
    def solve(board):
        if SudokuSolver.is_solution(board):
            return board
        row, col = SudokuSolver.get_first_unfilled_square(board)
        possible_solutions = SudokuSolver.get_valid_numbers(board, row, col)
        if possible_solutions:
            for number in possible_solutions:
                board[row][col] = number
                solved = SudokuSolver.solve(board)
                if SudokuSolver.is_solution(solved):
                    return solved

        board[row][col] = 0
        return board

    @staticmethod
    def get_valid_numbers(board, row, col):
        """Returns a set of possible numbers that could be inserted in a grid cell"""
        valid_in_row_set = SudokuSolver.get_valid_numbers_in_row(board, row)
        valid_in_col_set = SudokuSolver.get_valid_in_column(board, col)
        valid_in_square_set = SudokuSolver.get_valid_in_square(board, row, col)
        return valid_in_col_set & valid_in_row_set & valid_in_square_set

    @staticmethod
    def get_valid_numbers_in_row(board, row):
        """Returns a set of numbers valid in the row given sudoku constraints"""
        valid_numbers = {1,2,3,4,5,6,7,8,9}
        for item in board[row]:
            if item in valid_numbers:
                valid_numbers.remove(item)
        return valid_numbers

    @staticmethod
    def get_valid_in_column(board, col):
        """Returns a set of numbers valid in the column given sudoku constraints"""
        valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for row_index, _ in enumerate(board):
            square = board[row_index][col]
            if square in valid_numbers:
                valid_numbers.remove(square)
        return valid_numbers

    @staticmethod
    def get_valid_in_square(board, row, col):
        """Returns a set of numbers valid in the square given sudoku constraints"""
        valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        start_x = (col // 3) * 3
        start_y = (row // 3) * 3
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                square_value = board[y][x]
                if square_value in valid_numbers:
                    valid_numbers.remove(square_value)
        return valid_numbers

    @staticmethod
    def is_solution(board):
        """Checks if the board is competely filled with non zero numbers"""
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    return False
        return True

    @staticmethod
    def get_first_unfilled_square(board):
        """Gets the first square in the board that has a value of zero"""
        for row_index, row in enumerate(board):
            for col_index, _ in enumerate(row):
                if board[row_index][col_index] == 0:
                    return row_index, col_index

    def check_board_validity(self, board):
        pass

