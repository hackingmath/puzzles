'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1185606828110929921
12x12 Sudoku-like grid, special squares with sum of neighbors
OOP Version October 21, 2019'''

import copy
import time
import random

starttime = time.time()
BOARD = '.......X.XX..6X..7.X.X9.X.X....X......X.....X..XXX1..X9..5......X.X...X....X.X.....X.X7..X8..4X.X.....X....X...X....XX...X5XX.4...1.....X.X.X...'
#Evil 9x9 Sudoku:
#BOARD = '.4.......9.6.1.3..21...6.4....3...5.5.3...2.9.8...7....5.4...37..4.7.9.2.......8.'

class Board(object):
    def __init__(self,board,rows,cols,quadrows,quadcols):
        self.rows = rows
        self.cols = cols
        self.quadrows = quadrows
        self.quadcols = quadcols
        self.BOARD = board
        self.BLANKS = [i for i in range(self.rows*self.cols) if self.BOARD[i] == 'X']
        self.NUMS = [6,5,15,13,7,15,18,17,11,13,14,17,13,6,22,20,25,15,26,16,8,22,19,17,19,21,13,8,19,24,16,7,11,3,14,18] #values of dark digits
        self.NUMBLANKS = self.BOARD.count('.')
        self.created_board = self.create_board()
        self.populated_board = []

    def create_board(self):
        """Takes raw board and replaces dots with blanks
        to be filled with numbers"""
        output = []
        for n in self.BOARD:
            if n == 'X':
                term = 'X'
            elif n == '.':
                term = 0
            else:
                term = int(n)
            output.append(term)
        return output

    def populate_board(self,boardlist):
        '''Puts new values into existing board spots
        to prevent overwriting hard values'''
        output = []
        numscount = 0  # nums in white squares
        i = 0
        for j in range(self.rows * self.cols):
            if self.created_board[j] == 0:
                output.append(boardlist[i])
                i += 1
            elif self.created_board[j] == 'X':
                output.append('X')  # str(NUMS[numscount]))
                numscount += 1

            else:
                output.append(self.created_board[j])

        self.populated_board = list(output)
        return self.populated_board

    def row(self,n):
        '''returns values in row n of board'''
        return self.populated_board[self.cols*n:self.cols*n+self.cols]

    def col(self,n):
        '''returns values in col n of board'''
        output = []
        for j in range(self.rows):
            output.append(self.populated_board[self.rows*j + n])
        return output

    def quadrant(self,n):
        #put values in each quadrant into lists
        quadrants = []
        for k in range(0,self.rows,self.quadrows):
            for j in range(0,self.cols,self.quadcols):
                quadrants.append(self.populated_board[self.cols*k+j:self.cols*k+j+self.quadcols]+\
                                 self.populated_board[self.cols*(k+1)+j:self.cols*(k+1)+j+self.quadcols] +\
                                 self.populated_board[self.cols*(k+2)+j:self.cols*(k+2)+j+self.quadcols])
        return quadrants[n]

    def print_board(self,g):
        if len(g) < self.rows*self.cols:
            #print("g too short")
            self.populate_board(g)
        g = self.populated_board
        for i in range(self.rows):
            if self.cols == 12:
                print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} {g[self.cols*i+3]} | {g[self.cols*i+4]} {g[self.cols*i+5]} {g[self.cols*i+6]} {g[self.cols*i+7]} | {g[self.cols*i+8]} {g[self.cols*i+9]} {g[self.cols*i+10]} {g[self.cols*i+11]}")
            else:
                print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} | {g[self.cols*i+3]} {g[self.cols*i+4]} {g[self.cols*i+5]} | {g[self.cols*i+6]} {g[self.cols*i+7]} | {g[self.cols*i+8]}")# {g[self.cols*i+9]} {g[self.cols*i+10]} {g[self.cols*i+11]}")

            if i%3 == 2:
                print()
        print() #blank line


    def repeat(self,mylist):
        """Returns True if there is a repeat"""
        for n in range(1,10):
            if n not in [0,'X']:
                if mylist.count(n) > 1:
                    return True
        return False

    def neighbors(self,square):
        row = square // self.cols
        col = square % self.cols
        nbs = []
        if row > 0:
            val = self.populated_board[square-self.cols]
            nbs.append(val)
        if col > 0:
            val = self.populated_board[square-1]
            nbs.append(val)
        if row < 11:
            #print(board)
            #print(square,num)
            nbs.append(self.populated_board[square+self.cols])
        if col < 11:
            nbs.append(self.populated_board[square+1])
        while 'X' in nbs:
            nbs.remove('X')
        return nbs

    def check_no_conflicts(self,solutionlist):
        '''Returns False if there ARE conflicts'''
        self.populate_board(solutionlist)

        for x,v in enumerate(self.BLANKS):
            nbs = self.neighbors(v)
            if 0 not in nbs and sum(nbs) != self.NUMS[x]:
                #print("nbs:",v)
                return False

        for i in range(self.rows):
            thisrow = self.row(i)
            #print(thisrow)
            if self.repeat(thisrow):
                #print("repeat row",i)
                return False

            thiscol = self.col(i)
            #print(thiscol)
            if self.repeat(thiscol):
                #print("repeat col", i)
                return False

        for n in range(int(self.rows*self.cols/(self.quadrows*self.quadcols))):
            thisquad = self.quadrant(n)
            #print(n,thisquad)
            if self.repeat(thisquad):
                #print("quad",n)
                return False

        return True


def solve(values, safe_up_to, size):
    """Finds a solution to a backtracking problem.

    values     -- a sequence of values to try, in order. For a map coloring
                  problem, this may be a list of colors, such as ['red',
                  'green', 'yellow', 'purple']
    safe_up_to -- a function with two arguments, solution and position, that
                  returns whether the values assigned to slots 0..pos in
                  the solution list, satisfy the problem constraints.
    size       -- the total number of “slots” you are trying to fill

    Return the solution as a list of values.
    """
    global board
    solution = [0]*board.NUMBLANKS

    def extend_solution(position):
        for value in values:
            solution[position] = value
            board.populate_board(solution)
            #board.print_board(solution)
            if safe_up_to(solution):
                if position >= size-1 or extend_solution(position+1):
                    return solution
            else:
                solution[position] = 0
                if value == values[-1]:
                    solution[position-1] = 0
                if position < size - 1:
                    solution[position + 1] = 0

        return None

    return extend_solution(0)

def test():
    """Prints every step of solution to check functionality"""
    tboard = Board(BOARD,12,12,3,4)
    #create solution list and print it
    tsoln = [random.choice(list(range(1,10))) for i in range(BOARD.count('.'))]
    print(tsoln)
    print()
    #populate and print board
    tboard.print_board(tsoln)
    thisrow = tboard.row(0)
    print("Row 0",thisrow)
    print("Repeat?",tboard.repeat(thisrow))
    thiscol = tboard.col(0)
    print("Col 0", thiscol)
    print("Repeat?", tboard.repeat(thiscol))
    thisquad = tboard.quadrant(0)
    print("Quad 0",thisquad)
    print("Repeat?", tboard.repeat(thisquad))
    this_square = tboard.BLANKS[0]
    nbs = tboard.neighbors(this_square)
    print("Blank 0 neighbors:",nbs)
    print("Sum neighbors: expected",tboard.NUMS[0],"actual",sum(nbs))
    print()

def main():
    global board
    board = Board(BOARD,12,12,3,4)
    #board.populate_board([random.choice([1,2,3,4,5,6,7,8,9]) for i in range(board.NUMBLANKS)])
    #board.print_board(board.populated_board)
    soln = solve(range(1,10),board.check_no_conflicts,board.NUMBLANKS)
    board.print_board(soln)
    print("Time (secs):",round(time.time() - starttime,1))

main()

'''
Solution: 

7 4 2 3 | 8 9 1 X | 5 X X 6
1 6 X 5 | 2 7 3 X | 4 X 9 8
X 9 X 8 | 4 6 5 X | 1 2 3 7

8 3 X 9 | 1 4 2 5 | X 6 7 X
X X 1 7 | 6 X 9 8 | 2 5 4 3
5 2 6 4 | X 3 X 7 | 9 8 X 1

4 5 9 X | 7 X 6 3 | 8 1 2 X
2 X 7 6 | 9 X 8 1 | 3 4 X 5
X 8 3 1 | 5 2 X 4 | 7 9 6 X

9 1 4 X | 3 5 7 6 | X X 8 2
3 X 5 X | X 8 4 2 | 6 7 1 9
6 7 8 2 | X 1 X 9 | X 3 5 4 

'''