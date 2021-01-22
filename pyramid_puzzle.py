#https://artofproblemsolving.com/careers/job/4253969003_software_engineer

import time
starttime = time.time()

with open('C:/Users/Owner/Downloads/pyramid_sample_input.txt') as file:
    data = file.readlines()
    numList = [line.split() for line in data]

    pyramid = []
    target = int(numList[0][1])
    for row in numList[1:]:
        for n in row:
            pyramid.append([int(num) for num in n.split(',')])

target = 2400
pyramid = [[2],
           [4, 3],
           [3, 2, 6],
           [2, 9, 5, 2],
           [10, 5, 2, 15, 5],
           [2, 5, 4, 2, 3, 10]]

print(target)
print(pyramid)
ROWS = len(pyramid)

def solve(arr,target,product,loc):
    """Go through rows of arr and get to target number"""
    while loc[0] < len(arr)-1:
        row,col = loc[0],loc[1]
        new_product = product*arr[row+1,col]
        if target % new_product != 1:
            solve(arr,target,new_product,[row+1,col])

VALS = 'LR'

def check_no_conflicts(board,pyr,target):
    """Returns True if there are no conflicts"""
    #product is number in first row of pyramid
    product = pyr[0][0]
    r,c = 0,0
    while r < ROWS - 1:
        if board[r] == 'X': #unfinished list
            return True
        if board[r] == 'R':
            c += 1
        r += 1 #next row
        product *= pyr[r][c]
        if target % product != 0: #not divisible
            #print("not divisible",r,c)
            return False
        if r == ROWS - 1: #last row
            if target != product:
                #print("not equal",r,c)
                return False
    return True


def solve(values, safe_up_to, size):
    """Return the solution as a list of values"""
    solution = ['X'] * size

    def extend_solution(position):
        for value in values:
            solution[position] = value
            #print(solution) #uncomment to see guesses
            if safe_up_to(solution,pyramid,target):
                if position >= size - 1 or extend_solution(position + 1):
                    return solution
            else:  # backtrack
                solution[position] = 'X'
                if value == values[-1]: #if last possible value
                    solution[position - 1] = 'X' #reset previous term
                if position < size - 1: #reset next term
                    solution[position + 1] = 'X'
        return None

    return extend_solution(0)


print(solve(VALS, check_no_conflicts, ROWS-1))
print("Time(secs):", round(time.time() - starttime, 1))