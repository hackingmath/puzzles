'''
Using backtracker to solve yohaku puzzle
https://twitter.com/hackingmath/status/1127224655255887872
4x4 grid, consecutive numbers, sums of rows and cols...
center 4 numbers have to be triangular

May 11, 2019'''


import time
import random


starttime = time.time()

BOARD = ['.' for i in range(16)]

ROWS = [27,38,1,22]
COLS = [22,20,11,35]

'''
Trick to find starting number in these consecutive #
puzzles with sums: if you add all the row sums,
you get the sum of all the numbers. The numbers
are an arithmetic sequence.

sum = n(a0+an)/2 --> 2*sum/16 = a0 + a0 + 15
a0 = (2*sum/16 - 15)/2
'''

starting_number = int((2*sum(ROWS)/16 - 15)/2)
NUMS = list(range(starting_number,starting_number+16))

#generate list of triangle numbers to check
triangle_nums = [int(0.5*i*(i+1)) for i in range(1,7)]


def populate_board(boardlist):
    '''Puts new values into existing board spots
    to prevent overwriting hard values'''
    #print("boardlist",boardlist)
    output = []
    board = list(BOARD)
    i = 0
    for j in range(16):
        if boardlist[j] == '.':
            output.append(boardlist[i])
            i += 1
        else:
            output.append(board[j])
    return output

def row(board,n):
    '''returns values in row n of board'''

    return board[4*n:4*n+4]

def col(board,n):
    '''returns values in col n of board'''
    col_nums = [[0,4,8,12],
                [1,5,9,13],
                [2,6,10,14],
                [3,7,11,15]]

    return [board[x] for x in col_nums[n]]


def print_board(solution_board):
    board = list(solution_board)
    for i in range(4):
        print(row(board,i))
    print() #blank line


def apply_value(self,num,value):
    self.board[num] = value


def check_no_conflicts(solution_board):
    '''Returns False if there ARE conflicts'''
    #global board1
    board = list(solution_board)
    #print("populated board:",board)
    for n in NUMS:
        if board.count(n) >1:
            return False

    for i in range(4):
        thisrow = row(board,i)
        #print("this row:",thisrow)
        if thisrow.count('.') == 0:
            #check if row sums are right
            if sum(thisrow) != ROWS[i]:
                #print("row sum n")
                return False

        for n in NUMS:
            if thisrow.count(n) not in [0,1]:
                #print("row count n")
                #print('n:',n,'i:',i,"thisrow:",thisrow)
                return False
        thiscol = col(board,i)
        if thiscol.count('.') == 0:
            if sum(thiscol) != COLS[i]:

                #print("col sum n")
                return False

        for n in NUMS:
            if thiscol.count(n) not in [0,1]:
                #print("col count n")
                #print("n:",n,"i:",i,"thiscol:", thiscol)
                return False

    #check if center squares are triangular
    corners = [board[5], board[6],
               board[9], board[10]]
    if '.' not in corners:
        for c in corners:
            if c not in triangle_nums:
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
    solution = ['.' for i in range(16)]
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
                solution[position] = '.'
                if value != "." and value == values[-1]:
                    solution[position-1] = '.'
                if position < size-1:
                    solution[position + 1] = '.'

        return None

    return extend_solution(0)


board1 = BOARD
#print_board(board1)

print_board(solve(NUMS,check_no_conflicts,16))
print("time (mins):",round((time.time() - starttime)/60,1))
