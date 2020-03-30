'''From Matt Enlow
March 29, 2020'''

import copy
import time
import random

starttime = time.time()


#Puzzle Level 1 Example
LEVEL = 1
BOARD = {5:19,13:5,15:15}

LEVEL = 2
BOARD = {8:21,17:17,18:3}

def populate_board(boardlist):
    '''Puts hard-coded values into boardlist'''
    #print("boardlist",boardlist)
    output = boardlist[::]
    for i in BOARD.keys():
        output.insert(i,BOARD[i])

    return output

def print_board(board):
    g = populate_board(board)
    print()
    if LEVEL == 1:
        for i in range(0,20,5):
            print("{:2} {:2} {:2} {:2} {:2}".format(g[i], g[i+1], g[i+2], g[i+3], g[i+4]))
    else:
        for i in range(0,30,6):
            print("{:2} {:2} {:2} {:2} {:2} {:2}".format(g[i], g[i+1], g[i+2], g[i+3], g[i+4], g[i+5]))


def repeat(board):
    """Returns True if there is a repeat"""
    for n in board:
        if n != 0:
            if board.count(n) > 1:
                return True
    return False

def neighbors(board,n):
    """Returns False if neighbors of a number
    don't include n-1 and n+1"""
    nbs = list()
    #board1 = populate_board(board)
    num = board[n]
    if num == 0:
        return True
    if LEVEL == 1:
        if n % 5 > 0:
            nbs.append(board[n-1])
        if n % 5 < 4:
            nbs.append(board[n+1])
        if n // 5 > 0:
            nbs.append(board[n-5])
        if n // 5 < 3:
            nbs.append(board[n + 5])
        #print(nbs)
        if num == 1:
            if nbs.count(0) == 0:
                if 2 not in nbs:
                    print("2")
                    return False

        elif num == 20:
            if nbs.count(0) == 0:
                if 19 not in nbs:
                    print("19")
                    return False

        else:
            if num not in [1,20]:
                if num - 1 in board and num - 1 not in nbs:
                    return False
                if num + 1 in board and num + 1 not in nbs:
                    return False
                if nbs.count(0) == 0:
                    if num - 1 not in nbs or num + 1 not in nbs:
                        return False
        return True

    else:
        if n % 6 > 0:
            nbs.append(board[n-1])
        if n % 6 < 5:
            nbs.append(board[n+1])
        if n // 6 > 0:
            nbs.append(board[n-6])
        if n // 6 < 4:
            nbs.append(board[n + 6])
        #print(nbs)
        if num == 1:
            if nbs.count(0) == 0:
                if 2 not in nbs:
                    return False
        if num == 30:
            if nbs.count(0) == 0:
                if 29 not in nbs:
                    return False
        else:
            if num not in [1, 30]:
                if num - 1 in board and num - 1 not in nbs:
                    return False
                if num + 1 in board and num + 1 not in nbs:
                    return False
                if nbs.count(0) == 0:
                    if num - 1 not in nbs or num + 1 not in nbs:
                        return False
        return True


def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board = populate_board(board)
    if repeat(board): return False
    if LEVEL == 1: n = 20
    if LEVEL == 2: n = 30
    for i in range(n):
        if not neighbors(board,i):
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


if LEVEL == 1:
    NUMS = list(range(1,21))
else:
    NUMS = list(range(1,31))
for n in BOARD.values():
    NUMS.remove(n)

#print(NUMS)
print("Solution: ")
print_board(solve(NUMS,check_no_conflicts,len(NUMS)))
print("Time (secs):",round(time.time() - starttime,1))

'''
Solution: #200



'''