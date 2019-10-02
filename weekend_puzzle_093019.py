"""1to9PUzzle Weekend #1939
https://twitter.com/1to9puzzle/status/1177992726538665984
Sept 30, 2019"""
import random
import time

start = time.time()

BOARD = '''1010...0...0\
.1.....11100\
....01110..1\
....11..0111\
111.0.1..2..\
0001..1..0..\
2.21..11.1..\
....012.101.\
12.301.....1\
..0.10.12.0.\
...2.2112.0.\
0111......11'''

NUMBLANKS = BOARD.count('.')


class Cell:
    def __init__(self, num):
        self.val = num  # assign value
        self.connects = 0
        if self.val in ['0123']:
            self.connects = int(self.val)

class Grid:
    def __init__(self):

        self.numList = []
        self.cellList = []

    def create_list(self, alphaList):
        '''splices together BOARD with alphalist'''
        self.numList = []
        count = 0
        for i in BOARD:
            if i in '0123':
                self.numList.append(i)
            else:
                self.numList.append(alphaList[count])
                count += 1

        self.cellList = [Cell(n) for n in self.numList]
        self.calculate_connects(self.numList)
        return self.numList

    def show(self):
        for r in range(12):
            for c in range(12):
                self.cellList[12 * r + c].render(sz * c, sz * r)

    def calculate_connects(self, board):
        for cell in self.cellList:
            cell.connects = 0
        for i, letter in enumerate(board):
            row = i // 12
            col = i % 12
            if letter == 'a':
                if col > 0:
                    self.cellList[i-1].connects += 1
                if col < 11:
                    self.cellList[i+1].connects += 1

            elif letter == 'b':
                if row > 0:
                    self.cellList[i - 12].connects += 1
                if col > 0:
                    self.cellList[i - 1].connects += 1
                
            elif letter == 'c':
                if row < 11:
                    self.cellList[i + 12].connects += 1
                if col > 0:
                    self.cellList[i - 1].connects += 1

            elif letter == 'd':
                if row > 0:
                    self.cellList[i - 12].connects += 1
                if row < 11:
                    self.cellList[i + 12].connects += 1

            elif letter == 'e':
                if row > 0:
                    self.cellList[i - 12].connects += 1
                if col < 11:
                    self.cellList[i + 1].connects += 1

            elif letter == 'f':
                if row < 11:
                    self.cellList[i + 12].connects += 1
                if col < 11:
                    self.cellList[i + 1].connects += 1

    def row_repeat(self, board, n):
        '''returns True if there's a repeat in row n'''
        this_row = board[12 * n:12 * (n + 1)]

        for letter in 'abcdef':
            if this_row.count(letter) > 1:
                # println(this_row)
                return True
        return False

    def col_repeat(self, board, n):
        """Returns True if there's a repeat in column n"""
        this_col = []
        for i, x in enumerate(board):
            if i % 12 == n:
                this_col.append(x)
        # println("col "+str(n))
        # println(this_col)
        for letter in 'abcdef':
            if this_col.count(letter) > 1:
                # println(this_col)
                return True
        return False

    def block_repeat(self, board, n):
        """REturns True if there's a repeat in 3x3 block n"""
        this_block = []
        row_start = 3 * (n // 4)
        col_start = 3 * (n % 4)
        for r in range(3):
            this_row = board[(12 * (row_start + r) + col_start):(12 * (row_start + r) + col_start + 3)]
            for x in this_row:
                this_block.append(x)
        # println(n)
        # println(this_block)
        for letter in 'abcdef':
            if this_block.count(letter) > 1:
                # println(this_block)
                return True
        return False

    def check_no_conflicts(self, solution_board):

        numList = []
        count = 0
        for i in BOARD:
            if i in '0123':
                numList.append(i)
            else:
                numList.append(solution_board[count])
                count += 1
        # update number of connections in cells
        self.calculate_connects(numList)
        # check if any cells are connected over their val
        for cell in self.cellList:
            if cell.val in '0123':
                if int(cell.val) < cell.connects:
                    #print("connects",cell.val, cell.connects,
                    #self.cellList.index(cell))
                    return False 
        for i in range(12):
            if self.row_repeat(numList, i):
                #print("row "+str(i)+" repeat")
                return False
            if self.col_repeat(numList, i):
                #print("col "+str(i)+" repeat")
                return False
        for i in range(16):
            if self.block_repeat(numList, i):
                #print("block "+str(i)+" repeat")
                return False

        # check number of connections matches val
        if "X" not in numList:
            for cell in self.cellList:
                if cell.val in '0123':
                    if int(cell.val) != cell.connects:
                        #print("connects2",cell.val,cell.connects,
                        #self.cellList.index(cell))
                        return False
        return True

    def print_board(self,solution_board):
        b = self.create_list(solution_board)
        print()
        for i in range(12):
            print("{} {} {} | {} {} {} | {} {} {} | {} {} {}".format(b[12*i], b[12*i+1], b[12*i+2],
                                                                     b[12*i+3], b[12*i+4], b[12*i+5],
                                                                     b[12*i+6], b[12*i+7], b[12*i+8],
                                                                     b[12*i+9], b[12*i+10], b[12*i+11]))
            if i %3 == 2:
                print()

    def solve(self):
        """Finds a solution to a backtracking problem."""
        values = 'abcdef'
        solution = ["X"] * NUMBLANKS
        self.create_list(solution)

        def extend_solution(position):
            for value in values:
                solution[position] = value
                #self.print_board(solution)
                #print(''.join(solution))
                if self.check_no_conflicts(solution):
                    # solution = solution2
                    if position >= NUMBLANKS - 1 or extend_solution(position + 1):
                        return solution
                else:
                    solution[position] = "X"
                    if value == values[-1]:
                        solution[position - 1] = "X"
                    if position < NUMBLANKS - 1:
                        solution[position + 1] = "X"

            return None

        return extend_solution(0)


def main():
    global g, BOARD, NUMBLANKS
    # print("NUMBLANKS: "+str(NUMBLANKS))
    g = Grid()  # [random.choice(['a','b','c','d','e','f']) for i in range(NUMBLANKS)])

    #s = list('dacfebbdfecaceabdffdcaebdefacbfbcdeaabfedcdfbcaeebdcfaabedcfecfabdcdfeba')
    #g.check_no_conflicts(s)
    
    soln = g.solve()
    print("SOLUTION:")
    #print(soln)
    g.create_list(soln)
    g.print_board(soln)


main()
print("Time (secs): ",round(time.time() - start,1))


'''SOLUTION:

1 0 1 | 0 d a | c 0 f | e b 0
b 1 d | f e c | a 1 1 | 1 0 0
c e a | b 0 1 | 1 1 0 | d f 1

f d c | a 1 1 | e b 0 | 1 1 1
1 1 1 | d 0 e | 1 f a | 2 c b
0 0 0 | 1 f b | 1 c d | 0 e a

2 a 2 | 1 b f | 1 1 e | 1 d c
d f b | c 0 1 | 2 a 1 | 0 1 e
1 2 e | 3 0 1 | b d c | f a 1

a b 0 | e 1 0 | d 1 2 | c 0 f
e c f | 2 a 2 | 1 1 2 | b 0 d
0 1 1 | 1 c d | f e b | a 1 1

Time (secs):  70.7'''