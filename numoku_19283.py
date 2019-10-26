'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1182327992141221888
October 10, 2019'''

import copy
import time
import random

starttime = time.time()

BOARD = '.......4..3..............5..9.......'
SQUARES = {0:8,4:10,6:15,11:11,13:16,17:15,20:19,21:23,26:14,27:20,31:12,34:18} #squares with dark digits in them
NUMS = [8,10,15,11,16,15,19,23,14,20,12,18] #values of dark digits


def sum_neighbors(board,square,num):
    row = square // 6
    col = square % 6
    nbs = []
    if row > 0:
        val = board[square-6]
        nbs.append(val)
    if col > 0:
        val = board[square-1]
        nbs.append(val)
    if row < 5:
        #print(board)
        #print(square,num)
        nbs.append(board[square+6])
    if col < 5:
        nbs.append(board[square+1])
    if 0 not in nbs:
        if sum(nbs) != num:
            return False
    return True


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
        for n in row(board,i):
            print(n," ",end = "")
        print()
    print() #blank line


def repeat(mylist):
    """Returns True if there is a repeat"""
    for n in mylist:
        if n != 0:
            if mylist.count(n) > 1:
                return True
    return False


def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board1 = populate_board(board)
    for i in range(6):
        thisrow = row(board1, i)
        #print(thisrow)
        if repeat(thisrow):
            return False
        '''if sum(thisrow) > 30:
            return False'''
        if thisrow.count(0) == 0 and sum(thisrow) != 30:
            #print(f"row {i} count")
            #print(thisrow,sum(thisrow))
            return False
        thiscol = col(board1, i)
        #print(thiscol)
        if repeat(thiscol):
            return False
        '''if sum(thiscol) > 30:
            return False'''
        if thiscol.count(0) == 0 and sum(thiscol) != 30:
            #print(f"col {i} count")
            return False
    for n in range(4):
        thisquad = quadrant(board1,n)
        #print(n,thisquad)
        if repeat(thisquad):
            #print("quad",n)
            return False

    for i in SQUARES.keys():
        if not sum_neighbors(board1,i,SQUARES[i]):
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
    solution = [0]*size

    def extend_solution(position):
        for value in values:
            solution[position] = value
            print_board(solution)
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

    board1 = create_board(BOARD)
    '''board = [9,3,1,8,5,1,5,9,6,2,6,2,8,3,7,8,5,1,3,6,9,4,6,8,2,2,3,5,4,9]
    print_board(board)
    board2 = populate_board(board)
    #print(check_no_conflicts(board2))
    for i,n in enumerate(numlists):
        boardnums = [board2[num] for num in n]
        print(boardnums)
        print("numlists", i, n)
        if 0 not in boardnums:
            print(sum(boardnums) == SUMS[i])
                #print("Sum:",SUMS[i],sum(boardnums))
                #print("False")'''
    #print(NUMBLANKS)
    #print_board(board1)

    print_board(solve(range(1,10),check_no_conflicts,NUMBLANKS))
    print("Time (secs):",round(time.time() - starttime,1))

main()

'''
Solution: 

9  7  6  5  1  2  
1  4  5  9  3  8  
2  3  8  7  4  6  
4  2  7  6  8  3  
8  5  3  1  9  4  
6  9  1  2  5  7 

'''