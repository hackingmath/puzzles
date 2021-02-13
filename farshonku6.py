'''From 1to9puzzle Twitter post
https://twitter.com/1to9puzzle/status/1359899804491345931
February 11, 2021'''

import time
from itertools import combinations

starttime = time.time()

BOARD = '.'*36
TOP = [9,17,5,7,17,13]
BOTTOM = [10,9,25,22,10,13]
LEFT = [10,8,22,10,11,8]
RIGHT = [14,16,8,3,14,13]

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

def combos(arr):
    """Finds sum of increasing or decreasing
    nums from first in arr"""
    output = arr[0] + arr[1]
    if arr[1] > arr[0]:
        for i in range(2,6):
            if arr[i] == 0: return output
            if arr[i] < arr[i-1]:
                return output
            else:
                output += arr[i]
    if arr[1] < arr[0]:
        for i in range(2, 6):
            if arr[i] == 0: return output
            if arr[i] > arr[i - 1]:
                return output
            else:
                output += arr[i]


def check_no_conflicts(board,testing=False):
    '''Returns False if there ARE conflicts'''
    board1 = populate_board(board)
    for i in range(6):
        thisrow = row(board1, i)
        #print(thisrow)
        if repeat(thisrow):
            if testing:
                print(f"row {i} repeat")
                print(thisrow)
            return False
        if sum(thisrow) > 30:
            if testing:
                print(f"row {i} sum")
            return False
        if thisrow.count(0) == 0 and combos(thisrow) != LEFT[i]:
            if testing:
                print(f"row {i} combos")
                print(thisrow, combos(thisrow))
            return False
        reversed_row = thisrow[::-1]
        if reversed_row.count(0) == 0:
            if combos(reversed_row) != RIGHT[i]:
                if testing:
                    print(f"reversed_row {i} combos")
                    print(reversed_row, combos(reversed_row))
                return False
        if thisrow.count(0) == 0 and sum(thisrow) != 30:
            if testing:
                print(f"row {i} count")
                print(thisrow,sum(thisrow))
            return False
        thiscol = col(board1, i)
        #print(thiscol)
        if repeat(thiscol):
            return False
        if thiscol.count(0) == 0:
            if combos(thiscol) != TOP[i]:
            #if combos(thiscol) != None
                if testing:
                    print(f"thiscol {i} combos")
                    print(thiscol, combos(thiscol))
                return False
            if sum(thiscol) != 30:
                if testing:
                    print(f"thiscol {i} sum")
                    print(thiscol, sum(thiscol))
                    return False
        reversed_col = thiscol[::-1]
        if reversed_col.count(0) == 0:
            if combos(reversed_col) != BOTTOM[i]:
                if testing:
                    print(f"reversed_col {i} combos")
                    print(reversed_col, combos(reversed_col))
                return False


    for n in range(4):
        thisquad = quadrant(board1,n)
        #print(n,thisquad)
        if repeat(thisquad):
            #print("quad",n)
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

3  9  7  4  2  5  
8  1  5  7  6  3  
2  4  6  9  8  1  
6  5  9  2  1  7  
7  8  2  3  4  6  
4  3  1  5  9  8  

Time (secs): 0.4
'''
