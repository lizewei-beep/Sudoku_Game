import random
import copy
import concurrent.futures
import tkinter as tk

# 生成一个完整的数独网格
def generate_sudoku():
    base = 3
    side = base * base

    # 定义一个函数来决定每个格子的数字
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # 定义一个函数来打乱数组
    def shuffle(s): return random.sample(s, len(s))

    # 生成一个随机数组
    nums = shuffle(range(1, side + 1))

    # 使用shuffle和pattern函数生成一个已解决的数独板
    board = [[nums[pattern(r, c)] for c in range(side)] for r in range(side)]

    rows = [r for g in shuffle(range(base)) for r in shuffle(range(g * base, (g + 1) * base))]
    cols = [c for g in shuffle(range(base)) for c in shuffle(range(g * base, (g + 1) * base))]

    # 打乱行和列
    board = [[board[r][c] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 6

    # 将一部分格子设为空
    for p in map(lambda x: (x // side, x % side), random.sample(range(squares), empties)):
        board[p[0]][p[1]] = 0

    return board


# 解决一个数独网格
    def solve_sudoku(board):
        # 检查一个数字是否可以被放在一个特定的位置
        def is_valid(board, row, col, num):
            for x in range(9):
                if board[row][x] == num:
                    return False
                if board[x][col] == num:
                    return False

            # 检查3x3的网格
            start_row, start_col = row - row % 3, col - col % 3
            for i in range(3):
                for j in range(3):
                    if board[i + start_row][j + start_col] == num:
                        return False
            return True

    # 使用回溯算法解决数独
    def solve(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve(board):
                                return True
                            else:
                                board[i][j] = 0
                    return False
        return True

    # 如果无法解决，则输出"No solution exists"
    if not solve(board):
        print("No solution exists")
    else:
        return board


# 并发生成和解决数独网格
def concurrent_sudoku():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for _ in range(9):
            sudoku = generate_sudoku()
            solver = copy.deepcopy(sudoku)
            executor.submit(solve_sudoku, solver)


class SudokuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")

        # 存放所有待解决和已解决的数独
        self.sudokus_to_solve = []
        self.solved_sudokus = []

        # 当前显示的数独的索引
        self.current_index = 0

        # 创建按钮
        generate_button = tk.Button(self, text="生成数独及答案", command=self.generate)
        generate_button.pack(side="top")

        prev_button = tk.Button(self, text="上一个数独", command=self.prev_sudoku)
        prev_button.pack(side="left")

        next_button = tk.Button(self, text="下一个数独", command=self.next_sudoku)
        next_button.pack(side="right")

        show_solution_button = tk.Button(self, text="显示答案", command=self.show_solution)
        show_solution_button.pack(side="bottom")

        # 创建一个容器来包含数独
        self.sudoku_frame = tk.Frame(self)
        self.sudoku_frame.pack(side="top")

    # 将数独显示在GUI上
    def create_sudoku_frame(self, sudoku):
        for widget in self.sudoku_frame.winfo_children():
            widget.destroy()

        for i in range(9):
            for j in range(9):
                cell = tk.Label(self.sudoku_frame, text=sudoku[i][j] if sudoku[i][j] != 0 else " ",
                                width=2, height=1, font=("Helvetica", 20), relief="solid")
                cell.grid(row=i, column=j)

    # 生成新的数独
    def generate(self):
        self.sudokus_to_solve = [generate_sudoku() for _ in range(9)]
        self.solved_sudokus = [solve_sudoku(copy.deepcopy(sudoku)) for sudoku in self.sudokus_to_solve]
        self.current_index = 0
        self.create_sudoku_frame(self.sudokus_to_solve[self.current_index])

    # 显示前一个数独
    def prev_sudoku(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.create_sudoku_frame(self.sudokus_to_solve[self.current_index])

    # 显示下一个数独
    def next_sudoku(self):
        if self.current_index < len(self.sudokus_to_solve) - 1:
            self.current_index += 1
            self.create_sudoku_frame(self.sudokus_to_solve[self.current_index])

    # 显示答案
    def show_solution(self):
        if self.solved_sudokus:
            self.create_sudoku_frame(self.solved_sudokus[self.current_index])


if __name__ == "__main__":
    gui = SudokuGUI()
    gui.mainloop()
