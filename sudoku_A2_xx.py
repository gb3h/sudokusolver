import sys
import copy
from heapq import heappush, heappop

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

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
        def __init__(self, puzzleNode, past_actions=list()):
            self.puzzle = copy.deepcopy(puzzleNode)
            self.past_actions = past_actions
        
        # helper functions to get a node's col index 0-8
        def col(self, square):
            return square.id % 9
        # helper functions to get a node's row index 0-8
        def row(self, square):
            return square.id // 9
        # helper functions to get a node's square 0-8
        def get_box(self, square):
            c = [[0,1,2],[3,4,5],[6,7,8]]
            return c[self.row(square)//3][self.col(square)//3]
        def from_box_to_coord(self, box):
            c = [[0,0], [0,3], [0,6], [3,0], [3,3], [3,6], [6,0], [6,3], [6,6]]
            return c[box]


        def is_finished(self):
            for row in self.puzzle:
                for square in row:
                    if not square.fixed:
                        return False
            return True

        def finishable(self):
            for row in self.puzzle:
                for square in row:
                    if (not square.fixed) and (len(square.domain) == 0):
                        return False
            return True

        def __str__(self):
            res = ""
            for row in self.puzzle:
                for square in row:
                    res += " " + str(square.value) if square.fixed else " D" + str(len(square.domain))
                res += "\n"
            return res

        def init_arc_consistency(self):
            pq = []
            for row in self.puzzle:
                for square in row:
                    if square.fixed:
                        print(square.id)
                        heappush(pq, square)
            
            count = 0
            while (len(pq) > 0):
                #print("asd ", len(pq))

                curr = heappop(pq)
                count += 1
                row = self.row(curr)
                col = self.col(curr)
                #print("ID =", curr.id, "Val =", curr.value, "|||", row, col, sq)
                for other in self.puzzle[row]:
                    other.constrict(curr.value)
                    if len(other.domain) == 1:
                        other.value = other.domain[0]
                        other.fixed = True
                        other.domain = []
                        heappush(pq, other)
                for a in self.puzzle:
                    other = a[col]
                    if (other.id == 1):
                        print(curr.id)
                    other.constrict(curr.value)
                    if len(other.domain) == 1:
                        other.value = other.domain[0]
                        other.fixed = True
                        other.domain = []
                        heappush(pq, other)
                coord = self.from_box_to_coord(self.get_box(curr))
                for i in range(0, 3):
                    for j in range(0, 3):
                        x = coord[0] + i
                        y = coord[1] + j
                        other = self.puzzle[x][y]
                        other.constrict(curr.value)
                        if len(other.domain) == 1:
                            other.value = other.domain[0]
                            other.fixed = True
                            other.domain = []
                            heappush(pq, other)

    def dfs(self, node):
        node.init_arc_consistency()
        if node.is_finished():
            return node
        elif node.finishable():
            for item in node.generate_search_queue():
                new_node = node.replace(item)
                res = self.dfs(new_node)
            return res
        else:
            return

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

        initial_node = self.SudokuNode(
            puzzleNode = squre_form
        )

        print(initial_node)
        initial_node.init_arc_consistency()
        print(initial_node)

        #ans = self.dfs(initial_node)


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
