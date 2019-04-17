'''From Yohaku Twitter post
https://twitter.com/YohakuPuzzle/status/1118482362491256832April 17, 2019
April 17, 2019
3x3 Grid Primes, Row and Column Products'''

import copy
import time
import random
from math import sqrt

starttime = time.time()

POP_N = 10000
solved = False

#from specific puzzle 04/17/19
ROWS = [65,35,12]
COLS = [44,47,21]

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
        for i in range(5):
            print(self.numList[5*i:5*i+5])
        print("Mutations:",self.mutations)
        print("Crossover:",self.crossovers)
        print("Replacements:",self.replacements)
        print()
        
def setup():
    
    size(600,600)
    fill(0)
    textSize(48)
    reset()
    
def draw():
    global cycles_without_improvement,population,record_score,best
    background(255)
    cycles_without_improvement += 1
    if cycles_without_improvement >= 50:
        reset()
    textSize(36)
    text("Error: "+str(record_score),50,50)
    printBoard(best.numList)
    textSize(18)
    text("Mutations: "+str(best.mutations),450,50)
    
    #if this is the solution
    if record_score == 0:
        saveFrame("####.png")
        elapsed = round(time.time() - starttime,1)
        println("Time: "+str(elapsed)+"seconds")
        noLoop()
        # print(best.calc_score())
        # best.print_board()
        # solved = True
        # return
    #sort the population, best score first    
    population.sort(key=Puzzle.calc_score)
    population = population[:POP_N]
    #check if it's better than the record score
    score2 = population[0].calc_score()
    if score2 < record_score:
        record_score = score2
        best = population[0]
        
        saveFrame("####.png")
        cycles_without_improvement = 0
    #mutate the best Puzzle
    for j in range(1000):
        for i in range(1,9):
            new = best.mutate(i)
            population.append(new)
        #mutate some random Puzzles
        for i in range(1,9):
            ran = random.choice(population)
            new = ran.mutate(i)
            population.append(new)
        #replace some in best puzzles
    ####            for i in range(1,9):
    ####                new = best.replace(i)
    ####                population.append(new)
        #crossover
    ####            parenta,parentb = random.sample(population,2)
    ####            child = parenta.crossover(parentb)
    ####            population.append(child)
    #add some new Puzzles
    for i in range(1000):
        population.append(Puzzle())
    '''if frameCount %100 == 0:
        saveFrame("####.png")'''

def reset():
    global cycles_without_improvement,population,record_score,best
    population = []
    cycles_without_improvement = 0
    #fill population with Puzzles
    for i in range(POP_N):
        population.append(Puzzle())
    population.sort(key=Puzzle.calc_score)
    best = population[0]#random.choice(population)
    record_score = best.calc_score()
    first = record_score
    
def printBoard(numList):
    line(440,75,440,425)
    line(100,425,440,425)
    for i in range(3):
        text(ROWS[i],475,100+125*i)
        text(COLS[i],100+125*i,475)
        for j in range(3):
            text(numList[j+3*i],100+125*j,100+125*i)
            

'''Solution:
[23, 29, 13]
[19, 11, 5]
[2, 7, 3]
Mutations: 11
Crossover: 2
Replacements: 0
'''
