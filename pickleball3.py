"""Pickleball Tournament
12 teams 6 courts, 11 rounds
2 pickleball courts
1 dink court
1 left handed court
1 swim noodle court
1 one-bounce court

Each team should play 3-4 rounds PB
 1 or 2 rounds each of the other games"""

import random
from itertools import combinations

import time

start = time.time()

num_teams = 12
n_rounds = 11
n_courts = 6

def populate_board(boardlist):
    '''Puts values into pairs for games,
    rows for boards and columns for rounds'''
    #print("boardlist",boardlist)
    output = []
    #print("board:",board)
    '''for i in range(0,int(len(boardlist)),2):
        game = [boardlist[i],boardlist[i+1]]
        games.append(game)'''


    for j in range(n_rounds):
        round = boardlist[n_courts*j:n_courts*(j+1)]
        output.append(round)

    return output

def print_board(board):
    for r,round in enumerate(board):
        #for g,game in enumerate(round):
        #print(f'{board[r][g]}' for g in range(len(round)))
        print(f"  Round {r+1}  ",end="")
    print()
    for i in range(n_courts):
        row = [round[i] for round in board]
        for g,game in enumerate(row):

            print(" {:2d} vs {:2d}".format(game[0]+1,game[1]+1),end = '  ')
            if g == n_rounds-1: print()
    print()

def check_round(boardlist):
    """Checks for repeats in rounds in boardlist
    broken up into rounds"""
    b = populate_board(boardlist)
    for round in b:
        nums = []
        for game in round:
            n = game[0]
            if n != -1 and n in nums:
                return False
            else:
                nums.append(n)
            n = game[1]
            if n != -1 and n in nums:
                return False
            else:
                nums.append(n)
    return True

def check_rematch(boardlist):
    """Makes sure a game is not repeated"""
    for game in boardlist:
        if game == (-1,-1): continue
        if boardlist.count(game) > 1:
            return False
    return True

def check_rows(boardlist):
    """Teams should only be in courts 0-3 at most twice"""
    b = populate_board(boardlist)
    #print("Checking Rows")
    for c in range(n_courts-2):
        games = [b[r][c] for r in range(n_rounds)]
        nums = []
        for g in games:
            nums.append(g[0])
            nums.append(g[1])
        for i in range(num_teams):
            if nums.count(i) > 2:
                #print(b)
                #print("court:",c,"num:",i)
                return False
    return True


def check_no_conflicts(boardlist):
    if not check_round(boardlist):
        return False
    if not check_rematch(boardlist):
        return False
    if not check_rows(boardlist):
        return False
    return True

def tally(solution):
    for t in range(12):
        output = []
        for c in range(n_courts):
            games = [solution[r][c] for r in range(n_rounds)]
            nums = []
            for g in games:
                nums.append(g[0])
                nums.append(g[1])
            output.append(nums.count(t))
        print(f"Team {t+1}: {output}")


def solve(values, safe_up_to, size):
    global solution
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
    solution = [(-1,-1)]*size
    available_values = list(values)

    def extend_solution(position):
        global solution
        for value in values:
            if value in solution:
                continue
            solution[position] = value
            #print(solution)
            #save_board(solution)
            #print_board(populate_board(solution))
            if safe_up_to(solution):
                #solution = solution2
                #available_values.remove(value)
                if position >= size-1 or extend_solution(position+1):
                    return solution
            else:
                solution[position] = (-1,-1)
                '''if value == values[-1]:
                    solution[position-1] = (-1,-1)'''
                if position < size - 1:
                    solution[position + 1] = (-1,-1)

        return None

    return extend_solution(0)

p = random.sample(list(combinations(range(num_teams),2)),66)
#print(p)
soln = populate_board(solve(p,check_no_conflicts,66))
print_board(soln)
tally(soln)

print(f'Time: {round(time.time()-start,1)}')