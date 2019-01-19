'''1 to 9 Puzzle 
January 18, 2019
Peter with Curtis'''

import random

NUMBERS = [1,2,3,4,5,6,7,8,9] + 7*[0]
STRNUMS = [str(n) for n in NUMBERS]

class Puzzle(object):
	def __init__(self):
		self.numList = random.sample(STRNUMS,16)


p = Puzzle()
print(p.numList)