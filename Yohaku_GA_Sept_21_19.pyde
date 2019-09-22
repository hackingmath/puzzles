'''From Yohaku Twitter post
https://twitter.com/YohakuPuzzle/status/1175398323634786304
25 consecutive numbers, sums of rows/cols
Center 3x3 grid has to be prime nums'''

import copy
import time
import random
from math import sqrt

starttime = time.time()

POP_N = 10000
solved = False

#list of prime numbers to check
PRIMES = [2,3,5,7,11,13,17,19,23]
centers = [6,7,8,11,12,13,16,17,18]
notcenters = [n for n in range(25) if n not in centers]
#print(triangle_list)

#from specific puzzle 09/21/19
ROWS = [60,21,85,61,48]
COLS = [69,96,50,14,46]

start_num = int((2*sum(ROWS)/25 - 24)/2)

NUMS = [i for i in range(start_num,start_num+25)]

class Puzzle(object):
    def __init__(self):
        #Generates a list of consecutive numbers
        self.numList = list(range(start_num,start_num+25))
        self.score = 0
        self.rowscores = list()
        self.colscores = list()
        self.mutations = 0
        self.crossovers = 0
        self.replacements = 0

    def calc_score(self):
        self.findprimes() #get primes in middle first
        self.score = 0
        self.rowscores = list()
        self.colscores = list()
        for i in range(5):
            row = self.numList[i*5:(i+1)*5]
            #print(row)
            rowscore = abs(sum(row)-ROWS[i])
            self.score += rowscore
            self.rowscores.append(rowscore)
            col = int(self.numList[i % 5] + self.numList[i % 5 + 5]) + \
                  int(self.numList[i % 5 + 10]) + int(self.numList[i % 5 + 15]) + \
                  int(self.numList[i % 5 + 20])
            #print(col)
            colscore = abs(col-COLS[i])
            self.colscores.append(colscore)
            self.score += colscore
        
        return self.score

    def mutate(self,num):
        '''Swaps num numbers in the numList'''
        indices = random.sample(list(range(25)),num)
        child = Puzzle()
        child.mutations = self.mutations + 1
        child.crossovers = self.crossovers
        child.numList = self.numList[::]
        for i in range(num-1):
            child.numList[indices[i]],child.numList[indices[(i+1)%num]] = \
            child.numList[indices[(i+1)%num]], child.numList[indices[i]]
        return child

    def replace(self,n):
        '''Replaces n numbers in numList with other numbers'''
        child = Puzzle()
        child.crossovers = self.crossovers
        child.mutations = self.mutations
        child.replacements = self.replacements + 1
        child.numList = self.numList[::]
        notinlist = [x for x in range(start_num,start_num+25) if x not in child.numList]
        indices = random.sample(list(range(25)),n)
        for ind in indices:
            if len(notinlist) > 0:
              num = random.choice(notinlist)
              child.numList[ind] = num
              notinlist.remove(num)
        return child
    
    def findprimes(self):
        """non-primes in prime spots find primes in non-prime spots and swap"""
        for spot in centers:
            if self.numList[spot] not in PRIMES:
                for spot2 in notcenters:
                    if self.numList[spot2] in PRIMES:
                        self.numList[spot],self.numList[spot2] = \
                        self.numList[spot2],self.numList[spot]
            

    def crossover(self,partner):
        '''Splice together nums with partner's nums'''
        child = Puzzle()
        child.crossovers = self.crossovers + partner.crossovers + 1
        child.mutations = self.mutations + partner.mutations
        #randomly choose slice point
        index = random.randint(1,20)
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
            print(self.numList[5*i:5*i+5])
        println("Mutations:",self.mutations)
        println("Crossover:",self.crossovers)
        println("Replacements:",self.replacements)
        println()
        
    def printBoard(self):

        for i in range(5):
            for j in range(5):
                fill(0)
                text(self.numList[j+5*i],50+75*j,100+75*i)
                fill(255,0,0) #red
                text(self.rowscores[i],50 + 75*5, 100+75*i)
                text(self.colscores[j],50+75*j, 100+75*5)
        println("Mutations:"+str(self.mutations))
        println("Crossover:"+str(self.crossovers))
        println("Replacements:"+str(self.replacements))
        println("")
        
def setup():
    
    size(600,600)
    fill(0)
    textSize(36)
    reset()
    #println("Startnum:"+str(start_num))
    #println(notcenters)
    
def draw():
    global cycles_without_improvement,population,record_score,best
    background(255)
    cycles_without_improvement += 1
    if cycles_without_improvement >= 20:
        reset()
    fill(255,0,0) #red
    text("Error: "+str(record_score),30,30)
    best.printBoard()
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
        
        #saveFrame("####.png")
        cycles_without_improvement = 0
    #mutate the best Puzzle
    for j in range(1000):
        for i in range(1,10):
            new = best.mutate(i)
            population.append(new)
        #mutate some random Puzzles
        for i in range(1,20):
            ran = random.choice(population)
            new = ran.mutate(i)
            population.append(new)
        #replace some in best puzzles
        # for i in range(1,20):
        #     new = best.replace(i)
        #     population.append(new)
    for i in range(500):
        #crossover
        parenta,parentb = random.sample(population[:20],2)
        child = parenta.crossover(parentb)
        population.append(child)
    #add some new Puzzles
    '''for i in range(500):
        population.append(Puzzle())'''
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
    
'''Solution:
 16 22 12  0 10
  4 11  2  3  1
 20 23 17  7 18
 15 19 13  5  9
 14 21  6 -1  8 
 
 10 mutations
 time: 1934 seconds (32 minutes)
'''
