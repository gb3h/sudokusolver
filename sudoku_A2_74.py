import sys
import copy
import itertools
from heapq import heappush, heappop
# import statistics
# import time

class Sudoku(object):
    def __str__(self):
        return str(self.domains)

    # Method called get that returns the value of a certain index (we maintain indexes from 0-80)
    def get(self, index):
        return self.puzzle[index // 9][index % 9]

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.ans = copy.deepcopy(puzzle)

        # DFS counter to keep track of recursive calls for statistics
        # self.count = 0

        # Squares are our individual cells, indexed from 0-80
        self.squares = [x for x in range(0, 81)]

        # Init domains with 1-9 unless fixed val
        self.domains = {}
        index = 0
        for row in self.puzzle:
            for num in row:
                if (num == 0):
                    self.domains[index] = [x for x in range(1, 10)]
                else:
                    self.domains[index] = [num]
                index += 1

        # Initialise a neighbours map to easile get neighbours of a square
        # Calling neighbours[i] will get you all of i's neighbours
        self.neighbours = dict()
        for i in range(0, 81):
            row = Sudoku.row(i)
            col = Sudoku.col(i)
            sq = Sudoku.get_box(i)
            self.neighbours[i] = [x for x in range(0,81) if (Sudoku.row(x) == row) or (Sudoku.col(x) == col) or (Sudoku.get_box(x) == sq)]

        # Init temp tracker to track guesses in case we need to undo them later
        self.temp = dict()
        for i in self.squares:
            if self.get(i) == 0:
                self.temp[i] = list()
            else:
                self.temp[i] = [self.get(i)]

    # Helper function to get a square's col index 0-8
    @staticmethod
    def col(id):
        return id % 9
    # Helper functions to get a square's row index 0-8
    @staticmethod
    def row(id):
        return id // 9
    # Helper functions to get a square's box 0-8
    @staticmethod
    def get_box(id):
        c = [[0,1,2],[3,4,5],[6,7,8]]
        return c[Sudoku.row(id)//3][Sudoku.col(id)//3]

    # Finished method to check if a search has reached goal state
    # Domain of every square should be length 1
    def finished(self):
        for x in self.squares:
            if len(self.domains[x]) > 1:
                return False
        return True

    # Whenever we make a guess, first check that the guess is consistent
    def consistent(self, fixed_list, sq, value):
        for sq, val in fixed_list.items():
            if val == value and sq in self.neighbours[sq]:
                consistent = False
        return True 

    # When we make assignment, do a forward check to ensure neighbours are correct
    def assign(self, sq, value, fixed_list):
        fixed_list[sq] = value
        for n in self.neighbours[sq]:
            if not n in fixed_list:
                if value in self.domains[n]:
                    self.domains[n].remove(value)
                    self.temp[sq].append((n, value))

    # If an assignment/guess fails, restore state from temp with this undo method
    def undo(self, sq, fixed_list):
        if sq in fixed_list:
            for (other_sq, val) in self.temp[sq]:
                self.domains[other_sq].append(val)
            self.temp[sq] = []
            del fixed_list[sq]

    # Count num conflicts for our LCV heuristic
    def count_conflicts(self, sq, val):
        count = 0
        for n in self.neighbours[sq]:
            if len(self.domains[n]) > 1 and val in self.domains[n]:
                count += 1
        return count

    # Method to format our final list into the specification format
    @staticmethod
    def format_from_assignment(fixed_list):
        ls = []
        for x in range(0,9):
            ls.append([fixed_list[i+x*9] for i in range(0,9)])
        return ls

    # LCV heuristic, makes choice within domain based on its impact on neighbours
    def get_LCV(self, sq):
        ls = sorted(self.domains[sq], key=lambda val: self.count_conflicts(sq, val))
        return self.domains[sq] if (len(self.domains) == 1) else ls

    # MCV heuristic, sorts by smallest domain for unfixed squares and returns the lowest
    def get_MCV(self, fixed_list):
        unfixed_list = [sq for sq in self.squares if not sq in fixed_list]
        min_sq = min(unfixed_list, key=lambda i: len(self.domains[i]))
        return min_sq 

    # AC3 algorithm to force all neighbours to be consistent with fixed squares
    def make_arc_consistent(self):
        q = [x for x in self.squares if (self.get(x) != 0)]
        while (len(q) > 0):
            curr = q.pop(0)
            val = self.get(curr)
            for neighbour in self.neighbours[curr]:
                if val in self.domains[neighbour] and (neighbour != curr):
                    self.domains[neighbour].remove(val)
                    if len(self.domains[neighbour]) == 1:
                        q.append(neighbour)
                if len(self.domains[neighbour]) == 0:
                    return False
        return True

    def solve(self):
        def dfs(fixed_list, sudoku):
            # sudoku.count += 1
            if len(fixed_list) == 81:
                return fixed_list
            min_sq = sudoku.get_MCV(fixed_list)
            for value in sudoku.get_LCV(min_sq):
                if sudoku.consistent(fixed_list, min_sq, value):
                    sudoku.assign(min_sq, value, fixed_list)
                    res = dfs(fixed_list, sudoku)
                    if res:
                        return res
                    sudoku.undo(min_sq, fixed_list)
            return False

        if sudoku.make_arc_consistent():
            if not sudoku.finished():
                # domain_len = []
                # for each in sudoku.domains:
                #     if len(sudoku.domains[each]) > 1:
                #         zz.append(len(sudoku.domains[each]))
                # print(statistics.mean(domain_len))
                # print(statistics.median(domain_len))
                fixed_list = {}
                for x in sudoku.squares:
                    if len(sudoku.domains[x]) == 1:
                        fixed_list[x] = sudoku.domains[x][0]
                fixed_list = dfs(fixed_list, sudoku)
                for d in sudoku.domains:
                    sudoku.domains[d] = fixed_list[d] 
                if fixed_list:
                    ls = sudoku.format_from_assignment(fixed_list)
                else:
                    print("Unsolvable")
            else:
                ls = sudoku.format_from_assignment(sudoku.domains)

        self.ans = (ls if ls else self.ans)
        # don't print anything here. just resturn the answer
        # self.ans is a list of lists
        return self.ans
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

    # a = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    # b = time.time()
    # print("Time taken:", b-a)
    # print("Backtracking calls:", sudoku.count)
    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
