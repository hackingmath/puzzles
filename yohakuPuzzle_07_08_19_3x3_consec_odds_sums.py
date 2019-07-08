'''Solving Yohaku Puzzle
https://twitter.com/YohakuPuzzle/status/1148212796536041472
3x3 grid, consecutive odd numbers, sums of rows/cols given
July 8, 2019'''

import time
import random
from itertools import permutations

start = time.time()

ROWS = [33,47,19]
COLS = [39,41,19]

starting_num = 3

NUMS = range(starting_num,starting_num+18,2)

p = permutations(NUMS,9)

while True:
    a,b,c,d,e,f,g,h,i = next(p)
    if a + b + c != ROWS[0]:
        continue
    if d + e + f != ROWS[1]:
        continue
    if g + h + i != ROWS[2]:
        continue
    if a + d + g != COLS[0]:
        continue
    if b + e + h != COLS[1]:
        continue
    if f + i + c != COLS[2]:
        continue
    break

print('{:2d} {:2d} {:2d}'.format(a,b,c))
print('{:2d} {:2d} {:2d}'.format(d,e,f))
print('{:2d} {:2d} {:2d}'.format(g,h,i))
print("Time:",round(time.time()-start,1),"seconds")
