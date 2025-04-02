import pycosat

class Solver :
    def __init__(self,sudoku_lists, sudoku_no):
        self.sudoku = sudoku_lists[sudoku_no]
        self.sudoku_no = sudoku_no
        self.cnf = []
        pass

    def var(self, row, col, num):
        """Return a unique variable for (row, col, num)"""
        return (row * 81) + (col * 9) + num


    def get_row(self, pos):
        # return row elements form position
        x=pos[0]
        y=pos[1]
        row=[]
        for i in range(9):
            if self.sudoku[x*9+i]!='.':
                row.append(self.sudoku[x*9+i])
        return row

    def get_coloumn(self, pos):
        #Return all coloumn elements from position of element
        x=pos[0]
        y=pos[1]
        col=[]
        for i in range(9):
            if self.sudoku[i*9+y] != '.':
                col.append(int(self.sudoku[i*9+y]))
        return col
        pass


    def get_square(self,pos):
        # Returns all numbers in the 3x3 box containing (row, col)
        row=pos[0]
        col=pos[1]
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        box_numbers = []

        for i in range(3):
            for j in range(3):
                index = (start_row + i) * 9 + (start_col + j)
                if self.sudoku[index] != '.' :
                    box_numbers.append(int(self.sudoku[index]))

        return box_numbers


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

        
if __name__== '__main__':
    # name=input("File name: ")
    # sudoku_no = int(input(f"Sudoku no: "))
    # sudoku_no = 0
    file = open("p.txt", "r")  #change file name with input name
    # sudoku_list=file.readlines()
    # sudoku_solver = Solver(sudoku_list,sudoku_no)

    # # print(sudoku_list[sudoku_no])
    # row = sudoku_solver.get_nth_row((2,4))
    # print(row)
    # print(sudoku_solver.get_nth_coloumn((2,4)))
    # print(sudoku_solver.get_square((2,4)))

    file.close