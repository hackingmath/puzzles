'''Solving today's Yohaku Puzzle posted on Twitter
https://twitter.com/1to9puzzle/status/1123345947755311105
May 1, 2019'''

import random
import time

start = time.time()

NUMS = [1,2,3,4,5,6,7,8,9]

products = [90,90,72,24]

attempts = 0

#infinite loop
while True:
  #increment attempts
  attempts += 1
  if attempts % 100000 == 0:
      print(attempts,'attempts so far.')
  #assign values to the 9 variables
  a,b,c,d,f,g,h,i = random.sample(NUMS,8)
  
  #check if their sums satisfy the conditions:
  if a*b*c != products[0]:
    continue #go back to beginning of loop and start over
  if c*f*i != products[1]:
    continue
  if g*h*i != products[2]:
    continue
  if a*d*g != products[3]:
    continue
  
  #if the program has reached this point,
  #it must be the solution. Print it out:
  print()
  print(a,b,c)
  print(d," ",f)
  print(g,h,i)
  print()
  print(attempts,"attempts.")
  print("Time:", round(time.time() - start,2),"seconds.")
  break
