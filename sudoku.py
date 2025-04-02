import pycosat

class Solver:
    def __init__(self, sudoku_lists, sudoku_no):
        """Initialize Sudoku from a list of puzzles."""
        self.sudoku = sudoku_lists[sudoku_no].strip()
        self.sudoku_no = sudoku_no
        self.cnf = []
    def var(self, row, col, num):
        """Return a unique variable for (row, col, num)"""
        return (row * 81) + (col * 9) + num

    def get_row(self, pos):
        """Return all numbers in the row of the given position."""
        row, _ = pos
        return [int(self.sudoku[row * 9 + i]) for i in range(9) if self.sudoku[row * 9 + i] != '.']

    def get_coloumn(self, pos):
        """Return all numbers in the column of the given position."""
        _, col = pos
        return [int(self.sudoku[i * 9 + col]) for i in range(9) if self.sudoku[i * 9 + col] != '.']

    def get_square(self, pos):
        """Return all numbers in the 3x3 box of the given position."""
        row, col = pos
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        return [
            int(self.sudoku[(start_row + i) * 9 + (start_col + j)])
            for i in range(3) for j in range(3)
            if self.sudoku[(start_row + i) * 9 + (start_col + j)] != '.'
        ]

    def generate_cnf(self):
        """Generate CNF constraints for Sudoku rules using helper methods."""

        # Rule 1: Each cell contains at least one number
        for r in range(9):
            for c in range(9):
                self.cnf.append([self.var(r, c, n) for n in range(1, 10)])

        # Each cell contains at most one number
        for r in range(9):
            for c in range(9):
                for n1 in range(1, 10):
                    for n2 in range(n1 + 1, 10):
                        self.cnf.append([-self.var(r, c, n1), -self.var(r, c, n2)])

        # Use get_row() to enforce unique numbers per row
        for r in range(9):
            for n in range(1, 10):
                if n not in self.get_row((r, 0)):  # If `n` is not already present
                    self.cnf.append([self.var(r, c, n) for c in range(9)])
                    for c1 in range(9):
                        for c2 in range(c1 + 1, 9):
                            self.cnf.append([-self.var(r, c1, n), -self.var(r, c2, n)])

        # Use get_coloumn() to enforce unique numbers per column
        for c in range(9):
            for n in range(1, 10):
                if n not in self.get_coloumn((0, c)):  # If `n` is not already present
                    self.cnf.append([self.var(r, c, n) for r in range(9)])
                    for r1 in range(9):
                        for r2 in range(r1 + 1, 9):
                            self.cnf.append([-self.var(r1, c, n), -self.var(r2, c, n)])

        # Use get_square() to enforce unique numbers per 3x3 square
        for box_r in range(3):
            for box_c in range(3):
                for n in range(1, 10):
                    cells = [
                        (box_r * 3 + i, box_c * 3 + j) for i in range(3) for j in range(3)
                    ]
                    if n not in self.get_square(cells[0]):  # Check first cell in the box
                        self.cnf.append([self.var(r, c, n) for r, c in cells])
                        for (r1, c1) in cells:
                            for (r2, c2) in cells:
                                if (r1, c1) != (r2, c2):
                                    self.cnf.append([-self.var(r1, c1, n), -self.var(r2, c2, n)])

        # Rule 3: Encode pre-filled numbers
        for r in range(9):
            for c in range(9):
                num = self.sudoku[r * 9 + c]
                if num != '.':
                    self.cnf.append([self.var(r, c, int(num))])  # Force this number


    def solve(self):
        """Solve Sudoku using pycosat."""
        self.generate_cnf()
        solution = pycosat.solve(self.cnf)
        if solution == "UNSAT":
            return None  
        return self.decode_solution(solution)

    def decode_solution(self, solution):
        """Convert SAT solution back into a 9x9 Sudoku grid."""
        grid = [['.' for _ in range(9)] for _ in range(9)]
        for val in solution:
            if val > 0:  
                val -= 1  
                num = val % 9 + 1
                col = (val // 9) % 9
                row = (val // 81)
                grid[row][col] = str(num)
        return grid

    def print_sudoku(self, grid):
        """Print the Sudoku grid."""
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("-" * 21)
            row_str = " ".join(grid[r][c] if grid[r][c] != '.' else '.' for c in range(9))
            print(row_str[:6] + "| " + row_str[6:12] + "| " + row_str[12:])

if __name__ == '__main__':
    # Read Sudoku puzzles from a file
    file_name = "p.txt"
    sudoku_no = 0  # Select the first puzzle from the file
    # file_name = "test.py" 
    # sudoku_no = 0
    with open(file_name, "r") as file:
        sudoku_list = file.readlines()

    solver = Solver(sudoku_list, sudoku_no)
    solved_grid = solver.solve()

    if solved_grid:
        print("\nSolved Sudoku:")
        solver.print_sudoku(solved_grid)
    else:
        print("\nNo solution exists!")
