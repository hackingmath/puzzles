'''1to9 Puzzle
Feb 5, 2019'''

import random
import time

start_time = time.time()

#Row/column totals
#Change these for future puzzles
row1 = 8
row2 = 9
row3 = 9
row4 = 10
col1 = 9
col2 = 7
col3 = 11
col4 = 9
updiag = 13
downdiag = 23

loop_count = 0 #how many loops does it take?

while True:
    loop_count += 1
    #generate random list of 8 numbers, assign to letters
    a,b,c,d,e,f,g,h = random.sample([1,2,3,4,5,6,7,8,9],8)
    #check sums. If they don't work, start loop over
    if a + b != row1:
        continue
    if c + d != row2:
        continue
    if e + f != row3:
        continue
    if g + h != row4:
        continue
    if a + g != col1:
        continue
    if c + e != col2:
        continue
    if d + f != col3:
        continue
    if b + h != col4:
        continue
    if g + e + d + b != updiag:
        continue
    if a + c + f + h != downdiag:
        continue
    #if you've gotten to here, the list works!
    break

print(a," "," ",b)
print(" ",c,d," ")
print(" ",e,f," ")
print(g," "," ",h)

print("Number of loops:",loop_count)
print("Time:",time.time() - start_time,"seconds")
