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
            self.puzzle = puzzleNode#copy.deepcopy(puzzleNode)
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
                    if square.fixed:
                        res += '{:>9}'.format(square.value)
                    else:
                        string = ''
                        for x in square.domain:
                            string += str(x)
                        res +='{:>9}'.format(string)
                    # res +='{:>9}'.format(square.value)  if square.fixed else '{:>9}'.format(str(square.domain))
                res += "\n"
            return res
        
        def clash(self, square):
            row = self.row(square)
            col = self.col(square)
            for other in self.puzzle[row]:
                if other.fixed and (other.value == square.value) and (other.id != square.id):
                    return True
            for a in self.puzzle:
                other = a[col]
                if other.fixed and (other.value == square.value) and (other.id != square.id):
                    return True
            coord = self.from_box_to_coord(self.get_box(square))
            for i in range(0, 3):
                for j in range(0, 3):
                    x = coord[0] + i
                    y = coord[1] + j
                    other = self.puzzle[x][y]
                    if other.fixed and (other.value == square.value) and (other.id != square.id):
                        return True
            return False


        def arc_consistency(self, pq):
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            while (len(pq) > 0):
                curr = heappop(pq)
                if self.clash(curr):
                    return False
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

                #only one
                for num in nums:
                    possibleSquares = []
                    for other in self.puzzle[row]:
                        if num in other.domain:
                            possibleSquares.append(other)
                    if len(possibleSquares) == 1:
                        newSquare = possibleSquares[0]
                        newSquare.value = num
                        newSquare.fixed = True
                        newSquare.domain = []
                        heappush(pq, newSquare)

                for num in nums:
                    for col in range(0, 9):
                        possibleSquares = []
                        for a in self.puzzle:
                            other = a[col]
                            if num in other.domain:
                                possibleSquares.append(other)
                        if len(possibleSquares) == 1:
                            newSquare = possibleSquares[0]
                            newSquare.value = num
                            newSquare.fixed = True
                            newSquare.domain = []
                            heappush(pq, newSquare)

                for num in nums:
                    for box in range(0, 9):
                        possibleSquares = []
                        coord = self.from_box_to_coord(box)
                        for i in range(0, 3):
                            for j in range(0, 3):
                                x = coord[0] + i
                                y = coord[1] + j
                                other = self.puzzle[x][y]
                                if num in other.domain:
                                    possibleSquares.append(other)
                        if len(possibleSquares) == 1:
                            newSquare = possibleSquares[0]
                            newSquare.value = num
                            newSquare.fixed = True
                            newSquare.domain = []
                            heappush(pq, newSquare)
                # while len(other_pq) > 0:
                #     curr = heappop(other_pq)
                #     if len(curr.domain) == 0:
                #         #print(curr)
                #         return False
                #     else:
                #         curr.value = curr.domain[0]
                #         curr.fixed = True
                #         curr.domain = []
                #         heappush(pq, curr)


            return True

        def generate_search_queue(self):
            pq = []
            for row in self.puzzle:
                for square in row:
                    if not square.fixed:
                        heappush(pq, square)
            return pq

        def init_arc_consistency(self):
            pq = []
            for row in self.puzzle:
                for square in row:
                    if square.fixed:
                        heappush(pq, square)
            return self.arc_consistency(pq)

    def replace(self, node, replacement):
        new_puzzle = copy.deepcopy(node.puzzle)
        new_puzzle[node.row(replacement)][node.col(replacement)] = replacement
        #print(super())
        #print(self)
        return self.SudokuNode(puzzleNode = new_puzzle)
            
            

    def dfs(self, node):
        if node.is_finished():
            return node
        # elif node.finishable():
        else:
            for square in node.generate_search_queue():
                for each in square.domain:
                    replacement = self.Square(
                        id = square.id,
                        domain = list(),
                        fixed = True,
                        value = each
                    )
                    new_node = self.replace(node, replacement)
                    passed = new_node.arc_consistency([replacement])
                    print(new_node)
                    if passed:
                        res = self.dfs(new_node)
                    else:
                        res = False
                    if res:
                        return res
            return False
        # else:
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

        initial_node = self.SudokuNode(
            puzzleNode = squre_form
        )

        #print(initial_node)
        initial_node.init_arc_consistency()
        #print(initial_node)

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
