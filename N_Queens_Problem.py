'''N Queens problem using backtracking
June 29, 2019'''

import time
import random

start = time.time()

N = 10 #number of rows/cols

def stack_board(board):
    output = []
    for i in range(N):
        output.append([])
        for j in range(N):
            output[i].append(board[N * i + j])
    return output

def row(board,n):
    '''returns values in row n of board'''
    newboard = stack_board(board)
    return newboard[n]

def col(board,n):
    '''returns values in col n of stacked board'''
    newboard = stack_board(board)

    return [r[n] for r in newboard]

def diag(board,n):
    '''The diagonals start in the top left
    corner [0][0] and end with [N-1][N-1].
    Then they start in the lower left
    with [N-1][0] and end with [0][N-1]'''
    board = stack_board(board)
    output = []
    half = 2*N - 1
    for i in range(N):
        for j in range(N):
            if n < half:
                if i + j == n:
                    output.append(board[i][j])
            else:
                if i - j == half - n + N - 1:
                    output.append(board[i][j])
    return output

def print_board(solution_board):
    '''Prints from flat boardlist'''
    print()
    for i in range(N):
        for n in row(solution_board,i):
            print(n," ",end = "")
        print()
    print() #blank line

def check_no_conflicts(solution_board):
    for i in range(N):
        if row(solution_board,i).count('Q')>1 or col(solution_board,i).count('Q')>1:
            return False
    for j in range(4*N-2):
        if diag(solution_board,j).count('Q')>1: return False
    if solution_board.count(0) == 0:
        if solution_board.count("Q") != N:
            return False
    return True

def solve(values,safe_up_to,size):
    solution = [0]*size
    def extend_solution(position):
        for value in values:
            solution[position] = value
            print_board(solution)
            if safe_up_to(solution):
                if position >= size - 1 or extend_solution(position + 1):
                    return solution

            else:
                solution[position] = 0
                if value == values[-1]:
                    solution[position-1] = 0
                if position < size -1:
                    solution[position + 1] = 0
        return None
    return extend_solution(0)

print_board(solve(["Q",'.'],check_no_conflicts,N**2))
'''test_board = ['Q',0,0,0,
              0,'Q',0,0,
              0,0,'Q',0,
              0,0,0,'Q']
print_board(test_board)
for i in range(4*N-2):
    print(diag(test_board,i),diag(test_board,i).count("Q"))
print(check_no_conflicts(test_board))'''

elapsed = time.time()-start
if elapsed < 60:
    print("Time (secs):",round(elapsed,1))
else:
    mins = elapsed // 60
    secs = int(elapsed) % 60
    print("Time:",mins,"minutes,",secs,"seconds.")

