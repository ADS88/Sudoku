import tkinter as tk
import threading
from SudokuSolve import *
import copy


class MainApplication():
    def __init__(self, window):
        self.window = window
        self.grid_boxes_gui = []
        self.buttons = []
        self.feedback_label = None
        self.setup_gui()
        self.grid_boxes_values = [[1, 0, 0, 0, 7, 0, 3, 0, 0],
                                  [0, 8, 0, 0, 2, 0, 7, 0, 0],
                                  [3, 0, 0, 0, 8, 9, 0, 0, 4],
                                  [8, 4, 0, 0, 0, 1, 9, 0, 3],
                                  [0, 0, 3, 7, 0, 8, 5, 0, 0],
                                  [9, 0, 1, 2, 0, 0, 0, 7, 8],
                                  [7, 0, 0, 3, 5, 0, 0, 0, 9],
                                  [0, 0, 9, 0,4 ,0 ,0 ,5 ,0],
                                  [0, 0, 4, 0, 1, 0, 0, 0, 2]]
        self.set_grid_gui_from_values(self.grid_boxes_values)

    def setup_gui(self):
        """Creates buttons and labels used in the GUI"""
        self.window.title("Sudoku")
        self.set_dimensions()
        self.create_grid_gui()
        self.create_buttons()
        self.feedback_label = tk.Label(self.window, text="")
        self.feedback_label.grid(column=3, row=12, columnspan=2)

    def set_dimensions(self):
        self.window.geometry('690x550')
        self.window.columnconfigure(0, minsize=20)
        self.window.rowconfigure(0, minsize=20)
        self.window.rowconfigure(10, minsize=20)

    def create_buttons(self):
        """Creates the reset, new, solve and check buttons and binds their click events to methods"""
        reset_board_button = tk.Button(self.window, text="Reset Board", command=self.set_grid_gui_from_values, font=('Ubuntu', 12))
        new_board_button = tk.Button(self.window, text="New Board", command=self.new_board, font=('Ubuntu', 12))
        check_solution_button = tk.Button(self.window, text="Check Solution", command=self.check_solution, font=('Ubuntu', 12))
        solve_board_button = tk.Button(self.window, text="Solve Board", command=self.solve_board, font=('Ubuntu', 12))
        new_board_button.grid(column=1, row=11, columnspan=2)
        check_solution_button.grid(column=3, row=11, columnspan=2)
        reset_board_button.grid(column=5, row=11, columnspan=2)
        solve_board_button.grid(column=7, row=11, columnspan=2)
        self.buttons = [solve_board_button, check_solution_button, new_board_button, reset_board_button]

    def create_grid_gui(self):
        """Creates the GUI squares for the sudoku board"""
        for row in range(9):
            self.grid_boxes_gui.append([])
            for col in range(9):
                input_box = SudokuGridBox(self.window, width=3, font=('Ubuntu', 28), justify='center')
                input_box.configure(highlightbackground="red", highlightcolor="red")
                pady = (10, 0) if row % 3 == 0 else 0
                padx = (10, 0) if col % 3 == 0 else 0
                input_box.grid(column=col + 1, row=row + 1, padx=padx, pady=pady)
                self.grid_boxes_gui[row].append(input_box)

    def set_grid_gui_from_values(self, grid=None):
        """Sets the board to display the numbers in a sudoku grid given in nested list format,
        resets the board to what it was previously set as if grid is None"""
        if grid is None:
            grid = self.grid_boxes_values
        for row_index, row in enumerate(self.grid_boxes_gui):
            for column_index, box in enumerate(row):
                value = grid[row_index][column_index]
                if value != 0:
                    box.set(value)
                    box.config(state='readonly')
                else:
                    box.set("")
                    box.config(state="normal")
        self.reset_grid_colour()

    def get_grid_values_from_gui(self):
        """Gets a nested list representation of the current values in each of the boards squares"""
        board = []
        for index, row in enumerate(self.grid_boxes_gui):
            board.append([])
            for col in row:
                value = col.get()
                board[index].append(int(value)) if value != "" else board[index].append(0)
        return board

    def check_solution(self):
        """Checks if the current values in the gui are a valid solution using the rules of sudoku and displays the result
        to the user"""
        board = self.get_grid_values_from_gui()
        if is_solution(board):
            self.feedback_label.config(text="Correct solution", fg="Green")
        else:
            self.feedback_label.config(text="Incorrect solution", fg="Red")

    def solve_board(self):
        """Solves the current board and updates the gui to display the solution"""
        self.toggle_buttons(False)
        self.set_grid_gui_from_values()
        board = copy.deepcopy(self.grid_boxes_values)
        solve_thread = threading.Thread(target=solve, args=(board, self), daemon=True)
        solve_thread.start()
        # solve_thread.join()

    def new_board(self):
        """Generates a new list of values to fill the grid squares and sets the GUI to this new list"""
        self.grid_boxes_values = generate_new_board()
        self.set_grid_gui_from_values(self.grid_boxes_values)
        self.reset_grid_colour()

    def update_single_grid_gui_square(self, row, col, colour, value=None):
        """Updates the colour and value of a single square in the grid GUI"""
        self.grid_boxes_gui[row][col].config(fg=colour)
        if value is not None:
            if value == 0:
                value = ""
            self.grid_boxes_gui[row][col].set(value)

    def reset_grid_colour(self):
        """Sets all squares to be coloured black"""
        for row in self.grid_boxes_gui:
            for col in row:
                col.config(fg="black")

    def toggle_buttons(self, clickable):
        """Toggles if the buttons in the UI are clickable or not"""
        for button in self.buttons:
            button.config(state=tk.NORMAL if clickable else tk.DISABLED)


class SudokuGridBox(tk.Entry):
    def __init__(self, master=None, **kwargs):
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.old_value = ''
        self.var.trace('w', self.validate_input)
        self.get, self.set = self.var.get, self.var.set

    def validate_input(self, *args):
        """Ensures input to a grid box is a number from 1-9"""
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









