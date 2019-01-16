'''1 to 9 puzzle #181219
January 15, 2019
with Jared'''

import random
from itertools import permutations
import time

start = time.time()

nums = [1,2,3,4,5,6,7,8,9]
'''
guess = permutations(nums,8)

count = 0
while True:
    myList = next(guess)
    count += 1
    if myList[0]*myList[1]*myList[2] != 72:
        continue
    if myList[2]*myList[4]*myList[7] != 216:
        continue
    if myList[0]*myList[3]*myList[5] != 120:
        continue
    if myList[5]*myList[6]*myList[7] != 36:
        continue
    print(myList,count)
    break
'''374479
count = 0

edges = [72,216,120,36]

for n in nums:
    divides = False
    for e in edges:
        if e % n == 0:
            divides = True
    if not divides:
        print(n,"isn't a factor")
        nums.remove(n)

#myList = sample([1,2,3,4,5,6,7,8,9],8)
while True:
    #generate a list of numbers
    myList = random.sample(nums,8)
    count += 1
    #check
    if myList[0]*myList[1]*myList[2] != 72: continue
    if myList[2]*myList[4]*myList[7] != 216: continue
    if myList[0]*myList[3]*myList[5] != 120: continue
    if myList[5]*myList[6]*myList[7] != 36: continue
    print(myList,"count:", count)
    break

print(time.time() - start)
