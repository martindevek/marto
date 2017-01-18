import turtle

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'

class Maze:
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []

        self.distances = [] # distancia minima tentativa a la posicion de salida
        self.parentCoords = [] # coordenadas del nodo padre de donde proviene el camino minimo tentativo
        self.exitCoords = None # coordenadas de la salida del laberinto

        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            rowDistances = []
            rowCoords = []
            col = 0
            for ch in line[:-1]:
                rowList.append(ch)
                rowDistances.append(float("inf")) # definimos las filas de distancia con el máximo valor posible
                rowCoords.append(None)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            self.distances.append(rowDistances) # armamos la matriz de distancias con las distintas filas
            self.parentCoords.append(rowCoords)
            columnsInMaze = len(rowList)

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-(columnsInMaze-1)/2-.5,-(rowsInMaze-1)/2-.5,(columnsInMaze-1)/2+.5,(rowsInMaze-1)/2+.5)

    def drawMaze(self):
        self.t.speed(1000)
        self.wn.tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x] == OBSTACLE:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'orange')
        self.t.color('black')
        self.t.fillcolor('blue')
        self.wn.update()
        self.wn.tracer(1)

    def drawCenteredBox(self,x,y,color):
        self.t.up()
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    def dropBreadcrumb(self,color):
        self.t.dot(10,color)

    def updatePosition(self,row,col,val=None):
        if val:
            self.mazelist[row][col] = val
        self.moveTurtle(col,row)

        if val == PART_OF_PATH:
            color = 'green'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        else:
            color = None

        if color:
            self.dropBreadcrumb(color)

    def isExit(self, row, col):
        return (row == 0 or
                row == self.rowsInMaze-1 or
                col == 0 or
                col == self.columnsInMaze-1 )

    def __getitem__(self,idx):
        return self.mazelist[idx]

class Coords:
# Clase que representa un par de coordenadas
    def __init__(self, row, col):
        self.row = row
        self.col = col

def searchFrom(maze, startRow, startColumn, distance, parentCoords):
    # try each of four directions from this point until we find a way out.
    # base Case return values:
    #  1. We have run into an obstacle, return false
    # maze.updatePosition(startRow, startColumn)
    if maze[startRow][startColumn] == OBSTACLE :
        return
    #  2. We have found a square that has already been explored
    if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
        return
    # 3. We have found an outside edge not occupied by an obstacle
    if maze.isExit(startRow,startColumn):
        maze.exitCoords = Coords(startRow, startColumn)
    # 4. If we founded a shortest path before
    # in reference to exit coords
    if maze.exitCoords and maze.distances[maze.exitCoords.row][maze.exitCoords.col] <= distance:
        return
    # in reference to the actual coords
    if maze.distances[startRow][startColumn] <= distance:
        return

    # We founded a shortest path until now
    maze.distances[startRow][startColumn] = distance # seteamos la nueva distancia minima tentativa
    maze.parentCoords[startRow][startColumn] = parentCoords # nodo padre de donde proviene el camino minimo tentativo

    maze.updatePosition(startRow, startColumn)

    # Otherwise, use logical short circuiting to try each direction
    # in turn (if needed)
    searchFrom(maze, startRow-1, startColumn, distance+1, Coords(startRow, startColumn))
    searchFrom(maze, startRow+1, startColumn, distance+1, Coords(startRow, startColumn))
    searchFrom(maze, startRow, startColumn-1, distance+1, Coords(startRow, startColumn))
    searchFrom(maze, startRow, startColumn+1, distance+1, Coords(startRow, startColumn))


def exitMaze(maze, coords):
# funcion recursiva que se llama inicialmente con las coordenadas de la salida y recorre los nodos padre hasta llegar al punto de partida
    if coords:
        maze.updatePosition(coords.row, coords.col, PART_OF_PATH)
        exitMaze(maze, maze.parentCoords[coords.row][coords.col])


# MAIN PROGRAM
myMaze = Maze('maze2.txt')
myMaze.drawMaze()
myMaze.updatePosition(myMaze.startRow,myMaze.startCol)

searchFrom(myMaze, myMaze.startRow, myMaze.startCol, 0, None)

if myMaze.exitCoords:
    exitMaze(myMaze, myMaze.exitCoords)
else:
    print ("No way out")

input("press enter")
