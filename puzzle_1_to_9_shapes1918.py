'''1 to 9 puzzle #1918
https://twitter.com/1to9puzzle/status/1124721676900392960
May 5, 2019
3 shapes in a 9x9 grid'''

import random
import time

starttime = time.time()

SHAPES = ['N','C','S','T']
SHAPE_NUMS = [0,1,2,3] #blank, circle, square, triangle

BOARD = '..NC..N...C....N.S..NNT....S.S..N......SN...T.N.....NC....NN.N.ST.....S.T....NN..'

def adjacent(board,n,testing=False):
    """Calculates most adjacent shapes, and returns
    number 1,2,3 or N if none predominate"""
    neighbs = []
    if n > 8:
        up_n = n - 9
        neighbs.append(board[up_n])
    if n < 72:
        down_n = n + 9
        neighbs.append(board[down_n])
    if n % 9 > 0:
        left_n = n - 1
        neighbs.append(board[left_n])
    if n % 9 < 8:
        right_n = n + 1
        neighbs.append(board[right_n])
    if testing:
        print("neighbs:",neighbs)
    if 0 in neighbs:
        return True
    counts = {'1':0,'2':0,'3':0}
    for c in neighbs:
        if c in [1,2,3]:
            counts[str(c)] += 1
    if testing:
        print("counts:",counts)
    if (board[n] == 'N') and (counts['1'] == counts['2'] == counts['3']):
        return True
    max_value = max(counts.values())
    maxima = [key for key, value in counts.items() if value == max_value]
    if testing:
        print ("max_value:",max_value)
        print("maxima:",maxima)
    if len(maxima) > 1:
        if board[n] == 'N':
            return True
        else:
            return False
    if len(maxima) == 1 and SHAPES[int(maxima[0])] == board[n]:
        return True
    return False

def test_adjacent():
    output = []
    for c in BOARD:
        if c == '.':
            output.append(random.choice([1,2,3]))
        else:
            output.append(c)
    print_board(output)
    for i,cell in enumerate(output):
        if cell in SHAPES:
            print("cell:",cell)
            print(adjacent(output,i,True))

###BORROWED FROM SUDOKU SOLVER CODE

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
    '''Counts number of blank cells to be filled in'''
    global NUMBLANKS
    NUMBLANKS = 0
    output = []
    for n in board:
        if n == '.':
            NUMBLANKS += 1
            output.append(0)
        else:
            output.append(n)
        #print("NUMBLANKS:",NUMBLANKS)
    return output

def populate_board(boardlist):
    '''Puts new values into existing board spots
    to prevent overwriting hard values'''
    #print("boardlist",boardlist)
    output = []
    board = create_board(BOARD)
    #print("PopBoard:",board)
    i = 0
    for j,num in enumerate(board):
        if board[j] == 0:
            output.append(boardlist[i])
            i += 1
        else:
            output.append(board[j])
    #print("output:",output)
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
        row = board[9*i:9*i+9]
        r = ''
        for entry in row:
            if type(entry) == int:
                r += ' '+str(entry)+' '
            else:
                r += ' '+entry+' '
        print(r)
    print() #blank line

def apply_value(self,num,value):
    self.board[num] = value


def check_no_conflicts(inputboard):
    '''Returns False if there ARE conflicts'''
    board = populate_board(inputboard)
    for i in range(9):

        for n in range(1,4):
            if row(board,i).count(n) >2:
                #print("rowfail")
                return False
            if col(board,i).count(n) >2:
                #print("colfail")
                return False
            if quadrant(board,i).count(n) >2:
                #print("quadfail")
                return False

    for n,cell in enumerate(board):
        if cell in SHAPES:
            #print(cell)
            if not adjacent(board,n):
                #print("adjacentfail")
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

#test_adjacent()

def main():

    board1 = create_board(BOARD)
    print("numblanks:",NUMBLANKS)
    print_board(board1)

    soln = solve(list(range(1,4)),check_no_conflicts,NUMBLANKS)
    #print(soln)
    print()
    print_board(populate_board(soln))

    print("time (secs):",time.time() - starttime)

if __name__ == '__main__':
    main()