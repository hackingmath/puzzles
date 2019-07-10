"""
Using backtracker to solve Yohaku Puzzle
https://twitter.com/YohakuPuzzle/status/1145678183150379008
5x5 grid, center 3x3 are prime nums, row/col sums

July 1, 2019"""

import time
from math import sqrt

starttime = time.time()

# from specific puzzle 07/01/19
ROWS = [52,37,90,62,34]
COLS = [57,9,63,91,55]

starting_number = int((2*sum(ROWS)/25 - 24)/2)

# generate list of primes up to highest sum in puzzle
PRIMES = [2,3,5,7,11,13,17,19,23]
NUMS = [i for i in range(starting_number,starting_number+25)]

def row(board,n):
    '''returns values in row n of board'''
    #print(board)
    return board[5*n:5*n+5]

def col(board,n):
    '''returns values in col n of board'''
    col_nums = [[0,5,10,15,20],
                [1,6,11,16,21],
                [2,7,12,17,22],
                [3,8,13,18,23],
                [4,9,14,19,24]]

    return [board[x] for x in col_nums[n]]

def repeat(board):
    """Returns True if there is a repeat"""
    ncount = {}
    for n in board:
        if n == "X":
            return False
        if n in ncount:
            return True
        else:
            ncount[n] = 1
    return False

def print_board(solution_board):
    #board = populate_board(solution_board)
    for i in range(5):
        thisrow = row(solution_board,i)
        for j in range(5):
            print("{}".format(thisrow[j]),end=" ")
        print()
    print() #blank line

def print_solution_board(solution_board):
    #board = populate_board(solution_board)
    for i in range(5):
        thisrow = row(solution_board,i)
        for j in range(5):
            print("{:2d}".format(thisrow[j]),end=" ")
        print()
    print() #blank line

def row_sum(rowlist):
    output = 0
    for x in rowlist:
        if x != "X":
            output += x
    return output

def col_sum(colList):
    output = 0
    for x in colList:
        if x != "X":
            output += x

    return output


def check_no_conflicts(solution_board):
    '''Returns False if there ARE conflicts'''
    #global board1
    #board = populate_board(solution_board)
    #print("populated board:",board)

    #if repeat(solution_board):
        #return False

    for i in range(5):
        thisrow = row(solution_board,i)
        if i in [0,4]:
            for n in thisrow:
                if n in PRIMES:
                    return False
        #print("this row:",thisrow)
        rowsum = row_sum(thisrow)
        if (rowsum > ROWS[i]+1) or (thisrow.count("X") == 0 and rowsum!= ROWS[i]):
            #print("row sum n")
            return False

    for i in range(5):

        thiscol = col(solution_board,i)
        if i in [0,4]:
            for n in thiscol:
                if n in PRIMES:
                    return False
        colsum = col_sum(thiscol)
        if (colsum > COLS[i]+1) or (thiscol.count("X") == 0 and sum(thiscol) != COLS[i]):

            #print("col sum n")
            return False

    for j in [6,7,8,11,12,13,16,17,18]:
        if solution_board[j] == 'X': return True
        if solution_board[j] not in PRIMES:
            #print("not prime")
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
    solution = ["X"]*size
    #print("solution:",solution)

    def extend_solution(position):
        for value in values:
            if value in solution:
                continue
            solution[position] = value
            #print_board(solution)
            if safe_up_to(solution):
                #print("safe up to:",solution,position)
                #solution = solution2
                if position >= size-1 or extend_solution(position+1):
                    return solution
            else:
                solution[position] = "X"
                if value == values[-1]:
                    solution[position-1] = "X"
                if position < size-1:
                    solution[position + 1] = "X"

        return None

    return extend_solution(0)


#board1 = create_board(BOARD)
#print_board(board1)

sol = solve(NUMS,check_no_conflicts,25)
print_solution_board(sol)
print("time (secs):",round(time.time() - starttime,1))
