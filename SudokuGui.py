from tkinter import *
from SudokuSolve import *
import copy


class MainApplication():
    def __init__(self, window):
        self.window = window
        self.grid_boxes = []
        self.setup_gui()
        self.current_board = [[1,0,0,0,7,0,3,0,0],
                 [0,8,0,0,2,0,7,0,0],
                 [3,0,0,0,8,9,0,0,4],
                 [8,4,0,0,0,1,9,0,3],
                 [0,0,3,7,0,8,5,0,0],
                 [9,0,1,2,0,0,0,7,8],
                 [7,0,0,3,5,0,0,0,9],
                 [0,0,9,0,4,0,0,5,0],
                 [0,0,4,0,1,0,0,0,2]]
        self.set_board(self.current_board)

    def setup_gui(self):
        """Creates buttons and labels used in the GUI"""
        self.window.title("Sudoku")
        self.window.geometry('640x500')
        self.create_board()
        reset_board_button = Button(self.window, text="Reset Board", command=self.set_board)
        new_board_button = Button(self.window, text="New Board", command=self.new_board)
        check_solution_button = Button(self.window, text="Check solution", command=self.check_solution)
        solve_board_button = Button(self.window, text="Solve Board", command=self.solve_board)
        self.feedback_label = Label(self.window, text="")
        self.window.columnconfigure(0, minsize=20)
        self.window.rowconfigure(0, minsize=20)
        self.window.rowconfigure(10, minsize=20)
        new_board_button.grid(column=1, row=11, columnspan=2)
        check_solution_button.grid(column=3, row=11, columnspan=2)
        reset_board_button.grid(column=5, row=11, columnspan=2)
        solve_board_button.grid(column=7, row=11, columnspan=2)
        self.feedback_label.grid(column=3, row=12, columnspan=2)

    def create_board(self):
        """Creates the GUI for the board"""
        for row in range(9):
            self.grid_boxes.append([])
            for col in range(9):
                input_box = SudokuGridBox(self.window, width=3, font=('Ubuntu', 28))
                input_box.configure(highlightbackground="red", highlightcolor="red")
                input_box.grid(column=col+1, row=row+1)
                self.grid_boxes[row].append(input_box)

    def set_board(self, grid=None):
        if not grid:
            grid = self.current_board
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
                        box.config(state="normal")
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


    def check_solution(self):
        board = self.get_board_as_list()
        if is_solution(board):
            self.feedback_label.config(text="Correct solution")
        else:
            self.feedback_label.config(text="Incorrect solution")


    def solve_board(self):
        """Solves the board and displays the solution"""
        board = copy.deepcopy(self.current_board)
        solved_board = solve(board, self.window, self.grid_boxes)
        # self.set_board(solved_board)

    def new_board(self):
        self.current_board = generate_new_board()
        self.set_board(self.current_board)

    def insert_into_grid(self, value, row, col):
        self.grid_boxes[row][col].set(value)


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


if __name__ == "__main__":
    window = tk.Tk()
    MainApplication(window)
    window.mainloop()









