'''1 to 9 puzzle
November 29, 2018'''

import random

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

printNumoku(numList)
