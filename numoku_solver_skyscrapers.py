'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1149354342001983494
Skyscraper function added.
July 11, 2019'''

import copy
import time
import random

starttime = time.time()

#Puzzle 19192
BOARD = '.......7..8..............4..3.......'

"""
Solution:
2  6  8  1  9  4  
5  7  1  6  8  3  
9  3  4  7  5  2  
7  2  5  9  1  6  
1  4  9  5  3  8  
6  8  3  2  4  7  

Time (secs): 3107.9
"""
TOP = [3,3,2,4,1,3] #TOP
BOTTOM = [3,1,2,3,4,2] #BOTTOM
LEFT = [4,3,1,2,3,2] #LEFT
RIGHT = [2,2,4,2,2,2] #RIGHT

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
    output = boardlist[::]

    #i = 0
    for j in range(36):
        b = BOARD[j]
        if b != '.':
            output.insert(j,int(b))
    #print("populated board:",board)
    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[6*n:6*n+6]

def col(board,n):
    '''returns values in col n of board'''
    return [board[6*j + n] for j in range(6)]



def visible(mylist):
    counter = 1
    highest = mylist[0]
    for i in range(1, 6):
        if mylist[i] > highest:
            counter += 1
            highest = mylist[i]
    return counter

# def skyscraper(boardlist):
#     """Returns True if number of skyscrapers visible
#     works in mylist."""
#     for n in range(6):
#         if visible(col(boardlist,n)) != TOP[n]: return False
#         if visible(row(boardlist,n)) != LEFT[n]: return False
#         if visible(col(boardlist,n)[::-1]) != BOTTOM[n]: return False
#         if visible(row(boardlist,n)[::-1]) != RIGHT[n]: return False
#     return True

def quadrant(board,n):
    #put values in each quadrant into lists
    quadrants = []
    for idx,j in enumerate([0,1,6,7]): #the 4 sub-blocks
        quadrants.append([])
        block = []
        for k in range(3):
            for m in range(6*k+3*j,6*k+3*j+3):
                quadrants[idx].append(board[m])
    return quadrants[n]

def print_board(board):
    #board = []
    if len(board) < 36:
        board1 = populate_board(board)
    else:
        board1 = board[::]
    print("board1:",board1)
    for i in range(6):
        for n in row(board1,i):
            print(n," ",end = "")
        print()
    print() #blank line


def check_no_conflicts(board1,testing=False):
    '''Returns False if there ARE conflicts'''
    board = populate_board(board1)
    for i in range(6):
        thisrow = row(board,i)
        for n in thisrow:
            if n == 0: continue
            if thisrow.count(n) > 1:
                if testing:
                    print("row count")
                return False
        if thisrow.count(0) == 0:

            if sum(thisrow) != 30:
                if testing:
                    print("row sum")
                return False
            if visible(thisrow) != LEFT[i]:
                if testing:
                    print("left fail")
                    print("{},{}".format(visible(thisrow),LEFT[i]))
                    #print_board(board)
                return False
            if visible(thisrow[::-1]) != RIGHT[i]:
                if testing:
                    print("right fail")
                    print("{},{}".format(visible(thisrow[::-1]), RIGHT[i]))
                    print_board(board)
                return False
        thiscol = col(board,i)
        for n in thiscol:
            if n != 0 and thiscol.count(n) > 1:
                if testing: print("col count")
                return False
        if thiscol.count(0) == 0:

            if sum(thiscol) != 30:
                if testing: print("col sum")
                return False
            if visible(thiscol) != TOP[i]:
                if testing:
                    print("top fail")
                    print_board(board)
                return False
            if visible(thiscol[::-1]) != BOTTOM[i]:
                if testing:
                    print("bottom fail")
                    print_board(board)
                return False
        for i in range(4):
            thisquad = quadrant(board,i)
            for n in thisquad:
                if n != 0 and thisquad.count(n) > 1:
                    if testing:
                        print("quad count {}".format(n))
                        print(thisquad)
                        print_board(board)
                    return False

    '''if board.count(0) == 0 and not skyscraper(board):
        return False'''

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
            if safe_up_to(solution,False):
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


def main():

    print_board(solve(list(range(1,10)),check_no_conflicts,BOARD.count('.')))
    print("Time (secs):",round(time.time() - starttime,1))

def test():
    board = [random.randint(1,9) for i in range(BOARD.count('.'))]
    board1 = populate_board(board)
    print_board(board1)

#test()
main()

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
#19157 June 6, 2019
BOARD = '....4....8.9..1.3..9.3..2.5....6....'
#19164 June 13, 2019
BOARD = '...2......8...29.73.41...7......8...'
BOARD = '7....8..81...1..5..8..4...92..2....6'
#Puzzle 19185
BOARD = '...2........7.61....89.6........4...'
'''