'''Adapting my Numoku Solver to do Euler's
50 Sudoku's
Sept. 12, 2019'''

import copy
import time
import random

starttime = time.time()

#Puzzle 19234
#BOARD = 'XXX..69..XXX.8..4.XXX4....8..9XXX..7.3.XXX.9.2..XXX6..4....1XXX.5..7.XXX..75..XXX'
#BOARD = '.........5.3.67...9..3421.......4.....1...72...2.1.....3......9.8.1..2.....75.8.6'

def configure(puzzle):
    board = []
    '''translating dots to a board'''
    for i in range(9):
        board.append([])
        for j in range(9):
            n = puzzle[9*i+j]
            board[i].append(int(n))
    return board

def create_board(board):
    NUMBLANKS = 0
    for n in board:
        if n == 0:
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
    for j in range(81):
        if b[j] == 0:
            output.append(solutionlist[i])
            i += 1
        else:
            output.append(b[j])
    return output

def row(board,n):
    '''returns values in row n of board'''
    return board[n*9:9*n+9]

def row_sum(board):
    """Returns sum of values in row n"""

    rowsum = 0
    for x in board:
        if x != 0:
            rowsum += x
    return rowsum

def col(board,n):
    '''returns values in col n of board'''
    return [board[9*i+n] for i in range(9)]

def col_sum(board):
    """Returns sum of values in row n"""
    colsum = 0
    for x in board:
        if x != 0:
            colsum += x
    return colsum

def quadrant(board,n):
    #put values in each quadrant into lists
    quads = [[0,1,2,9,10,11,18,19,20],
             [3, 4, 5, 12, 13, 14, 21, 22, 23],
             [6, 7, 8, 15, 16, 17, 24, 25, 26],
             [27, 28, 29, 36, 37, 38, 45, 46, 47],
             [30,31,32,39,40,41,48,49,50],
             [33, 34, 35, 42, 43, 44, 51, 52, 53],
             [54, 55, 56, 63, 64, 65, 72, 73, 74],
             [57, 58, 59, 66, 67, 68, 75, 76, 77],
             [60,61,62,69,70,71,78,79,80]]
    return [board[x] for x in quads[n]]

def print_board(board):
    if len(board) < 81:
        g = populate_board(board)
    else:
        g=list(board)

    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[0],g[1],g[2],g[3],g[4],g[5],g[6],g[7],g[8]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[9],g[10],g[11],g[12],g[13],g[14],g[15],g[16],g[17]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[18],g[19],g[20],g[21],g[22],g[23],g[24],g[25],g[26]))
    print()
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[27],g[28],g[29],g[30],g[31],g[32],g[33],g[34],g[35]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[36],g[37],g[38],g[39],g[40],g[41],g[42],g[43],g[44]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[45],g[46],g[47],g[48],g[49],g[50],g[51],g[52],g[53]))
    print()
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[54],g[55],g[56],g[57],g[58],g[59],g[60],g[61],g[62]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[63],g[64],g[65],g[66],g[67],g[68],g[69],g[70],g[71]))
    print("{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d} |{:2d} {:2d} {:2d}".format(g[72],g[73],g[74],g[75],g[76],g[77],g[78],g[79],g[80]))
    print()
    return int(str(g[0])+str(g[1]) + str(g[2]))


def repeat(board):
    """Returns True if there is a repeat"""
    for n in board:
        if n != 0 and board.count(n) > 1:
            return True
    return False



def check_no_conflicts(board):
    '''Returns False if there ARE conflicts'''
    board = populate_board(board)
    for i in range(9):
        thisrow = row(board, i)
        if repeat(thisrow):
            #print("row repeat",i)
            return False
        if row_sum(thisrow) > 45:
            #print("greater sum row",i)
            return False

        thiscol = col(board, i)
        if repeat(thiscol):
            #print("col repeat", i)
            return False
        if sum(thiscol) > 45:
            #print("greater col row", i)
            return False

    for n in range(6):

        if repeat(quadrant(board,n)):
            #print("quadrant {n} repeat")
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

def main():
    global NUMBLANKS,b,top_left
    NUMBLANKS = 0
    boards = []
    # keep track of 3-digit number in top-left of solution
    top_left = 0
    with open('C:\\Users\\Farrell Family\\Desktop\\p096_sudoku.txt') as f:
        for i in range(50):
            board = ''
            for j in range(10):
                data = f.readline()
                if (j % 10) != 0: #only boards, not headers
                    board += data[:9]
            board = [int(s) for s in board]
            boards.append(board)

    for i,b in enumerate(boards):
        this_board = time.time()
        NUMBLANKS = create_board(b)

        soln = solve(list(range(1, 10)), check_no_conflicts, NUMBLANKS)

        print("Board #{}:".format(i))
        top_left += print_board(soln)
        #top_left += int(str(soln[0]) + str(soln[1]) + str(soln[2]))
        #print()
        print("Top Left:", top_left)
        this_time = round(time.time() - this_board,1)
        print("This board time: {}:{}".format(int(this_time // 60), this_time % 60) )
        total_time = round(time.time() - starttime, 1)
        print("Total time: {}:{}".format(int(total_time // 60), total_time % 60) )
        print()

    #BOARD = "005000400030040000000001006007900000500000060000020050070300000900000200000004007"
    #NUMBLANKS = create_board(BOARD)

    #soln = solve(list(range(1, 10)), check_no_conflicts, NUMBLANKS)


    total_time = round(time.time() - starttime, 1)
    print("Total time: {}:{}".format(int(total_time // 60), total_time % 60))
    print()



main()



#print_board(soln)
print("Top Left:",top_left)

