"""From Video by James Tanton 
https://youtu.be/3EmDDhBg5Gw
June 7, 2021

List of numbers between 1-24. Choose 2 
numbers as legs, find their hypotenuse. 
Remove the legs from the list, add the hypotenuse
to the list, keep pairing them up and
erasing until you get to one last number.

"""
from math import sqrt
import random

nums = [x for x in range(1,25)]

while len(nums) > 1:
    print(nums)
    print(len(nums))
    a,b = random.sample(nums,2)
    c = sqrt(a**2 + b**2)
    if c in nums:
        nums.remove(c)
    else:
        nums.append(c)
    nums.remove(a)
    nums.remove(b)

print(nums) #[70]
