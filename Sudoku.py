import copy
import random
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, messagebox

def is_valid(board, row, col, num):  #检查数字在该位置是否有效
    for x in range(9):
        if board[row][x] == num:
            return False

    for y in range(9):
        if board[y][col] == num:
            return False

    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def solve(board, row=0, col=0):# 解决数独问题
    if row == 9:
        row = 0
        if col + 1 == 9:
            return True
        else:
            col += 1

    if board[row][col] != 0:
        return solve(board, row + 1, col)

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board, row + 1, col):
                return True
        board[row][col] = 0
    return False


def generate_sudoku(difficulty):# 生成数独问题
    board = [[0] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            board[i][j] = (i * 3 + i // 3 + j) % 9 + 1

    if difficulty == 'high':
        num_of_blanks = random.randint(40, 45)
    else:
        num_of_blanks = random.randint(25, 30)

    for _ in range(num_of_blanks):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return "\n".join(" ".join(str(val) for val in row) for row in board)


class SudokuGUI:
    def __init__(self):
        self.root = tk.Tk() # 创建根窗口
        self.root.title("数独生成器") # 设置标题

        # 创建用于显示数独和解答的标签网格
        self.sudoku_cells = [[{
          "label": tk.Label(self.root, width=6, height=2),
          "value": tk.StringVar(),
        } for _ in range(12)] for _ in range(9)]

        for i in range(9):
            for j in range(12):
                cell = self.sudoku_cells[i][j]
                cell["label"].configure(textvariable=cell["value"])
                if j >= 3:  # 只有数独部分的单元格才有边框
                    cell["label"].config(borderwidth=1, relief="solid")
                cell["label"].grid(row=i+4, column=j, sticky=tk.N+tk.S+tk.E+tk.W)

        self.difficulty_label = tk.Label(self.root, text="难度 (high / low): ")
        self.difficulty_label.grid(row=4, column=0)

        self.difficulty_entry = tk.Entry(self.root)
        self.difficulty_entry.grid(row=4, column=1)

        self.generate_button = tk.Button(
            self.root,
            text="生成数独",
            command=self.generate_sudokus
        )
        self.generate_button.grid(row=5, column=0, columnspan=2)

        self.current_board = 0
        self.display_solution_button = tk.Button(
            self.root,
            text="显示答案",
            command=self.display_solution
        )
        self.display_solution_button.grid(row=6, column=0, columnspan=2)

        self.next_button = tk.Button(
            self.root,
            text="下一个",
            command=self.next_sudoku
        )
        self.next_button.grid(row=7, column=1)

        self.prev_button = tk.Button(
            self.root,
            text="上一个",
            command=self.prev_sudoku
        )
        self.prev_button.grid(row=7, column=0)

    def generate_sudokus(self): # 生成数独问题并展示第一个数独问题
        difficulty = self.difficulty_entry.get()

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(generate_sudoku, [difficulty]*9))

        self.boards = [
            [[int(num) for num in line.split()] for line in board.split('\n')]
            for board in results
        ]

        self.current_board = 0
        self.display_board()

    def clear_board(self):# 清空界面上的数独问题
        for i in range(9):
            for j in range(3, 12):
                cell = self.sudoku_cells[i][j]
                cell["value"].set(" ")
                cell["label"].configure(bg="white")

    def display_board(self):# 显示当前的数独问题
        self.clear_board()
        board = self.boards[self.current_board]

        for i in range(9):
            for j in range(9):
                cell_value = board[i][j]
                cell_text = str(cell_value) if cell_value != 0 else " "
                cell = self.sudoku_cells[i][j + 3]
                cell["value"].set(cell_text)
                if cell_value != 0:
                    cell["label"].configure(bg="lightgray")

    def next_sudoku(self):# 显示下一个数独问题
        self.current_board = (self.current_board + 1) % len(self.boards)
        self.display_board()

    def prev_sudoku(self):# 显示前一个数独问题
        self.current_board = (self.current_board - 1) % len(self.boards)
        self.display_board()

    def display_solution(self):# 显示当前数独问题的解
        board_to_solve = copy.deepcopy(self.boards[self.current_board])
        solve(board_to_solve)

        for i in range(9):
            for j in range(9):
                cell_value = board_to_solve[i][j]
                self.sudoku_cells[i][j + 3]["value"].set(str(cell_value))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = SudokuGUI()
    gui.run()
    difficulty = input("Please select a difficulty (high or low): ")
    num_batches = int(input("How many batches of Sudoku puzzles would you like to generate? "))# 生成数独问题的批次,由于显示问题该功能最终被废弃

    for batch in range(num_batches):# 生成并导出数独问题到文件，同样由于一系列问题不得不放弃文件导入本地功能
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(generate_sudoku, [difficulty] * 9))

        print(f"Batch {batch + 1}:")
        print("\n-------------------\n")

        for index, sudoku_board in enumerate(results):
            print(sudoku_board)
            print("\n" + "-" * 20 + "\n")

            with open(f"sudoku_{batch + 1}_{index}.txt", "w") as file:
                file.write(sudoku_board)




