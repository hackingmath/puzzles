'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1156966827509129217/photo/1
August 2, 2019'''

import copy
import time
import random

starttime = time.time()

#Puzzle 190726A
BOARD = '...26....6....8...8..1..4......77......5..2..6...2....1....64...'

QUAD_SUMS = [23,14,17,18,21,18,11,22,16,18,20,18,12,22,24,14]

QUADS = [0,0,1,1,2,2,3,3,
             0,0,1,1,2,2,3,3,
             4,4,5,5,6,6,7,7,
             4,4,5,5,6,6,7,7,
             8,8,9,9,10,10,11,11,
             8,8,9,9,10,10,11,11,
             12,12,13,13,14,14,15,15,
             12,12,13,13,14,14,15,15]


def quadrant(board,n):
    '''Returns a list of 4 elements in quadrant n'''
    global QUADS
    return [board[x] for x in range(64) if QUADS[x] == n]

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
    for j in range(64):
        if board[j] == 0:
            output.append(boardlist[i])
            i += 1
        else:
            output.append(board[j])
    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[8*n:8*n+8]

def col(board,n):
    '''returns values in col n of board'''
    output = []
    for j in range(8):
        output.append(board[8*j + n])
    return output

def print_board(board):
    #board = []
    if len(board) < 64:
        board = populate_board(board)
    for i in range(8):
        for n in row(board,i):
            print(n," ",end = "")
        print()
    print() #blank line

def repeat(mylist):
    for n in mylist:
        if n == 0:
            return False
        else:
            if mylist.count(n) > 1:
                return True
    return False



def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board = populate_board(board)
    for i in range(8):
        thisrow = row(board,i)
        if repeat(thisrow):

                return False
        thiscol = col(board,i)
        if repeat(thiscol):

            return False

        thisquad = quadrant(board,i)
        if repeat(thisquad):

            return False
        if thisquad.count(0) == 0 and sum(thisquad) != QUAD_SUMS[i]:

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

print_board(solve(list(range(1,9)),check_no_conflicts,NUMBLANKS))
print("Time (secs):",round(time.time() - starttime,1))

