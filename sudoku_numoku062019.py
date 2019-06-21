'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1141743205022519296
June 20, 2019'''

import copy
import time
import random

starttime = time.time()

boards = []

#from specific puzzle #190118
BOARD = '4x0x00x05\
0700x60xx\
0xx30x200\
600xxx070\
xx006040x\
x07500xx0\
04x00xx01\
00xxx5090\
x060200xx'


def calc_quadrant(n):
    '''Calculates which quadrant the given cell is in'''
    quads = [[0,1,2,9,10,11,18,19,20],
             [3,4,5,12,13,14,21,22,23],
             [6,7,8,15,16,17,24,25,26],
             [27,28,29,36,37,38,45,46,47],
             [30,31,32,39,40,41,48,49,50],
             [33,34,35,42,43,44,51,52,53],
             [54,55,56,63,64,65,72,73,74],
             [57,58,59,66,67,68,75,76,77],
             [60,61,62,69,70,71,78,79,80]]
    for q in range(9):
        if n in quads[q]:
            return q

def create_board(board):

    output = []
    for n in board:
        if n == '\n' or n == ' ': continue
        if n == 'x':
            output.append(' ')
        else:
            output.append(int(n))
    return output

def populate_board(boardlist):
    global board
    '''Puts new values into existing board spots
    to prevent overwriting hard values'''
    #print("boardlist",boardlist)
    output = []
    board = create_board(BOARD)
    #print("board:",board)
    i = 0
    for j in range(81):
        if board[j] == 0:
            #try:
            output.append(boardlist[i])
            i += 1
        else:
            output.append(board[j])

    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[9*n:9*n+9]

def col(board,n):
    '''returns values in col n of board'''
    output = []
    for j in range(9):
        output.append(board[9*j + n])
    return output

def sum_row(board,n):
    output = 0
    for n in row(board,n):
        if n != ' ':
            output += n

    return output == 30


def sum_col(board, n):
    output = 0
    for n in col(board,n):
        if n != ' ':
            output += n

    return output == 30

def quadrant(board,n):
    #put values in each quadrant into lists
    quadrants = []
    for j in [0,1,2,9,10,11,18,19,20]: #the 9 sub-blocks
        block = []
        for k in range(3):
            block.append(board[9*k+3*j:9*k+3*j+3])
        quad = []
        for thing in block:
            for t in thing:
                quad.append(t)
        quadrants.append(quad)
    return quadrants[n]

def print_board(board):
    #board = []
    '''if len(board) < 81:
        board = populate_board(board)'''
    for i in range(9):
        this_row = row(board,i)
        for j in range(9):
            print(this_row[j],end = ' ')
        print()
    print() #blank line


def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board1 = populate_board(board)
    #print("board1:",board1)
    for i in range(9):
        for n in range(1,10):
            this_row = row(board1,i)
            if this_row.count(n) not in [0,1]:
                #print("row_n")
                return False
            this_col = col(board1,i)
            if this_col.count(n) not in [0,1]:
                #print("col_n")
                return False
            this_quad = quadrant(board1,i)
            if this_quad.count(n) not in [0,1]:
                #print("quad_n")
                return False

        if 0 not in row(board1,i) and not sum_row(board1,i):
            #print("sum_row_n")
            return False
        if 0 not in col(board1,i) and not sum_col(board1,i):
            #print("sum_col_n")
            return False

    return True


def solve(values, safe_up_to, size):
    global solution
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
    #board = create_board(solution)

    def extend_solution(position):
        global solution
        for value in values:
            solution[position] = value
            #save_board(solution)
            #print_board(populate_board(solution))
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

#print_board(board1)

soln = solve(list(range(1,10)),check_no_conflicts,36)
#print(soln)
print_board(populate_board(soln))
#get the first 3 numbers in each puzzle. This should have
#turned them into 3-digit numbers. I had to do it manually!
#running_total += sum(row(populate_board(soln),0)[:3])
#print(running_total)

#print(running_total)
print("time (secs):",round(time.time() - starttime,1))

