'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1187356805329874945
Numoku with Skyscraper requirements
 October 26, 2019'''

import copy
import time
import random

starttime = time.time()

BOARD = '.......4..7..............9..5.......'
COLORS = 'RRYRYRRYRWRRRWWWRYRWWWYRRRRWRYRYRRYR'

class Board(object):
    def __init__(self,board,rows,cols,quadrows,quadcols):
        self.rows = rows
        self.cols = cols
        self.quadrows = quadrows
        self.quadcols = quadcols
        self.BOARD = board
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
                term = 'X'
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
            if self.created_board[j] == 'X':
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
        """put values in each quadrant into lists"""
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
            elif self.cols == 9:
                print(f"{g[self.cols*i+0]} {g[self.cols*i+1]} {g[self.cols*i+2]} | {g[self.cols*i+3]} {g[self.cols*i+4]} {g[self.cols*i+5]} | {g[self.cols*i+6]} {g[self.cols*i+7]} | {g[self.cols*i+8]}")# {g[self.cols*i+9]} {g[self.cols*i+10]} {g[self.cols*i+11]}")
            elif self.cols == 6:
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

    def print_colors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(f"{COLORS[self.rows*i + j]}",end = " ")
            print()

    def visible(self,square):
        """Returns how many directions it's visible from in skyscraper model"""
        visnum = 0
        rownum = square // self.cols
        colnum = square % self.cols
        thisrow = self.row(rownum)
        thiscol = self.col(colnum)
        #left
        mynum = self.populated_board[square]
        if mynum == max(thisrow[:(colnum+1)]):
            visnum += 1
        #right
        if mynum == max(thisrow[colnum:]):
            visnum += 1
        #up
        if mynum == max(thiscol[:rownum + 1]):
            visnum += 1
        #down
        if mynum == max(thiscol[rownum:]):
            visnum += 1

        if visnum > 1:
            return "R"
        elif visnum == 1:
            return "Y"
        else:
            return "W"


    def neighbors(self,square):
        row = square // self.cols
        col = square % self.cols
        return self.row(row) + self.col(col)
        nbs = []
        if row > 0:
            val = self.populated_board[square-self.cols]
            nbs.append(val)
        else: nbs.append(0)
        if col > 0:
            val = self.populated_board[square-1]
            nbs.append(val)
        else: nbs.append(0)
        if row < self.rows-1:
            #print(board)
            #print(square,num)
            nbs.append(self.populated_board[square+self.cols])
        else:
            nbs.append(0)
        if col < self.cols-1:
            nbs.append(self.populated_board[square+1])
        else:
            nbs.append(0)
        '''while 'X' in nbs:
            nbs.remove('X')'''

        return nbs


    def check_no_conflicts(self,solutionlist):
        '''Returns False if there ARE conflicts'''
        self.populate_board(solutionlist)

        for i in range(self.rows):
            thisrow = self.row(i)
            #print(thisrow)
            if self.repeat(thisrow):
                #print("repeat row",i)
                return False
            if thisrow.count('X') == 0 and sum(thisrow) != 30:
                return False

            thiscol = self.col(i)
            #print(thiscol)
            if self.repeat(thiscol):
                #print("repeat col", i)
                return False
            if thiscol.count('X') == 0 and sum(thiscol) != 30:
                return False

        for n in range(int(self.rows*self.cols/(self.quadrows*self.quadcols))):
            thisquad = self.quadrant(n)
            #print(n,thisquad)
            if self.repeat(thisquad):
                #print("quad",n)
                return False

        for i in range(self.rows*self.cols):
            if COLORS[i] == 'W':
                mynum = self.populated_board[i]
                if mynum != 'X' and mynum > 6:
                    return False
            if 'X' not in self.neighbors(i):
                if self.visible(i) != COLORS[i]:
                    # print("Visible square", i)
                    # print("this square:",self.populated_board[i])
                    # print("neighbs:",self.neighbors(i))
                    # print("Sum neighbors: expected", COLORS[i], "actual", self.visible(i))
                    # print("check?", COLORS[i] == self.check_neighbors(i))
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
    solution = ['X']*board.NUMBLANKS

    def extend_solution(position):
        for value in values:
            solution[position] = value
            board.populate_board(solution)
            #board.print_board(solution)
            if safe_up_to(solution):
                if position >= size-1 or extend_solution(position+1):
                    return solution
            else:
                solution[position] = 'X'
                if value == values[-1]:
                    solution[position-1] = 'X'
                if position < size - 1:
                    solution[position + 1] = 'X'

        return None

    return extend_solution(0)

def test():
    """Prints every step of solution to check functionality"""
    tboard = Board(BOARD,6,6,3,3)
    #create solution list and print it
    tsoln = [random.choice(list(range(1,10))) for i in range(tboard.NUMBLANKS)]
    print(tsoln)
    print()
    #populate and print board
    tboard.print_board(tsoln)
    tboard.print_colors()
    thisrow = tboard.row(0)
    print("Row 0",thisrow)
    print("Repeat?",tboard.repeat(thisrow))
    thiscol = tboard.col(0)
    print("Col 0", thiscol)
    print("Repeat?", tboard.repeat(thiscol))
    thisquad = tboard.quadrant(0)
    print("Quad 0",thisquad)
    print("Repeat?", tboard.repeat(thisquad))
    this_square = 4
    print("This square:",tboard.populated_board[this_square])
    nbs = tboard.neighbors(this_square)
    print("Square 0 neighbors:",nbs)
    print("Sum neighbors: expected",COLORS[this_square],"actual",tboard.visible(this_square))
    #print("check?",COLORS[this_square] == tboard.check_neighbors(this_square))
    print()

def main():
    global board
    board = Board(BOARD,6,6,3,3)
    #board.populate_board([random.choice([1,2,3,4,5,6,7,8,9]) for i in range(board.NUMBLANKS)])
    #board.print_board(board.populated_board)
    soln = solve(range(1,10),board.check_no_conflicts,board.NUMBLANKS)
    board.print_board(soln)
    print("Time (secs):",round(time.time() - starttime,1))

main()
#test()

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