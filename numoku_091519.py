"""1 to 9 Numoku Puzzle
https://twitter.com/1to9puzzle/status/1162035008749445120
August 15, 2019"""

import time
import random

start = time.time()

BOARD = '.1..4.4....6..61....94..8....7.4..8.'

def create_board(board):

    output = []
    for n in board:
        if n != '.':
            term = int(n)
        else:
            term = 'X'
        output.append(term)
    return output

def populate_board(boardlist):
    """Populates board with new values to prevent overwriting
    hard values"""
    output = []
    board = create_board(BOARD)
    #print("Board:",board)
    i = 0
    for j in range(36):
        if board[j] == 'X':
            output.append(boardlist[i]) #solution board
            i += 1
        else:
            output.append(board[j]) #hard-coded board

    return output

def print_board(board):
    """Makes the board pretty"""
    print("{} {} {} | {} {} {}".format(board[0],board[1],board[2],board[3],board[4],board[5]))
    print("{} {} {} | {} {} {}".format(board[6], board[7], board[8], board[9], board[10], board[11]))
    print("{} {} {} | {} {} {}".format(board[12], board[13], board[14], board[15], board[16], board[17]))
    print("------|------")
    print("{} {} {} | {} {} {}".format(board[18], board[19], board[20], board[21], board[22], board[23]))
    print("{} {} {} | {} {} {}".format(board[24], board[25], board[26], board[27], board[28], board[29]))
    print("{} {} {} | {} {} {}".format(board[30], board[31], board[32], board[33], board[34], board[35]))
    print()

def row(board,n):
    """Returns values in row n of board"""
    return board[6*n:6*n+6]

def col(board,n):
    """Returns values in column n of board"""
    output = []
    for j in range(6):
        output.append(board[6*j + n])
    return output

def quadrant(board,n):
    """puts values in each quadrant into lists"""
    quadrants = []
    for j in [0,1,6,7]:
        block = []
        for k in range(3):
            block.append(board[6*k+3*j:6*k+3*j+3])
        quad = []
        for thing in block:
            for t in thing:
                quad.append(t)
        quadrants.append(quad)
    return quadrants[n]

def repeat(mylist):
    """Returns True if there is a repeat in mylist"""
    for n in mylist:
        if n != 'X':
            if mylist.count(n) > 1:
                return True
    return False

def check_no_conflicts(solutionboard):
    """Returns False if there ARE conflicts"""
    board = populate_board(solutionboard)
    #print_board(board)
    for i in range(6):
        thisrow = row(board,i)
        if repeat(thisrow):
            return False
        if thisrow.count('X') == 0 and sum(thisrow) != 30:
            return False
        thiscol = col(board,i)
        if repeat(thiscol):
            return False
        if thiscol.count('X') == 0 and sum(thiscol) != 30:
            return False

    for j in range(4):
        thisquad = quadrant(board,j)
        if repeat(thisquad):
            return False
    return True


def solve(values,safe_up_to, size):
    """Finds a solution via backtracking"""
    solution = ['X']*size
    #print("size:",size)
    def extend_solution(position):
        for value in values:
            solution[position] = value
            #print_board(solution)
            if safe_up_to(solution):
                if position >= size -1 or extend_solution(position + 1):
                    return solution
            else:
                solution[position] = 'X'
                if value == values[-1]:
                    solution[position - 1] = 'X'
                if position < size - 1:
                    solution[position + 1] = 'X'
        return None

    return extend_solution(0)

# def main():
#     global NUMBLANKS
board1 = create_board(BOARD)
print()
print("Solution:")
print()
#     #board2 = populate_board(board1)
print_board(populate_board(solve(range(1,10),check_no_conflicts,BOARD.count('.'))))

# board = [random.choice(range(1,10)) for i in range(36)]
#print_board(board2)
# print(check_no_conflicts(board))

print("Time:",round(time.time() - start,1))

# if __name__ == '__main__':
#     main()