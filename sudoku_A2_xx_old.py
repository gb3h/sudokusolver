import sys
import copy
from heapq import heappush, heappop

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists
        self.neighbours = dict()
        for i in range(0, 81):
            row = self.row(i)
            col = self.col(i)
            sq = self.get_box(i)
            self.neighbours[i] = [x for x in range(0,81) if (self.row(x) == row) or (self.col(x) == col) or (self.get_box(x) == sq)]

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

    class Square(object):
        # A data representation of a single square
        # Holds an id (0-63) and a domain
        def __init__(self, id, domain, fixed, value):
            self.id = id
            self.domain = copy.deepcopy(domain)
            self.fixed = fixed
            self.value = value

        # Constrict removes a list of values from its own domain
        def constrict(self, constraint):
            if constraint in self.domain:
                self.domain.remove(constraint)

        # Comparator for our priority queue
        def __lt__(self, other):
            return len(self.domain) < len(other.domain)
        
        def __str__(self):
            return str(self.value) if self.fixed else str(self.domain)

    class SudokuNode(object):
        def __init__(self, puzzleNode):
            self.puzzle = copy.deepcopy(puzzleNode)
            self.neighbours = dict()
            for i in range(0, 81):
                row = Sudoku.row(i)
                col = Sudoku.col(i)
                sq = Sudoku.get_box(i)
                self.neighbours[i] = [x for x in range(0,81) if (Sudoku.row(x) == row) or (Sudoku.col(x) == col) or (Sudoku.get_box(x) == sq)]

        def get_square(self, id):
            return self.puzzle[Sudoku.row(id)][Sudoku.col(id)]

        def is_finished(self):
            for row in self.puzzle:
                for sq in row:
                    if not sq.fixed:
                        return False
            return True

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

        def __str__(self):
            res = ""
            for row in self.puzzle:
                for square in row:
                    if square.fixed:
                        res += '{:>9}'.format(square.value)
                    else:
                        string = 'D'
                        for x in square.domain:
                            string += str(x)
                        res +='{:>9}'.format(string)
                res += "\n"
            return res

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


    def replace(self, node, replacement):
        new_puzzle = node.puzzle
        new_puzzle[self.row(replacement.id)][self.col(replacement.id)] = copy.deepcopy(replacement)
        return self.SudokuNode(new_puzzle)

    def dfs(self, node, depth):
        print(depth)
        if node.is_finished():
            return node
        for square in node.generate_search_queue():
            a = sorted(square.domain, key=lambda val: node.count_conflicts(square, val))
            # print(square.id, square.value, a)
            for each in a:
                # print(each)
                replacement = self.Square(
                    fixed = True,
                    domain = list(),
                    value = each,
                    id = square.id
                )
                if node.finishable(replacement):
                    new_node = self.replace(node, replacement)
                    # print(new_node)
                    res = self.dfs(new_node, depth+1)
                    if res:
                        return res
        return False
        #     return False

    def solve(self):
        #TODO: Your code here
        squre_form = list()
        for i in range(0,9):
            squre_form.append(list())
            for x in range(0,9):
                if (self.puzzle[i][x] == 0):
                    squre_form[i].append(self.Square(
                        id      = i*9 + x,
                        domain  = [x for x in range(1,10)],
                        fixed   = False,
                        value   = 0
                        ))
                else:
                    squre_form[i].append(self.Square(
                        id      = i*9+x,
                        domain  = list(),
                        fixed   = True,
                        value   = self.puzzle[i][x]
                        ))
        initial_node = self.SudokuNode(squre_form)


        initial_node.init_arc_consistency()

        ans = self.dfs(initial_node, 0)
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
