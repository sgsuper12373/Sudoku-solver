import pycosat

class Solver :
    def __init__(self,sudoku_lists, sudoku_no):
        self.sudoku = sudoku_lists[sudoku_no]
        self.sudoku_no = sudoku_no
        pass
    def isRowCorrect(self,row):
        pass

    def isColoumnCorrect(self,coloumn):
        pass



    def isSquareCorrectt(self,square):
        pass



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

        
if __name__== '__main__':
    # name=input("File name: ")
    # sudoku_no = int(input(f"Sudoku no: "))
    sudoku_no = 0
    file = open("p.txt", "r")  #change file name with input name
    sudoku_list=file.readlines()
    sudoku_solver = Solver(sudoku_list,sudoku_no)

    # print(sudoku_list[sudoku_no])
    row = sudoku_solver.get_nth_row((2,4))
    print(row)
    print(sudoku_solver.get_nth_coloumn((2,4)))
    print(sudoku_solver.get_square((2,4)))

    file.close