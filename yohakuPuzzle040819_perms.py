'''Solving today's Yohaku Puzzle posted on Twitter
https://twitter.com/YohakuPuzzle/status/1115220831339069441
April 8, 2019'''

from random import sample
from itertools import permutations
from math import sqrt
import time

start = time.time()
  
#generate list of numbers up to highest sum in puzzle, or 12
primeList = [i for i in range(1,13)]
#print(primeList)
      
rows = [15,22,9]
cols = [17,7,22]

attempts = 0

#generate list of permutations of primeList
perms = permutations(primeList,9)
#infinite loop
while True:
  #increment attempts
  attempts += 1
  if attempts % 1000000 == 0:
      print(attempts,'attempts so far.')
  #assign values to the 8 variables
  p = next(perms)
  a,b,c,d,e,f,g,h,i = p
  #print(p)
  
  #check if their sums satisfy the conditions:
  if a+b+c != rows[0]:
    continue #go back to beginning of loop and start over
  if d+e+f != rows[1]:
    continue
  if g+h+i != rows[2]:
    continue
  if a+d+g != cols[0]:
    continue
  if b+e+h != cols[1]:
    continue
  if c+f+i != cols[2]:
    continue
  #if the program has reached this point,
  #it must be the solution. Print it out:
  print(a,b,c)
  print(d,e,f)
  print(g,h,i)
  print()
  print(attempts,"attempts.")
  print("Time:", round(time.time() - start,2),"seconds.")
  break
