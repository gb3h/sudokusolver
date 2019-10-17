import time
import sys
import copy
import itertools
from heapq import heappush, heappop

class Sudoku(object):
    def __str__(self):
        return str(self.domains)

    def get(self, index):
        return self.puzzle[index//9][index%9]

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.count = 0
        self.ans = copy.deepcopy(puzzle)
        self.squares = [x for x in range(0, 81)]
        self.domains = {}
        index = 0
        for row in self.puzzle:
            for num in row:
                if (num == 0):
                    self.domains[index] = [x for x in range(1,10)]
                else:
                    self.domains[index] = [num]
                index += 1

        self.neighbours = dict()
        for i in range(0, 81):
            row = Sudoku.row(i)
            col = Sudoku.col(i)
            sq = Sudoku.get_box(i)
            self.neighbours[i] = [x for x in range(0,81) if (Sudoku.row(x) == row) or (Sudoku.col(x) == col) or (Sudoku.get_box(x) == sq)]

        self.temp = dict()
        for i in self.squares:
            if self.get(i) == 0:
                self.temp[i] = list()
            else:
                self.temp[i] = [self.get(i)]

    @staticmethod
    def col(id):
        return id % 9
    # helper functions to get a node's row index 0-8
    @staticmethod
    def row(id):
        return id // 9
    # helper functions to get a node's square 0-8
    @staticmethod
    def get_box(id):
        c = [[0,1,2],[3,4,5],[6,7,8]]
        return c[Sudoku.row(id)//3][Sudoku.col(id)//3]
    @staticmethod
    def from_box_to_coord(box):
        c = [[0,0], [0,3], [0,6], [3,0], [3,3], [3,6], [6,0], [6,3], [6,6]]
        return c[box]

    def finished(self):
        for x in self.squares:
            if len(self.domains[x]) > 1:
                return False
        return True

    def finishable(self, fixed_list):
        for x in self.squares:
            if len(self.domains[x]) > 1 and x not in fixed_list:
                return False
        return True

    def consistent(self, fixed_list, sq, value):
        for key, val in fixed_list.items():
            if val == value and key in self.neighbours[sq]:
                consistent = False
        return True 

    def assign(self, sq, value, fixed_list):
        fixed_list[sq] = value
        self.forward_check(sq, value, fixed_list)

    def unassign(self, sq, fixed_list):
        if sq in fixed_list:
            for (D, v) in self.temp[sq]:
                self.domains[D].append(v)
            self.temp[sq] = []
            del fixed_list[sq]

    def forward_check(self, sq, value, fixed_list):
        for n in self.neighbours[sq]:
            if n not in fixed_list:
                if value in self.domains[n]:
                    self.domains[n].remove(value)
                    self.temp[sq].append((n, value))

    @staticmethod
    def constraint(xi, xj): return xi != xj

    @staticmethod
    def permutate(iterable):
        result = list()
        for L in range(0, len(iterable) + 1):
            if L == 2:
                for subset in itertools.permutations(iterable, L):
                    result.append(subset)
        return result

    @staticmethod
    def conflicts(sudoku, sq, val):
        count = 0
        for n in sudoku.neighbours[sq]:
            if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
                count += 1
        return count

    def solve(self):
        def ac3(sudoku):
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

        def backtrack(fixed_list, sudoku):
            sudoku.count += 1
            if len(fixed_list) == len(sudoku.squares):
                return fixed_list
            var = select_unassigned_variable(fixed_list, sudoku)
            for value in order_domain_values(sudoku, var):
                if sudoku.consistent(fixed_list, var, value):
                    sudoku.assign(var, value, fixed_list)
                    result = backtrack(fixed_list, sudoku)
                    if result:
                        return result
                    sudoku.unassign(var, fixed_list)
            return False

        # Most Constrained Variable heuristic
        # Pick the unassigned variable that has fewest legal values remaining.
        def select_unassigned_variable(fixed_list, sudoku):
            unassigned = [v for v in sudoku.squares if v not in fixed_list]
            return min(unassigned, key=lambda var: len(sudoku.domains[var]))

        # Least Constraining Value heuristic
        # Prefers the value that rules out the fewest choices for the neighboring variables in the constraint graph.
        def order_domain_values(sudoku, var):
            if len(sudoku.domains[var]) == 1:
                return sudoku.domains[var]
            return sorted(sudoku.domains[var], key=lambda val: sudoku.conflicts(sudoku, var, val))

        if ac3(sudoku):
            if sudoku.finished():
                print(sudoku)
            else:
                # print(sudoku)
                fixed_list = {}
                for x in sudoku.squares:
                    if len(sudoku.domains[x]) == 1:
                        fixed_list[x] = sudoku.domains[x][0]
                fixed_list = backtrack(fixed_list, sudoku)
                for d in sudoku.domains:
                    sudoku.domains[d] = fixed_list[d] 
                if fixed_list:
                    ls = []
                    for x in range(0,9):
                        ls.append([fixed_list[i+x*9] for i in range(0,9)])
                else:
                    print("No solution exists")

        self.ans = ls
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

    a = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    b = time.time()
    print("Time taken:", b-a)
    print("Backtracking calls:", sudoku.count)
    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
