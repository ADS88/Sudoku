from random import choice, randint
import time
from tkinter import *



def solve(board, grid_boxes):
    if is_solution(board):
        return board
    row, col = get_first_unfilled_square(board)
    possible_solutions = get_valid_numbers(board, row, col)
    if possible_solutions:
        grid_boxes[row][col].config(fg="Green")
        for number in possible_solutions:
            time.sleep(0.0001)
            grid_boxes[row][col].set(number)
            board[row][col] = number
            solved = solve(board, grid_boxes)
            if is_solution(solved):
                return solved

    board[row][col] = 0
    grid_boxes[row][col].config(fg="Red")
    time.sleep(0.0001)
    return board


def get_valid_numbers(board, row, col):
    """Returns a set of possible numbers that could be inserted in a grid cell"""
    valid_in_row_set = get_valid_numbers_in_row(board, row, col)
    valid_in_col_set = get_valid_in_column(board, row, col)
    valid_in_square_set = get_valid_in_square(board, row, col)
    return valid_in_col_set & valid_in_row_set & valid_in_square_set


def get_valid_numbers_in_row(board, row, col):
    """Returns a set of numbers valid in box given the sudoku row constraints"""
    valid_numbers = {1,2,3,4,5,6,7,8,9}
    for index, item in enumerate(board[row]):
        if index == col:
            continue
        elif item in valid_numbers:
            valid_numbers.remove(item)
    return valid_numbers


def get_valid_in_column(board, row, col):
    """Returns a set of numbers valid in the column given sudoku constraints"""
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    for row_index, _ in enumerate(board):
        if row_index == row:
            continue
        square = board[row_index][col]
        if square in valid_numbers:
            valid_numbers.remove(square)
    return valid_numbers


def get_valid_in_square(board, row, col):
    """Returns a set of numbers valid in the square given sudoku constraints"""
    valid_numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    start_x = (col // 3) * 3
    start_y = (row // 3) * 3
    for y in range(start_y, start_y + 3):
        for x in range(start_x, start_x + 3):
            square_value = board[y][x]
            if y == row and x == col:
                continue
            elif square_value in valid_numbers:
                valid_numbers.remove(square_value)
    return valid_numbers


def is_solution(board):
    """Checks if the board is competely filled with non zero numbers"""
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] not in get_valid_numbers(board, row, col):
                return False
    return True


def get_first_unfilled_square(board):
    """Gets the first square in the board that has a value of zero"""
    for row_index, row in enumerate(board):
        for col_index, _ in enumerate(row):
            if board[row_index][col_index] == 0:
                return row_index, col_index


def generate_new_board():
    """Randomly generates a seed for a board, then solves the board and removes
    numbers until more than one solution can be reached"""
    new_board = [[0] * 9 for i in range(9)]
    possible_numbers = [1,2,3,4,5,6,7,8,9]
    row = randint(0,8)
    for col in range(len(new_board[row])):
        value = choice(possible_numbers)
        possible_numbers.remove(value)
        new_board[row][col] = value

    new_board = solve(new_board)

    for row in range(9):
        num_squares_to_delete = randint(7,9)
        for i in range(num_squares_to_delete):
            col = randint(0,8)
            new_board[row][col] = 0

    return new_board

