"""
Using backtracker to solve Yohaku Puzzle
https://twitter.com/YohakuPuzzle/status/1177196930100846592
3x3 grid of integers, row/col products
top left 2x2 has a sum of 0

Sept 26, 2019"""

import time

starttime = time.time()

ROWS = [-6,90,-14]
COLS = [18,-20,-21]

row_factors = set()
for n in ROWS:
    n = abs(n)
    for i in range(1,n):
        if n % i == 0:
            row_factors.add(i)

col_factors = set()
for n in COLS:
    n = abs(n)
    for i in range(1,n):
        if n % i == 0:
            col_factors.add(i)

num_set = {n for n in row_factors if n in col_factors}
NUMS = []
for n in num_set:
    NUMS.append(n)
    NUMS.append(-1*n)

def row(board,n):
    '''returns values in row n of board'''

    return board[3*n:3*n+3]

def col(board,n):
    '''returns values in col n of board'''
    col_nums = [[0,3,6],
                [1,4,7],
                [2,5,8]]

    return [board[x] for x in col_nums[n]]

def repeat(board):
    """Returns True if there is a repeat"""
    for n in board:
        if n != "X":
            if board.count(n) > 1:
                return True
    return False


def print_board(solution_board):
    #board = populate_board(solution_board)
    if "X" in solution_board:
        print()
        for i in range(3):
            print("{} {} {}".format(row(solution_board, i)[0],
                                             row(solution_board, i)[1],
                                             row(solution_board, i)[2]))
        print()  # blank line
    else:
        print()
        for i in range(3):
            print("{:2d} {:2d} {:2d}".format(row(solution_board,i)[0],
                                                       row(solution_board, i)[1],
                                                       row(solution_board, i)[2]))
        print() #blank line


def check_no_conflicts(solution_board):
    '''Returns False if there ARE conflicts'''
    #global board1
    #board = populate_board(solution_board)
    #print("populated board:",board)

    if repeat(solution_board):
        return False

    for i in range(3):
        thisrow = row(solution_board,i)
        #print("this row:",thisrow)
        if thisrow.count("X") == 0:
            if thisrow[0]*thisrow[1]*thisrow[2] != ROWS[i]:
                #print("row sum n")
                return False

        thiscol = col(solution_board,i)
        if thiscol.count("X") == 0:
            if thiscol[0]*thiscol[1]*thiscol[2] != COLS[i]:

                #print("col sum n")
                return False
    upper_left = [0,1,3,4]
    upper_squares = [solution_board[x] for x in upper_left]
    if upper_squares.count('X') == 0 and sum(upper_squares) !=0:
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
    #print("solution:",solution)

    def extend_solution(position):
        for value in values:
            solution[position] = value
            #print_board(solution)
            if safe_up_to(solution):
                #print("safe up to:",solution,position)
                #solution = solution2
                if position >= size-1 or extend_solution(position+1):
                    return solution
            else:
                solution[position] = 'X'
                if value == values[-1]:
                    solution[position-1] = 'X'
                if position < size-1:
                    solution[position + 1] = 'X'

        return None

    return extend_solution(0)


#board1 = create_board(BOARD)
#print_board(board1)

print_board(solve(NUMS,check_no_conflicts,9))
print("time (secs):",round(time.time() - starttime,1))
