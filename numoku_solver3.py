'''Originally from 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1086294378413473792
February 3, 2019'''

import copy
import time
import random

starttime = time.time()

#19157 June 6, 2019
BOARD = '....4....8.9..1.3..9.3..2.5....6....'

def calc_quadrant(n):
    '''Calculates which quadrant the given cell is in'''
    quads = [[0,1,2,6,7,8,12,13,14],
             [3,4,5,9,10,11,15,16,17],
             [18,19,20,24,25,26,30,31,32],
             [21,22,23,27,28,29,33,34,35]]
    for q in range(4):
        if n in quads[q]:
            return q

def create_board(board):
    global NUMBLANKS
    NUMBLANKS = 0
    output = []
    for n in board:
        if n != '.':
            term = int(n)
        else:
            term = 0
            NUMBLANKS += 1
        output.append(term)
    return output

def populate_board(boardlist):
    '''Puts new values into existing board spots
    to prevent overwriting hard values'''
    #print("boardlist",boardlist)
    output = []
    board = create_board(BOARD)
    i = 0
    for j in range(36):
        if board[j] == 0:
            output.append(boardlist[i])
            i += 1
        else:
            output.append(board[j])
    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[6*n:6*n+6]

def col(board,n):
    '''returns values in col n of board'''
    output = []
    for j in range(6):
        output.append(board[6*j + n])
    return output

def quadrant(board,n):
    #put values in each quadrant into lists
    quadrants = []
    for j in [0,1,6,7]: #the 4 sub-blocks
        block = []
        for k in range(3):
            block.append(board[6*k+3*j:6*k+3*j+3])
        quad = []
        for thing in block:
            for t in thing:
                quad.append(t)
        quadrants.append(quad)
    return quadrants[n]

def print_board(board):
    #board = []
    if len(board) < 36:
        board = populate_board(board)
    for i in range(6):
        print(row(board,i))
    print() #blank line


def apply_value(self,num,value):
    self.board[num] = value


def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board = populate_board(board)
    for i in range(6):
        thisrow = row(board,i)
        if thisrow.count(0) == 0:
            if sum(thisrow) != 30:
                return False
        thiscol = col(board,i)
        if thiscol.count(0) == 0:
            if sum(thiscol) != 30:
                return False
        for n in range(1,10):
            if row(board,i).count(n) not in [0,1]:
                return False
            if col(board,i).count(n) not in [0,1]:
                return False
            if quadrant(board,(i%4)).count(n) not in [0,1]:
                return False
    '''Only for one puzzle:
    if board[13] != 0 and board[14] != 0:
        if board[13]> board[14]: return False'''
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
    solution = [0]*size

    def extend_solution(position):
        for value in values:
            solution[position] = value
            #print_board(solution)
            if safe_up_to(solution):
                #solution = solution2
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


board1 = create_board(BOARD)
#print_board(board1)

print_board(solve(list(range(1,10)),check_no_conflicts,NUMBLANKS))
print("Time (secs):",round(time.time() - starttime,1))

'''
from 1/03/19
BOARD = '4.6..8...3...1...75...1...4...8..4.2'

from 2/07/19
BOARD = '..869.2.......5..83.79.4.....6..6...'

from 3/15/19
BOARD = '.8....2.7..8...29..568.......3.9..2.'

from 3/21/19
BOARD = '.5..7.7....6..48....61..1....5.9..2.'

19087
BOARD = '5...89.6...2..9......2..6...9.18...6'

from 4/17/2019
19101
BOARD = '.86......6.3.3...24...9.3.9......53.'

#from 1/06/19
#BOARD = '.8.2....9..47...6..9...33..6....2.5.'
#except that a > b:
[4, 8, 6, 2, 9, 1]
[2, 5, 9, 3, 7, 4]
[7, 3, 1, 8, 6, 5]
[8, 9, 5, 4, 1, 3]
[3, 4, 7, 6, 2, 8]
[6, 1, 2, 7, 5, 9]

[6, 8, 4, 2, 9, 1]
[5, 2, 9, 3, 7, 4]
[7, 1, 3, 8, 6, 5]
[8, 9, 5, 4, 1, 3]
[3, 4, 7, 6, 2, 8]
[1, 6, 2, 7, 5, 9]

from 4/18/2019
#19108
BOARD = '..2.8.3..5...7...35...9...7..8.3.1..'
#from 5/02/2019
#19115
BOARD = '.15.....3..2....1498....1..2.....48.'
#19094
BOARD = '...64.7.....5.27....75.6.....7.53...'
#19129 May 10, 2019
BOARD = '...8...8..3.9..5....83.4.5..7...3...'
#19136 May 16, 2019
BOARD = '25...7.....3..74....68..7.....8...64'
#19150 May 30, 2019
BOARD = '7....5...8...362....195...9...3....7'
'''
