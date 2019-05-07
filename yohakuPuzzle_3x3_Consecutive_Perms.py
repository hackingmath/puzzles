'''From Yohaku Twitter post
https://twitter.com/YohakuPuzzle/status/1125727584141004800
May 7, 2019'''

import time
import random
from math import sqrt
from itertools import permutations

start_time = time.time()

solved = False

#from specific puzzle 05/07/19
ROWS = [108,400,462]
COLS = [330,120,504]

def checkRows(numList):
    for i in range(3):
        row = numList[i*3:(i+1)*3]
        if row[0]*row[1]*row[2] != ROWS[i]:
            #print("Row",i,"doesn't work.")
            return False
    return True
        
def checkCols(numList):
    for i in range(3):
        col = int(numList[i % 3] * numList[i % 3 + 3]) * \
                  int(numList[i % 3+ 6])
        if col != COLS[i]:
            #print("Column",i,"doesn't work.")
            return False
    return True

attempts = 0
start_num = -3 #start consecutive nums here

while not solved:
    #choose starting point for consecutive nums
    print("Start_num:",start_num)
    #create list of consecutive numbers
    numList = list(range(start_num,start_num+9))
    #take permutations of that list
    perms = permutations(numList)

    while True and not solved:
        try:
            #generate the next permutation
            s = next(perms)
            #increment attempts              
            attempts +=1
            #print out attempts occasionally
            if attempts % 1000000 == 0:
                print("Attempts:",attempts)
            #check row and column products
            if not checkRows(s):
                continue
            if not checkCols(s):
                continue
            #If it gets to this point, it's solved
            solved = True
            break
        #if it gets to the end of the permutations
        #of that list, start at the next number
        except StopIteration:
            start_num+=1
            break

print()
for i in range(3):
    print(s[i*3:(i+1)*3])

print()
print("Total Attempts:",attempts)
print("Time:",round(time.time()-start_time,1),"secs.")
