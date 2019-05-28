"""Solving yohaku puzzle
https://twitter.com/YohakuPuzzle/status/1133342332865196032
3x3 grid factors
May 28, 2019"""

import random

ROWS = [36,120,528]
COLS = [220,16,648]

def common_factors(r,c):
    output = []
    rfacts = factors(ROWS[r])
    cfacts = factors(COLS[c])
    for r in rfacts:
        if r in cfacts:
            output.append(r)
    return output

def factors(num):
    '''Returns a list of the factors of num'''
    factorList = []
    for i in range(1,num+1):
        if num % i == 0:
            factorList.append(i)
    return factorList

def choose_factors():
    output = []
    for r in range(3):
        for c in range(3):
            x = random.choice(common_factors(r,c))
            while x in output:
                x = random.choice(common_factors(r,c))

            output.append(x)
    return output

while True:
    f = choose_factors()
    #print(f)
    if f[0] * f[1] * f[2] != ROWS[0]:
        continue
    if f[3] * f[4] * f[5] != ROWS[1]:
        continue
    if f[6] * f[7] * f[8] != ROWS[2]:
        continue
    if f[0] * f[3] * f[6] != COLS[0]:
        continue
    if f[1] * f[4] * f[7] != COLS[1]:
        continue
    if f[2] * f[5] * f[8] != COLS[2]:
        continue
    print("Solution:")
    print(" {} {} {}".format(f[0],f[1],f[2]))
    print(" {} {} {}".format(f[3],f[4],f[5]))
    print(" {} {} {}".format(f[6],f[7],f[8]))
    print()
