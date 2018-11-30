'''1 to 9 puzzle
November 29, 2018'''

import random

def createList():
    '''Creates 36-long list, with values from
    the puzzle in question'''

    numList = [random.randint(1,9) for i in range(36)]

    #values from design

    numList[0] = 6
    numList[4] = 5
    numList[6] = 8
    numList[8] = 3
    numList[15] = 8
    numList[16] = 3
    numList[19] = 5
    numList[20] = 4
    numList[27] = 5
    numList[29] = 6
    numList[31] = 6
    numList[35] = 8

    return numList

def scoreList(myList):
    '''Scores list according to whether rows
     and cols add up to 30 and boxes add up to 45
    Lower values are better'''
    #first separate the rows so the list is stacked:
    stackedList = [[] for i in range(6)]
    counter = 0
    for i in range(6):
        for j in range(6):
            stackedList[i].append(myList[6*i+j])

    #Score the rows   
    output = 0
    for row in stackedList:
        output += abs(30 - sum(row))

    #Score the cols:
    for c in range(6):
        colsum = 0
        for r in range(6):
            colsum += stackedList[r][c]
        output += abs(30 - colsum)

    #score the boxes
    for x in range(2):
        for y in range(2):
            boxsum = 0
            boxsum += sum(stackedList[3*x][3*y:3*y+3])
            boxsum += sum(stackedList[3*x+1][3*y:3*y+3])
            boxsum += sum(stackedList[3*x+2][3*y:3*y+3])
            output += abs(45 - boxsum)
    return output
    
def mutateN(mylist):
    '''Changes a random number in the list to a random digit'''
    n1,n2 = random.sample(list(range(1,10)),2)
    index = random.randint(0,35)
    if mylist[index] != n1:
        mylist[index] = n1
    else:
        mylist[index] = n2
    return mylist

def printNumoku(mylist):
    '''Prints 6x6 grid'''
    for i,num in enumerate(mylist):
        print(num,end = ' ')
        if i % 6 == 2:
            print('|',end = ' ')
        if i % 6 == 5:
            print()
        if i == 17:
            print('-------------')

numList = createList()
theScore = scoreList(numList)
printNumoku(numList)
print("Score:",theScore)
numList2 = mutateN(numList)
printNumoku(numList2)
print("New Score:",scoreList(numList2))
