'''Numoku Puzzle #19006
January 15, 2019'''

class Numoku(object):
    def __init__(self,puzList):
        self.numList = []
        #stacks the rows of the list
        for i in range(6):
            self.numList.append([])
            for j in range(6):
                self.numList[i].append(puzList[6*i+j])

    def row(self,n):
        return self.numList[n]

    def column(self,n):
        col = []
        for row in self.numList:
            col.append(row[n])
        return col

    def printout(self):
        for row in self.numList:
            print(row)
            

nums = [1,2,3,4,5,6,7,8,9]
puz = [0,8,0,2,0,0,
       0,0,9,0,0,4,
       7,0,0,0,6,0,
       0,9,0,0,0,3,
       3,0,0,6,0,0,
       0,0,2,0,5,0]

n = Numoku(puz)

print(n.numList)
