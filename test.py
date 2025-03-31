import pycosat  

# file = open("p.txt", 'r')
# line= file.readline()
# # print(line)
# rows=[]

# # extractin rows and printing sudoku(row by row)
# for row_no  in range(9):  
#     row=[]
#     for i in range(9):
#         row.append(line[row_no*9 + i])
#     rows.append(row)
# for row  in range(9):  
#         print(rows[row])

# .........
# ...8.5.49
# 2...6.3.1
# ..9......
# ....21.38
# ...3.....
# ..5......
# ..6..48..
# 13...96.2

cnf = [[-1, -2], [1, -2], [1, 2], [-1,2]]
solution = pycosat.solve(cnf)
print(solution)  