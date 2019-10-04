"""DIY Matrix Operations
Sept. 26, 2019"""

import random

class Matrix(object):
    def __init__(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.data = []

        for r in range(self.rows):
            self.data.append([])
            for c in range(self.cols):
                self.data[r].append(0)

    def randomize(self):
        """Assigns random value between 0 and 1"""
        for r, row in enumerate(self.data):
            for i in range(self.cols):
                self.data[r][i] = random.random()


def fromArray(arr):
    m = Matrix(len(arr),1)
    for i,val in enumerate(arr):
        m.data[i][0] = val
    return m

def add(A,B):
    """Add A matrix to B"""
    output = []
    for i in range(len(A)):
        output.append([])
        for j in range(len(A[0])):
            output[i].append(A[i][j] + B[i][j])
    return output

def transpose(A):
    '''Transposes matrix'''

    output = []
    m = len(A)
    n = len(A[0])
    # create an n x m matrix
    for i in range(n):
        output.append([])
    for j in range(m):
    # replace a[i][j] with a[j][i]
        output[i].append(A[j][i])
    return output


def multiply(A,B):
    '''Returns the product of
    matrix a and matrix b'''

    newmatrix = []
    for i in range(len(A)):
        row = []
        #for every column in b
        for j in range(B[0]):
            sum1 = 0
            #for every element in the column
            for k in range(B):
                sum1 += A[i][k]*B[k][j]
            row.append(sum1)
        newmatrix.append(row)
    return newmatrix

def multiply_scalar(self,b):
    """Returns self's data multiplied by
    a number b."""
    newmatrix = []
    for i in range(self.rows):
        row = [b * self.data[i][j] for j in range(self.cols)]
        newmatrix.append(row)

    self.data = newmatrix

def map(A,func):
    """Returns self's data with a function applied."""
    newmatrix = []
    for i in range(A):
        row = []
        for j in range(len(A[0])):
            row.append(func(A[i][j]))
        newmatrix.append(row)

    return newmatrix

def print_matrix(A):
    for row in A:
        print(row)


def g(x):
    return 2*x + 5

if __name__ == '__main__':
    m2 = Matrix(2,2)
    m3 = Matrix(2,2)
    #m2.randomize()
    m2 = 5
    m3.randomize()
    #print(type(m2))
    #m2.data = [[1,2],[3,4]]
    m3.data = [[5,6],[-2,-1]]
    #print(m2.data)
    #print(m3.data)
    m3.map(g)
    m3.print_matrix()
