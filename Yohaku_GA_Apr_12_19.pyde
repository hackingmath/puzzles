'''From Yohaku Twitter post
https://twitter.com/YohakuPuzzle/status/1116669881380769792
16 consecutive numbers, sums of rows/cols
Corners have to be triangle nums'''

import copy
import time
import random
from math import sqrt

starttime = time.time()

POP_N = 10000
solved = False

#generate list of triangle numbers to check
triangle_nums = [int(0.5*i*(i+1)) for i in range(1,7)]
#print(triangle_list)

#from specific puzzle 04/12/19
ROWS = [38,30,49,19]
COLS = [10,46,41,39]

class Puzzle(object):
    def __init__(self):
        #Generates a list of consecutive numbers
        start_num = random.randint(1,15) #random starting num
        self.numList = list(range(start_num,start_num+16))
        self.score = 0
        self.mutations = 0
        self.crossovers = 0
        self.replacements = 0

    def calc_score(self):
        self.score = 0
        for i in range(4):
            row = self.numList[i*4:(i+1)*4]
            #print(row)
            self.score += abs(sum(row)-ROWS[i])
            col = int(self.numList[i % 4] + self.numList[i % 4 + 4]) + \
                  int(self.numList[i % 4 + 8]) + int(self.numList[i % 4 + 12])
            #print(col)
            self.score += abs(col-COLS[i])
        #add penalty for corners not being triangular numbers
        corners = [self.numList[0], self.numList[3],
                   self.numList[12],self.numList[15]]
        for c in corners:
            if c not in triangle_nums:
                self.score += 1
        return self.score

    def mutate(self,num):
        '''Swaps num numbers in the numList'''
        indices = random.sample(list(range(16)),num)
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
            if len(notinlist) > 0:
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
        for i in range(4):
            print(self.numList[4*i:4*i+4])
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
    if cycles_without_improvement >= 100:
        reset()
    
    text("Score: "+str(record_score),50,50)
    printBoard(best.numList)
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
    for i in range(500):
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

    for i in range(4):
        for j in range(4):
            text(numList[j+4*i],100+100*j,150+100*i)
        

'''Solution:

'''
