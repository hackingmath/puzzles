'''Sudoku and Numoku Solver
OOP Version October 21, 2019'''

import copy
import time
import random

starttime = time.time()

"""For Sudoku, in main() set board = Board(9,9,3,3)
For Numoku set board = Board(6,6,3,3)"""

BOARD = '..1.4.....75.86...89........4....8.15..1.2..37.9....6........49...72.63.....6.1..'
#BOARD = '...8...8..3.9..5....83.4.5..7...3...'
class Board(object):
    def __init__(self,board,rows,cols,quadrows,quadcols):
        self.rows = rows
        self.cols = cols
        self.quadrows = quadrows
        self.quadcols = quadcols
        self.BOARD = board
        self.BLANKS = [i for i in range(self.rows*self.cols) if self.BOARD[i] == 'X']
        self.NUMBLANKS = self.BOARD.count('.')
        self.created_board = self.create_board()
        self.populated_board = []

    def create_board(self):
        """Takes raw board and replaces dots with blanks
        to be filled with numbers"""
        output = []
        for n in self.BOARD:
            if n == '.':
                term = 0
            else:
                term = int(n)
            output.append(term)
        return output

    def populate_board(self,boardlist):
        '''Puts new values into existing board spots
        to prevent overwriting hard values'''
        output = []
        i = 0
        for j in range(self.rows * self.cols):
            if self.created_board[j] == 0:
                output.append(boardlist[i])
                i += 1
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
            if self.rows == 9:
                print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} | {g[self.cols*i+3]} {g[self.cols*i+4]} {g[self.cols*i+5]} | {g[self.cols*i+6]} {g[self.cols*i+7]} {g[self.cols*i+8]}")# {g[self.cols*i+9]} {g[self.cols*i+10]} {g[self.cols*i+11]}")
            else:
                print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} | {g[self.cols*i+3]} {g[self.cols*i+4]} {g[self.cols*i+5]}")
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
            if self.rows == 6:
                if thisrow.count(0) == 0 and sum(thisrow) != 30:
                    return False

            thiscol = self.col(i)
            #print(thiscol)
            if self.repeat(thiscol):
                #print("repeat col", i)
                return False
            if self.rows == 6:
                if thiscol.count(0) == 0 and sum(thiscol) != 30:
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

2 3 1 | 9 4 5 | 7 8 6
4 7 5 | 3 8 6 | 9 1 2
8 9 6 | 2 7 1 | 3 5 4

3 4 2 | 6 5 7 | 8 9 1
5 6 8 | 1 9 2 | 4 7 3
7 1 9 | 4 3 8 | 2 6 5

6 2 7 | 8 1 3 | 5 4 9
1 5 4 | 7 2 9 | 6 3 8
9 8 3 | 5 6 4 | 1 2 7


Time (secs): 0.9

'''