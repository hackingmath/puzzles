'''From Yohaku Twitter post
https://twitter.com/YohakuPuzzle/status/1123571046303522816
May 1, 2019'''

import time
import random
from math import sqrt

starttime = time.time()

#from specific puzzle 05/01/19
ROWS = [59,28,19]
COLS = [18,35,53]

POP_N = 2000
solved = False

def isPrime(num):
  '''Returns True if num is Prime'''
  if num == 2: return True
  if num % 2 == 0: return False
  for i in range(3,int(sqrt(num))+1,2):
    if num % i == 0:
      return False
  return True
  
#generate list of primes up to highest sum in puzzle
NUMBERS = [i for i in range(2,73) if isPrime(i)]

class Puzzle(object):
    def __init__(self):
        self.numList = random.sample(NUMBERS,9)
        self.score = 0
        self.mutations = 0
        self.crossovers = 0
        self.replacements = 0

    def calc_score(self):
        self.score = 0
        for i in range(3):
            row = self.numList[i*3:(i+1)*3]
            #print(row)
            self.score += abs(sum(row)-ROWS[i])
            col = int(self.numList[i % 3] + self.numList[i % 3 + 3]) + \
                  int(self.numList[i % 3 + 6])
            #print(col)
            self.score += abs(col-COLS[i])
        return self.score

    def mutate(self,num):
        '''Swaps num numbers in the numList'''
        indices = random.sample(list(range(9)),num)
        child = Puzzle()
        child.mutations = self.mutations + 1
        child.crossovers = self.crossovers
        child.numList = self.numList[::]
        for i in range(num-1):
            child.numList[indices[i]],child.numList[indices[(i+1)%num]] = \
            child.numList[indices[(i+1)%num]], child.numList[indices[i]]
        return child

    def replace(self,n):
        '''Replaces n numbers in numList with other primes'''
        child = Puzzle()
        child.crossovers = self.crossovers
        child.mutations = self.mutations
        child.replacements = self.replacements + 1
        child.numList = self.numList[::]
        notinlist = [x for x in NUMBERS if x not in child.numList]
        indices = random.sample(list(range(0,9)),n)
        for ind in indices:
            num = random.choice(notinlist)
            child.numList[ind] = num
            notinlist.remove(num)
        return child

    def crossover(self,partner):
        '''Splice together nums with partner's nums'''
        child = Puzzle()
        child.crossovers = self.crossovers + partner.crossovers + 1
        child.mutations = self.mutations + partner.mutations
        #randomly choose slice point
        index = random.randint(1,7)
        #add numbers up to slice point
        child.numList = self.numList[:index]
        #half the time reverse them
        if random.random()<0.5:
            child.numList = child.numList[::-1]
        #list of numbers not in the slice
        notinslice = [x for x in partner.numList if x not in child.numList]
        #add the numbers not in the slice
        child.numList += notinslice
        return child

    def print_board(self):
        #board = []
        for i in range(3):
            print(self.numList[3*i:3*i+3])
        print("Mutations:",self.mutations)
        print("Crossover:",self.crossovers)
        print("Replacements:",self.replacements)
        print()

def main():
    global solved
    population = []
    cycles_without_improvement = 0
    #fill population with Puzzles
    for i in range(POP_N):
        population.append(Puzzle())

    best = random.choice(population)
    record_score = best.calc_score()
    first = record_score

    while not solved:
        cycles_without_improvement += 1
        if cycles_without_improvement >= 10:
            main()
        if i % 500 == 0:
            print("Cycles:",i)
        #best.print_board()
        score1 = best.calc_score()
        if record_score == 0:
            print(best.calc_score())
            best.print_board()
            solved = True
            return#break
            
        population.sort(key=Puzzle.calc_score)
        #scores = [p.calc_score() for p in population]
        #print(scores)
        #population = population[::-1]
        population = population[:POP_N]
        score2 = population[0].calc_score()
        if score2 < record_score:
            record_score = score2
            best = population[0]
            print("Record:",record_score)
            best.print_board()
            cycles_without_improvement = 0
        #mutate the best Puzzle
        for j in range(2000):
            for i in range(2,10):
                new = best.mutate(i)
                population.append(new)
            #mutate some random Puzzles
            for i in range(2,10):
                ran = random.choice(population)
                new = ran.mutate(i)
                population.append(new)
            #replace some in best puzzles
            for i in range(2,7):
                new = best.replace(i)
                population.append(new)
            #crossover
            parenta,parentb = random.sample(population,2)
            child = parenta.crossover(parentb)
            population.append(child)
        #add some new Puzzles
        for i in range(500):
            population.append(Puzzle())
        

main()

#best.print_board()
#print(record_score)
elapsed = round(time.time() - starttime,1)
print("Time:",elapsed,"seconds")

'''Solution:

'''
