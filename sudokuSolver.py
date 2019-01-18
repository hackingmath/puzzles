'''From Youtube channel 0612 TV w/ NERDfirst
https://www.youtube.com/watch?v=y1ahOBeyM40
January 17, 2019'''

import copy
import time

start = time.time()

hard = '.........5.3.67...9..3421.......4.....1...72...2.1.....3......9.8.1..2.....75.8.6'
expert = '....7..6....185..945.9........8...1.62.........3.....7...4.6...3.........48.5.19.'
evil = '85..7.4...7.2......6...9...9...6....3.8...7.1....2...5...8...2......1.9...7.3..58'
easy1 = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
easy2= '6..874.1...9.36......19.8..7946.......1.894.....41..69.7..5..9..539.76..9.2.61.47'
#board = []
total = 0

def printBoard(board):
    #global board
    for row in board:
        print(row)

def solve(b):
    global total #board,total
    try:
        fillAllObvious(b)
    except:
        return False

    if isComplete(b):
        return True
    i,j = 0,0
    #look for blank squares
    for rowIdx,row in enumerate(b):
        for colIdx,col in enumerate(row):
            if col != '.':
                continue
            else:
                i,j = rowIdx,colIdx
                
    #get possibilities for that square
    possibilities = getPossibilities(b,i,j)
    for value in possibilities:
        #save the board before changing
        snapshot = copy.deepcopy(b)
        #place the value in that square
        b[i][j] = value
        #solve with that value
        result = solve(b)
        #if it solves it, we're done
        if result:
            total += int(b[0][0])+int(b[0][1])+int(b[0][2])
            return True
        #otherwise, return to saved board
        else:
            b = copy.deepcopy(snapshot)
    return False

def fillAllObvious(board):
    #if there are any obvious moves, fill them
    #global board
    while True:
        somethingChanged = False
        #go through all squares, filling if you can
        #if there are no changes, return
        for i in range(9):
            for j in range(9):
                possibilities = getPossibilities(board,i,j)
                #no possibilities for that square
                if possibilities == False:
                    continue
                if len(possibilities) == 0:
                    raise RuntimeError("No Moves Left")
                #if there's only one possibility, fill it
                if len(possibilities) == 1:
                    board[i][j] = possibilities[0]
                    somethingChanged = True
        if not somethingChanged:
            return

def getPossibilities(board,i,j):
    #global board
    #if square isn't empty, no possibilities
    if board[i][j] != '.':
        return False
    possibilities = {str(n) for n in range(1,10)}
    #take away values in row
    for val in board[i]:
        possibilities -= set(val)
    #take away values in column
    for idx in range(9):
        possibilities -= set(board[idx][j])
    #take away values in block
    iStart = (i // 3) * 3
    jStart = (j // 3) * 3

    block = board[iStart:iStart + 3]
    for idx, row in enumerate(block):
        block[idx] = row[jStart:jStart+3]

    for row in block:
        for col in row:
            possibilities -= set(col)

    return list(possibilities)

def isComplete(board):
    #global board
    for row in board:
        for col in row:
            if col == '.':
                return False
    return True

def displayBoard(board):
    '''displays Sudoku board'''
    sz = 50
    for r,row in enumerate(board):
        for c,col in enumerate(row):
            y,x = r*sz+sz/2.0, c*sz+sz/2.0
            noFill()
            strokeWeight(1)
            rect(x,y,sz,sz)
            fill(0)
            text(col,x-sz/6.0,y+sz/6.0)
    strokeWeight(2)
    line(3*sz,0,3*sz,9*sz)
    line(6*sz,0,6*sz,9*sz)
    line(0,3*sz,9*sz,3*sz)
    line(0,6*sz,9*sz,6*sz)

def main():
    #global board
    with open('p096_sudoku.txt','r') as f:
        data = f.read().split()
        print(data[:10]) #list of strings
        total = 0
        #this many games
        for i in range(2):
            strboard = ''
            for j in range(2,11):
                strboard += data[11*i+j]
            #printBoard(strboard)
            #strboard = sum(strboard)
            
            board = []
            for i in range(9):
                board.append([])
                for j in range(9):
                    num = strboard[9*i+j]
                    if num == '0':
                        board[i].append('.')
                    else:
                        board[i].append(num)
                    
            printBoard(board)
            
        
            solve(board)
            #displayBoard(board)
            printBoard(board)
            print("total",total)
            #elapsed = time.time() - start
            #print(elapsed)'''

if __name__ == '__main__':
    main()
