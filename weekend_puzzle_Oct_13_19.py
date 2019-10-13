'''Adapting my Numoku Solver to do a weekend
https://twitter.com/1to9puzzle/status/1183187525923291137
Oct. 13, 2019'''

import copy
import time
import random

starttime = time.time()


BOARD = "XXXXXXXXXXXX3XXXXXXXXXXXX"
NUMS = [1,2,4,5,6,7,8,9,0]
NUMBLANKS = 0
ROWS = [7,15,9,9,5]
COLS = [25,6,3,1,10]
DIAGS = [10,7]

def create_board(board):
    NUMBLANKS = 0
    for n in board:
        if  n == 'X':
            NUMBLANKS += 1
    return NUMBLANKS

def populate_board(solutionlist):
    '''Puts new values into existing board spots
    to prevent overwriting hard values'''
    #global NUMBLANKS
    #print("boardlist",boardlist)
    output = []
    #NUMBLANKS = create_board(board)
    i = 0
    for j in range(25):
        if BOARD[j] == 'X':
            output.append(solutionlist[i])
            i += 1
        else:
            output.append(int(BOARD[j]))
    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[n*5:5*n+5]

def row_sum(board,n):
    """Returns sum of values in row n"""

    rowsum = 0
    for x in row(board,n):
        if x != 'X':
            rowsum += x
    return rowsum

def col(board,n):
    '''returns values in col n of board'''
    return [board[5*i+n] for i in range(5)]

def col_sum(board,n):
    """Returns sum of values in row n"""
    colsum = 0
    for x in col(board,n):
        if x != 'X':
            colsum += x
    return colsum

def diagonal(board,n):
    #put values in each quadrant into lists
    if n == 0:
        return [board[x] for x in [20,16,12,8,4]]
    else:
        return [board[x] for x in [0,6,12,18,24]]

def print_board(board):
    if len(board) < 81:
        g = populate_board(board)
    else:
        g=list(board)

    print("{} {} {} {} {}".format(g[0],g[1],g[2],g[3],g[4]))
    print("{} {} {} {} {}".format(g[5],g[6],g[7],g[8],g[9]))
    print("{} {} {} {} {}".format(g[10],g[11],g[12],g[13],g[14]))
    print("{} {} {} {} {}".format(g[15],g[16],g[17],g[18],g[19]))
    print("{} {} {} {} {}".format(g[20],g[21],g[22],g[23],g[24]))
    print()

def repeat(board):
    """Returns True if there is a repeat"""
    for n in board:
        if n not in [0,'X'] and board.count(n) > 1:
            return True
    return False



def check_no_conflicts(solutionboard):
    '''Returns False if there ARE conflicts'''
    board = populate_board(solutionboard)
    if repeat(board): return False
    for i in range(5):
        thisrow = row(board, i)
        #print(thisrow)
        if repeat(thisrow):
            #print("row repeat",i)
            return False
        if row_sum(board,i) > ROWS[i]: return False
        if "X" not in thisrow and row_sum(board,i) != ROWS[i]:
            return False

        thiscol = col(board, i)
        if repeat(thiscol):
            #print("col repeat", i)
            return False
        if col_sum(board,i) > COLS[i]: return False
        if 'X' not in thiscol and col_sum(board,i) != COLS[i]:
            return False

    for n in range(2):

        if repeat(diagonal(board,n)):
            print("diagonal {} repeat".format(n))
            #print_board(board)
            return False
        if 'X' not in diagonal(board,n) and sum(diagonal(board,n)) != DIAGS[n]:
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
    solution = ['X']*size

    def extend_solution(position):
        for value in values:
            solution[position] = value
            print_board(solution)
            #print(solution)
            if safe_up_to(solution):
                #solution = solution2
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

def main():

    NUMBLANKS = create_board(BOARD)
    #print("NUMBLANKS:", NUMBLANKS)

    soln = solve(NUMS, check_no_conflicts, 24)
    print_board(soln)

    # soln = [random.choice(['A','B','C','D','E','F','G']) for x in range(NUMBLANKS)]
    # board1 = populate_board(soln)
    # print_board(board1)
    # i = 10
    # print(check_product_squares(board1,i))
    
    total_time = round(time.time() - starttime, 1)
    print("Total time: {}:{}".format(int(total_time // 60), total_time % 60))
    print()

main()


