import sys
import copy

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.puzzle[i][j] == '0':
                    self.puzzle[i][j] == '123456789'



        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans

    def removeConfirmed(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if len(self.puzzle[i][j]) == 1:
                    ##clear row
                    for y in range(0, 9):
                        if y != j:
                            self.puzzle[i][y] = self.puzzle[i][y].replace(self.puzzle[i][j], '')
                    ##clear column
                    for x in range(0, 9):
                        if x != i:
                            self.puzzle[x][j] = self.puzzle[x][j].replace(self.puzzle[i][j], '')
                    ##clear box
                    x = i - i%3 #row start
                    y = j - j%3 #column start
                    xEnd = x + 3 #row end
                    yEnd = y + 3 #column end
                    while x < xEnd:
                        while y < yEnd:
                            if x != i and y != j:
                                self.puzzle[x][y].replace(self.puzzle[i][j], '')
                            y + 1
                        y = y - 3
                        x + 1

    def soleAvailNum(self):
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        #by row
        for i in range(0, 9):
            for currentNum in nums:
                availIndex = []
                for j in range(0, 9):
                    if self.puzzle[i][j].find(currentNum) != -1:
                        availIndex.append(j)
                if len(availIndex) == 1:
                    self.puzzle[i][availIndex[0]] = currentNum

        #by col
        for j in range(0, 9):
            for currentNum in nums:
                availIndex = []
                for i in range(0, 9):
                    if self.puzzle[i][j].find(currentNum) != -1:
                        availIndex.append(i)
                if len(availIndex) == 1:
                    self.puzzle[availIndex[0]][j] = currentNum

        #by box
        for x in range(0, 9, 3): #box starting x index
            for y in range(0, 9, 3): #box starting y index
                for currentNum in nums:
                    availIndex = []
                    for i in range(0, 3):
                        for j in range (0, 3):
                            if self.puzzle[i][j].find(currentNum) != -1:
                                availIndex.append([i, j])
                    if len(availIndex) == 1:
                        self.puzzle[availIndex[0]][availIndex[1]] == currentNum







    def

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
