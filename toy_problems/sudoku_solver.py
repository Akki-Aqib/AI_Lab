"""
Sudoku Solver - Backtracking Algorithm
Solves any valid 9x9 Sudoku puzzle
"""

def print_board(board):
    print("+-------+-------+-------+")
    for i, row in enumerate(board):
        if i in (3, 6):
            print("+-------+-------+-------+")
        line = "| "
        for j, val in enumerate(row):
            line += (str(val) if val != 0 else '.') + " "
            if j in (2, 5):
                line += "| "
        print(line + "|")
    print("+-------+-------+-------+")

def is_valid(board, row, col, num):
    # Check row
    if num in board[row]:
        return False
    # Check column
    if num in [board[r][col] for r in range(9)]:
        return False
    # Check 3x3 box
    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if board[r][c] == num:
                return False
    return True

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def solve(board):
    empty = find_empty(board)
    if not empty:
        return True  # Solved!
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0  # Backtrack
    return False

if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    print("=== Sudoku Solver (Backtracking) ===")
    print("\nUnsolved Puzzle:")
    print_board(puzzle)

    if solve(puzzle):
        print("\nSolved Puzzle:")
        print_board(puzzle)
    else:
        print("No solution exists.")
