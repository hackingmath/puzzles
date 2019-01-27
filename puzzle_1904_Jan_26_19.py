'''Solving a 1 to 9 puzzle
https://twitter.com/1to9puzzle
January 26, 2019'''

import random
from itertools import permutations, product

class Square(object):
    def __init__(self,numList):
        self.numList = numList

    def add(self, B):
        '''adds matrices A and B and returns a list
        of all possible differences between given numbers'''
        nums = list(range(1, 10))
        # list for choices of numbers
        terms = []
        # add and subtract all pairs
        for i in range(9):
            this_term = []
            term = self.numList[i] + B[i]
            if term in nums:
                this_term.append(term)
            term = self.numList[i] - B[i]
            if term in nums:
                this_term.append(term)
            # put all choices in terms list
            terms.append(this_term)
        final_output = []
        output = []
        choices = []
        for i, t in enumerate(terms):
            if len(t) == 0:
                pass  # same number in s1 and diff
            if len(t) == 1:
                output.append(t[0])
            else:
                # record which terms have choices
                choices.append(i)
                output.append(t)
        data = product([0, 1], repeat=len(choices))
        '''This produces (0,0,0),(0,0,1) and so on'''
        while True:
            try:
                p = next(data)
                output_list = []  # one list
                j = 0
                for i, t in enumerate(output):
                    if i in choices:
                        # insert the choices
                        output_list.append(t[p[j]])
                        j += 1
                    else:
                        output_list.append(t)

                if len(output_list) != 9:
                    continue
                wrong = False
                for n in output_list:
                    if output_list.count(n) > 1:
                        wrong = True
                        break
                if wrong:
                    continue
                final_output.append(output_list)

            except:
                break

        # print(final_output)
        return final_output

class Puzzle(object):
    def __init__(self,dark_squares,given):
        self.dark = dark_squares
        self.given = given
        #squares
        self.s1 = Square([0 for i in range(9)])
        self.s1.numList[4] = self.given[0]
        self.s2 = Square([0 for i in range(9)])
        self.s2.numList[4] = self.given[1]
        self.s3 = Square([0 for i in range(9)])
        self.s3.numList[4] = self.given[2]
        self.s4 = Square([0 for i in range(9)])
        self.s4.numList[4] = self.given[3]
        self.board = []

        self.solutions = []
        self.s2_list = []
        self.s3_list = []
        self.s4_list = []

    def printBoard(self):
        '''Prints out board for inspection'''
        # put together in a board
        self.board = [self.s1.numList[:3] + self.s2.numList[:3],
                      self.s1.numList[3:6] + self.s2.numList[3:6],
                      self.s1.numList[6:] + self.s2.numList[6:],
                      self.s4.numList[:3] + self.s3.numList[:3],
                      self.s4.numList[3:6] + self.s3.numList[3:6],
                      self.s4.numList[6:] + self.s3.numList[6:]]
        for row in self.board:
            for c in row:
                print(c,end = ',')
            print()
        print()

    def solve(self):
        wrong = False #we're not wrong yet!

        # Generate a starting square
        g = permutations([1, 2, 4, 5, 6, 7, 8, 9])
        count_right = 0
        while True:
            # for i in range(10):
            try:
                # generate list of numbers
                self.s1 = Square(list(next(g)))
                # insert 3 in middle square
                self.s1.numList = self.s1.numList[:4] + [self.given[0]] + self.s1.numList[4:]
                # add s1 and the first difference list
                # print("s1:", self.s1)
                # print("d0:", self.dark[0])
                s2_list = self.s1.add(self.dark[0])
                for s2 in s2_list:

                    # print("s2:",s2)
                    if not s2:
                        continue
                    if check_rows(self.s1.numList, s2):
                        self.solutions.append([Square(self.s1.numList), Square(s2)])
            except StopIteration:
                break
        #solution pairs for s1 and s2 are in the self.solutions list. There were 64 solutions so far
        print("solutions:", len(self.solutions))
        for solution in self.solutions:
            s2 = solution[1]

            s3_list = s2.add(dark[1])
            #s3 = Square(s3_list)
            # print(s3_list)
            for s3 in s3_list:
                if not s3:
                    continue
                if s3[4] != 9:
                    continue
                # print("s3:", s3)
                # for n in s3:
                #     if s3.count(n) > 1:
                #         wrong = True
                #         break
                if wrong:
                    continue
                s3_square = Square(s3)
                solution.append(s3_square)
        #There's only 1 solution left
        for solution in self.solutions:
            if len(solution) == 3:
                self.s1 = solution[0]
                self.s2 = solution[1]
                self.s3 = solution[2]
                #self.printBoard()

        s4_list = self.s3.add(dark[2])

        for s4 in s4_list:
            if not s4:
                continue
            if s4[4] != 4:
                continue

            #print(s4)
            self.s4 = Square(s4)
            solution.append(self.s4)
        self.printBoard()



# dark squares
dark = [[3, 3, 2,
         3, 4, 4,
         3, 2, 6],
        [5, 2, 5, 2, 2, 5, 7, 3, 1],
        [6, 4, 1, 4, 5, 7, 5, 4, 4],
        [4, 1, 2, 1, 1, 6, 1, 1, 3]]

given = [3, 7, 9, 4]

def check_rows(A,B):
    '''Checks two flat lists for repeats in rows
    Returns False if there's a repeat'''
    stacked_list = []
    for i in range(3):
        #stacked_list.append([])
        stacked_list.append(A[3*i:3*(i+1)]+B[3*i:3*(i+1)])
    for row in stacked_list:
        for num in row:
            if row.count(num) > 1:
                return False
    return True

### Program starts here ###

p = Puzzle(dark,given)
p.solve()
p.printBoard()
