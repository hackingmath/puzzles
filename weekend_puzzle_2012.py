'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1241396589593157632/photo/1
Sudoku Board, with nums on all sides, sums of squares up to and
including 3, 6 or 9
March 21, 2020'''

import copy
import time
import random

starttime = time.time()

LEFT = [3,6,9,10,11,19,13,20,7]
RIGHT = [13,25,11,9,20,6,7,3,24]
TOP = [3,20,24,11,11,19,6,9,22]
BOTTOM = [36,6,14,17,3,21,9,18,11]

def row(board,n):
    '''returns values in row n of board'''
    return board[9*n:9*n+9]

def col(board,n):
    '''returns values in col n of board'''
    output = []
    for j in range(9):
        output.append(board[9*j + n])
    return output

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

    g=list(board)

    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[9],g[10],g[11],g[12],g[13],g[14],g[15],g[16],g[17]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[18],g[19],g[20],g[21],g[22],g[23],g[24],g[25],g[26]))
    print()
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[27],g[28],g[29],g[30],g[31],g[32],g[33],g[34],g[35]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[36],g[37],g[38],g[39],g[40],g[41],g[42],g[43],g[44]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[45],g[46],g[47],g[48],g[49],g[50],g[51],g[52],g[53]))
    print()
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[54],g[55],g[56],g[57],g[58],g[59],g[60],g[61],g[62]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[63],g[64],g[65],g[66],g[67],g[68],g[69],g[70],g[71]))
    print("{:2} {:2} {:2} | {:2} {:2} {:2} | {:2} {:2} {:2}".format(g[72],g[73],g[74],g[75],g[76],g[77],g[78],g[79],g[80]))
    print()
    print()

def left_sum(board,i,testing = False):
    """Returns True if the sum from the left of
    row i is LEFT[i]"""
    this_row = row(board,i)
    if 3 not in this_row: i_3 = 9
    else: i_3 = this_row.index(3)
    if 6 not in this_row: i_6 = 9
    else: i_6 = this_row.index(6)
    if 9 not in this_row: i_9 = 9
    else: i_9 = this_row.index(9)
    idx = min(i_3,i_6,i_9)
    this_slice = this_row[:idx + 1]
    if testing:

        print("left:",idx,this_slice,sum(this_slice))
    return sum(this_slice) == LEFT[i]

def right_sum(board,i,testing = False):
    """Returns True if the sum from the right of
    row i is RIGHT[i]"""
    this_row = row(board,i)
    if 3 not in this_row: i_3 = 9
    else: i_3 = this_row.index(3)
    if 6 not in this_row: i_6 = 9
    else: i_6 = this_row.index(6)
    if 9 not in this_row: i_9 = 9
    else: i_9 = this_row.index(9)
    idx = max(i_3,i_6,i_9)
    this_slice = this_row[idx:]
    if testing:

        print("right:",idx,this_slice,sum(this_slice))
    return sum(this_slice) == RIGHT[i]

def top_sum(board,i,testing = False):
    """Returns True if the sum from the top of
    col i is TOP[i]"""
    this_col = col(board,i)
    if 3 not in this_col: i_3 = 9
    else: i_3 = this_col.index(3)
    if 6 not in this_col: i_6 = 9
    else: i_6 = this_col.index(6)
    if 9 not in this_col: i_9 = 9
    else: i_9 = this_col.index(9)
    idx = min(i_3,i_6,i_9)
    this_slice = this_col[:idx + 1]
    if testing:

        print("top:",idx,this_slice,sum(this_slice))
    return sum(this_slice) == TOP[i]

def bottom_sum(board,i,testing = False):
    """Returns True if the sum from the bottom of
    col i is BOTTOM[i]"""
    this_col = col(board,i)
    if 3 not in this_col: i_3 = 0
    else: i_3 = this_col.index(3)
    if 6 not in this_col: i_6 = 0
    else: i_6 = this_col.index(6)
    if 9 not in this_col: i_9 = 0
    else: i_9 = this_col.index(9)
    idx = max(i_3,i_6,i_9)
    this_slice = this_col[idx:]
    if testing:

        print("bottom:",idx,this_slice,sum(this_slice))
    return sum(this_slice) == BOTTOM[i]

def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    for i in range(9):
        this_row = row(board, i)
        this_col = col(board, i)
        for n in range(1, 10):
            if this_row.count(n) not in [0, 1]:
                return False
            if this_col.count(n) not in [0, 1]:
                return False
            if quadrant(board, i).count(n) not in [0, 1]:
                return False

        if 3 in this_row or 6 in this_row or 9 in this_row:
            if not left_sum(board, i):
                return False
        if this_row.count(0) == 0:
            if not right_sum(board, i):
                return False
        if 3 in this_col or 6 in this_col or 9 in this_col:
            if not top_sum(board, i):
                return False
        if this_col.count(0) == 0:
            if not bottom_sum(board, i):
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
            #save_board(solution)
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

def test():
    NUMS = list(range(1,10))
    board = [random.sample(NUMS,9) for i in range(9)]
    board1 = []
    for r in board:
        for n in r:
            board1.append(n)
    print_board(board1)
    print(row(board1,0))
    print(RIGHT[0])
    print(right_sum(board1,0,True))

def main():

    soln = solve(list(range(1,10)),check_no_conflicts,81)
    # print(soln)
    print_board(soln)
    #get the first 3 numbers in each puzzle. This should have
    #turned them into 3-digit numbers. I had to do it manually!
    #running_total += sum(row(populate_board(soln),0)[:3])
    #print(running_total)

    #print(running_total)

#test()
main()

print("time (secs):",time.time() - starttime)

'''
Solution:

 3  5  1 |  8  2  7 |  6  9  4
 6  4  7 |  3  9  1 |  5  8  2
 9  8  2 |  6  4  5 |  3  1  7

 7  3  8 |  4  5  6 |  1  2  9
 2  9  6 |  7  1  3 |  8  4  5
 5  1  4 |  9  8  2 |  7  3  6

 8  2  3 |  5  7  9 |  4  6  1
 4  7  9 |  1  6  8 |  2  5  3
 1  6  5 |  2  3  4 |  9  7  8


time (secs): 1910.8874769210815
'''