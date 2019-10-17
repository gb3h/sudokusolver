import sys
import copy
from heapq import heappush, heappop

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    class SudokuNode(object):
        def __init__(self, puzzleNode):
            self.puzzle = copy.deepcopy(puzzleNode)
            self.squares = [x for x in range(0, 81)]
            self.domain = dict()
            self.fixed = list()
            self.neighbours = dict()
            for i in range(0, 81):
                row = Sudoku.row(i)
                col = Sudoku.col(i)
                sq = Sudoku.get_box(i)
                self.neighbours[i] = [x for x in range(0,81) if (Sudoku.row(x) == row) or (Sudoku.col(x) == col) or (Sudoku.get_box(x) == sq)]

            

        def finishable(self, square):
            for neighbour in self.neighbours[square.id]:
                neighbour = self.get_square(neighbour)
                if neighbour.fixed and (neighbour.value == square.value) and (neighbour.id != square.id):
                    return False
            return True

        def consistent(self):
            for row in self.puzzle:
                for square in row:
                    if square.fixed:
                        for each in self.neighbours[square.id]:
                            neighbour = self.get_square(each)
                            if (neighbour.id != square.id) and (neighbour.value == square.value):
                                # print(neighbour.id, neighbour.value, square.id, square.value)
                                return False
            return True

        def arc_consistency(self, pq):
            while (len(pq) > 0):
                curr = heappop(pq)
                for neighbour in self.neighbours[curr.id]:
                    neighbour = self.get_square(neighbour)
                    neighbour.constrict(curr.value)
                    if neighbour.fixed:
                        if (neighbour.value == curr.value) and (neighbour.id != curr.id):
                            return False
                    elif (not neighbour.fixed):
                        if (len(neighbour.domain) == 0):
                            return False
                        if (len(neighbour.domain) == 1):
                            neighbour.fixed = True
                            neighbour.value = neighbour.domain[0]
                            neighbour.domain = []
            return True

        def init_arc_consistency(self):
            pq = []
            for row in self.puzzle:
                for square in row:
                    if square.fixed:
                        heappush(pq, square)
                        self.num_fixed += 1
            return self.arc_consistency(pq)

        def generate_search_queue(self):
            pq = []
            for row in self.puzzle:
                for square in row:
                    if not square.fixed:
                        heappush(pq, copy.deepcopy(square))
            return pq

        def count_conflicts(self, square, value):
            count = 0
            for n in self.neighbours[square.id]:
                n = self.get_square(n)
                if len(n.domain) >= 1 and value in n.domain:
                    count += 1
            return count




    def dfs(self, node):
        if node.is_finished():
            return node
        for square in node.generate_search_queue():
            a = sorted(square.domain, key=lambda val: node.count_conflicts(square, val))
            # print(a)
            for each in a:
                if node.finishable(square.id, each):
                    node.replace(square.id, each)
                    res = self.dfs(node)
                    if node:
                        return node
                    node.undo(square.id, each) 
        return False
        #     return False

    def solve(self):
        
        initial_node = self.SudokuNode(
            puzzleNode = puzzle
        )

        # print(initial_node)
        initial_node.init_arc_consistency()
        print(initial_node)

        ans = self.dfs(initial_node)
        print(ans)


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

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
