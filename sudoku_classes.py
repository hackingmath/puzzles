'''Sudoku Solver
OOP Version October 21, 2019'''

import copy
import time
import random

starttime = time.time()
BOARD = '.......X5XX6.6X..73X4X9.X.X....X.2....X.....X..XXX1..X9..5......X.X...X....X.X.....X.X7..X8..4X.X.....X....X...X....XX...X5XX.4...1....2X1X9X...'
#How would this work on a simple ("evil") 9x9 Sudoku? (answer: lightning fast! Around a second)
BOARD = '..1.4.....75.86...89........4....8.15..1.2..37.9....6........49...72.63.....6.1..'

class Board(object):
    def __init__(self,board,rows,cols,quadrows,quadcols):
        self.rows = rows
        self.cols = cols
        self.quadrows = quadrows
        self.quadcols = quadcols
        self.BOARD = board
        self.BLANKS = [i for i in range(self.rows*self.cols) if self.BOARD[i] == 'X']
        #self.NUMS = [6,5,15,13,7,15,18,17,11,13,14,17,13,6,22,20,25,15,26,16,8,22,19,17,19,21,13,8,19,24,16,7,11,3,14,18] #values of dark digits
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
            print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} | {g[self.cols*i+3]} {g[self.cols*i+4]} {g[self.cols*i+5]} | {g[self.cols*i+6]} {g[self.cols*i+7]} {g[self.cols*i+8]}")# {g[self.cols*i+9]} {g[self.cols*i+10]} {g[self.cols*i+11]}")

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

    def check_no_conflicts(self,solutionlist):
        '''Returns False if there ARE conflicts'''
        self.populate_board(solutionlist)

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



def main():
    global board
    board = Board(BOARD,9,9,3,3)
    #board.populate_board([random.choice([1,2,3,4,5,6,7,8,9]) for i in range(board.NUMBLANKS)])
    #board.print_board(board.populated_board)
    soln = solve(range(1,10),board.check_no_conflicts,board.NUMBLANKS)
    board.print_board(soln)
    print("Time (secs):",round(time.time() - starttime,1))

main()

'''
Solution: 


'''