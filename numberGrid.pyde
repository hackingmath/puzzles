'''solving 1 to 9's Number puzzle using
Maze Generator idea from Shiffman.
https://twitter.com/1to9puzzle/status/1129867234816417792
May 19, 2019'''

cols, rows = 5,5
w = 100 #width of a cell
GRIDVALS = [["A","6","-","2","/"],
        ["6","-","9","*","9"],
        ["/","9","==","1","+"],
        ["2","/","2","+","9"],
        ["-","7","/","4","B"]]

MOVES = [[0,1],[0,-1],[1,0],[-1,0]]

class Cell:
    def __init__(self,i,j):
        self.i = i #columns, x
        self.j = j #rows, y
        self.visited = False
        self.value = GRIDVALS[self.j][self.i]
        
    def ind(self,i,j):
        '''Returns index of flat list'''
        return int(i + 5*j)
        
    def checkNeighbors(self):
        global cellList
        neighbors = []
        if self.j > 0:
            top = cellList[self.ind(self.i,self.j-1)]
        if self.j < 4:
            bottom = cellList[self.ind(self.i,self.j+1)]
        if self.i > 0:
            left = cellList[self.ind(self.i-1,self.j)]
        if self.i < 4:
            right = cellList[self.ind(self.i+1,self.j)]
        try:
            if top and not top.visited:
                neighbors.append(top)
                #println("appended top")
        except UnboundLocalError:
            pass
        
        try:
            if bottom and not bottom.visited:
                #println("appended bottom")
                neighbors.append(bottom)
        except UnboundLocalError:
            pass
            
        try:
            if left and not left.visited:
                #println("appended left")
                neighbors.append(left)
        except UnboundLocalError:
            pass
        
        try:
            if right and not right.visited:
                #println("appended right")
                neighbors.append(right)
        except UnboundLocalError:
            pass
        
        
        #println("Neighbors:")
        #println(neighbors)
        
        if len(neighbors)>0:
            r = int(random(0,len(neighbors)))
            return neighbors[r]
        else:
            return None
        
    def show(self):
        x = self.i*w
        y = self.j*w
        stroke(0)
        if self.visited:
            fill(151)
        else:
            if self.i == self.j:
                if self.i in [0,4]:
                    fill(255)
                if self.i == 2:
                    fill(200)
                else:
                    fill(0,200,0)
            if (self.i + self.j) % 2 == 0:
                fill(255,255,0)
            else:
                fill(0,200,0)
        rect(x,y,w,w)
        # line(x,y,x+w,y)
        # line(x+w,y,x+w,y+w)
        # line(x+w,y+w,x,y+w)
        # line(x,y+w,x,y)
        fill(0)
        text(GRIDVALS[self.j][self.i],x+30,y+60)
        
class Grid:
    def __init__(self):
        global cellList,current
        cellList = [Cell(i,j) for j in range(5) for i in range(5)]
        current = cellList[0]
        
    def update(self):
        global cellList
        for cell in cellList:
            cell.show()

g = Grid()
valueList = []

def setup():
    size(500,500)
    textSize(40)
    fill(0)
    
def evaluate(string):
    if "A" in string:
        ind = string.index("A")
        string = string[(ind+1):]
    copystr = string[0]
    for i in range(1,len(string)):
        
        if string[i-1] == '/': 
            copystr += str(float(int(string[i])))
        else:
            copystr += string[i]
    ind = copystr.index("==")
    left = eval(copystr[:ind])
    println("Left: "+str(left))
    #println(copystr[ind+1:])
    right = eval(copystr[ind+2:])
    println("Right: "+str(right))
    return abs(left-right) < 0.1#eval(copystr)
    

def draw():
#     println(evaluate('6-9/2-7/4+2==1*2/9+9'))
# def main():
    #frameRate(20)
    global current,valueList,g
    background(255)
    g.update()
    current.visited = True
    if current.value == "B":
        if "==" in valueList:
            value_string = ''.join(valueList)
            println(value_string)
            
            if evaluate(value_string[1:]):
                println("Solved!")
                noLoop()
            else:
                g = Grid()
                valueList = []
        else:
            g = Grid()
            valueList = []
            
    #println(str(current.i)+','+ str(current.j))
    valueList.append(current.value)
    next = current.checkNeighbors()
    if next:
        next.visited = True
        current = next
    else:
        g = Grid()
        valueList = []
    #value_string = ''.join(valueList)
    #println(value_string)
    #noLoop()
    #saveFrame("####.png")
