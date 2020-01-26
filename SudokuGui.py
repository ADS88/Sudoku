from tkinter import *
from SudokuSolve import *


class SudokuGrid():
    def __init__(self, default_board):
        self.window = Tk()
        self.grid_boxes = []
        self.setup_gui()
        self.set_board(default_board)
        self.window.mainloop()

    def setup_gui(self):
        """Creates buttons and labels used in the GUI"""
        self.window.title("Sudoku")
        self.window.geometry('800x600')
        self.create_board()
        random_game_button = Button(self.window, text="Random Game", command=self.set_board)
        solve_board_button = Button(self.window, text="Solve Board", command=self.solve_board)
        feedback_label = Label(self.window, text="Welcome to my cool sudoku game")
        random_game_button.grid(column=0, row=14, columnspan=4)
        solve_board_button.grid(column=5, row=14, columnspan=4)
        feedback_label.grid(column=0, row=15, columnspan=4)


    def create_board(self):
        """Creates the GUI for the board"""
        for row in range(9):
            self.grid_boxes.append([])
            for col in range(9):
                input_box = SudokuGridBox(self.window, width=3, font=('Ubuntu', 28))
                input_box.configure(highlightbackground="red", highlightcolor="red")
                input_box.grid(column=col, row=row)
                self.grid_boxes[row].append(input_box)

    def set_board(self, grid=None):
        """Sets the board to display the numbers in a sudoku grid, resets the board if grid is None"""
        for row_index, row in enumerate(self.grid_boxes):
            for column_index, box in enumerate(row):
                if grid:
                    value = grid[row_index][column_index]
                    if value != 0:
                        box.set(value)
                        box.config(state='readonly')
                    else:
                        box.set("")
                else:
                    box.set("")
                    box.config(state="normal")

    def get_board_as_list(self):
        """Gets a list representation of the current stat of the board"""
        board = []
        for index, row in enumerate(self.grid_boxes):
            board.append([])
            for col in row:
                value = col.get()
                board[index].append(int(value)) if value != "" else board[index].append(0)
        return board

    def solve_board(self):
        """Solves the board and displays the solution"""
        board = self.get_board_as_list()
        solved_board = SudokuSolver.solve(board)
        self.set_board(solved_board)


class SudokuGridBox(Entry):
    def __init__(self, master=None, **kwargs):
        self.var = StringVar()
        Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.validate_input)
        self.get, self.set = self.var.get, self.var.set

    def validate_input(self, *args):
        """Ensures input to a grid box is a number from 1-9 and a there is a possible solution with that input"""
        value = self.get()
        if not value:
            self.set("")

        elif value.isdigit() and len(value) < 2 and value != "0":
            # the current value is only digits; allow this
            self.old_value = self.get()
        else:
            self.set(self.old_value)



default_board = [[1,0,0,0,7,0,3,0,0],
                 [0,8,0,0,2,0,7,0,0],
                 [3,0,0,0,8,9,0,0,4],
                 [8,4,0,0,0,1,9,0,3],
                 [0,0,3,7,0,8,5,0,0],
                 [9,0,1,2,0,0,0,7,8],
                 [7,0,0,3,5,0,0,0,9],
                 [0,0,9,0,4,0,0,5,0],
                 [0,0,4,0,1,0,0,0,2]]

sudoko_grid = SudokuGrid(default_board)







