import random
import numpy as np

from turtle import Turtle  # https://coolpythoncodes.com/python-turtle/

""" 
Created 1/11/18 by Payson Blackwell

This program creates a maze in a 2D array, and then displays it using the Turtle graphics

 """


# class needed for making pathway
class Point:
    def __init__(self, r, c, parent=None):
        self.r = r
        self.c = c
        self.parent = parent

    def opposite(self):
        if self.r > self.parent.r:
            return Point(self.r+1, self.c, self)
        if self.r < self.parent.r:
            return Point(self.r-1, self.c, self)
        if self.c > self.parent.c:
            return Point(self.r, self.c+1, self)
        if self.c < self.parent.c:
            return Point(self.r, self.c-1, self)
        return None

#class for each individual block
class Block:
    def __init__(self, state, size = 25):
        self.state = state  # closed for solid, open for nothing
        self.visited = 0

        self.color = "blue"
        self.size = size


class Maze:
    def __init__(self, row, col, xCoor = -375, yCoor = 350, blockSize = 25, hardPoints = True):
        self.row = row
        self.col = col
        self.startXCoor = xCoor
        self.startYCoor = yCoor
        self.blockSize = blockSize

        # initializing for start and end blocks Coordinates (usefull for randomaly placed blocks)
        self.startBlockCoors = list()
        self.endBlockCoors = list()

        # Fill all blocks as closed
        self.blocks = [[0 for x in range(self.col)] for y in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                self.blocks[i][j] = Block('closed', blockSize)

        # Setting up Turtle for drawing
        self.t = Turtle()
        self.t.screen.bgcolor('orange')
        self.t.color("blue")
        self.t.shape("turtle")
        self.t.speed(0)

        # Turn off animations to make it go fast
        self.t.screen.tracer(0)

        # move starting drawing point to coordinates
        self.t.up()
        self.t.goto(xCoor, yCoor)
        self.t.down()  

        # make the maze pathway itself
        self.makePaths(hardPoints)
        # draw what is inside the 2d array
        self.drawMaze()      

        # update the screen after making changes (I disabled automatically updating the screen to make it draw instantly)
        self.t.screen.update() 

        # Turns back on animation and puts turtle at starting block
        self.setUpForSolving()


    # Draws a block and moves the cursor to bottom left hand corner of new block, facing east of new 
    def drawBlock(self, block):
        # Draws a block if it is closed, start, or end
        if block.state in ["closed", 'start', 'end', 'wall']:
            self.t.color(block.color)
            self.t.begin_fill()
            # Draw the square
            for steps in range(4):
                self.t.fd(block.size)
                self.t.right(90)
            self.t.end_fill()

        # Move to bottom left corner of block just made
        self.t.up()
        self.t.right(90)
        self.t.fd(block.size)
        self.t.down()
        self.t.left(90)

    # Calls Draw for each block
    def drawMaze(self):
        # Go through list and draw blocks
        for i in range(self.row):
            for j in range(self.col):
                self.drawBlock(self.blocks[i][j])

            # Move to the next Column
            self.t.up()
            self.t.fd(self.blocks[i][j].size)
            self.t.left(90)
            self.t.fd(self.blocks[i][j].size * (j+1))
            self.t.right(90)
            self.t.down()

    # Maze Code based on:
        #https://github.com/Malmactor/maze-solver/blob/master/src/generator.py
            #Which uses Prim's method:
                #https://en.wikipedia.org/wiki/Maze_generation_algorithm

    def makePaths(self, hardPoints = True):
        maze_r = self.row
        maze_c = self.col

        # Set edges as wall
        for i in range(self.row):
            for j in range(self.col):               
                if(i == 0 or j == 0 or i == (self.row-1) or j == (self.col-1)):
                    self.blocks[i][j].state = 'wall'
                    self.blocks[i][j].color = 'black'

        # Puts starting point in the top left corner   
        if hardPoints:
            # For starting in the top left corner
            start_x = 0
            start_y = 1
        else:
            # for starting in random location
            start_x = np.random.random_integers(maze_r)-1
            start_y = np.random.random_integers(maze_c)-1

        # Store coordinates of starting block
        self.startBlockCoors.append(start_x)
        self.startBlockCoors.append(start_y)

        # declare it a start block and make it green
        self.blocks[start_x][start_y].state = 'start'
        self.blocks[start_x][start_y].color = 'green'
        start = Point(start_x, start_y)

        # iterate through direct neighbors of node
        frontier = list()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x*y == 0 and x+y != 0:
                    if start.r+x >= 0 and start.r+x < maze_r and start.c+y >= 0 and start.c+y < maze_c:
                        frontier.append(Point(start.r+x, start.c+y, start))    
  
        last = None # Initializing last for later

        # Go through current neighbors
        while frontier:
            # pick current neighbor at random
            current = frontier.pop(np.random.random_integers(len(frontier))-1)
            opposite = current.opposite()

            # if both current neighbor and its opposite are walls
            if opposite.r >= 0 and opposite.r < maze_r and opposite.c >= 0 and opposite.c < maze_c:
                if self.blocks[current.r][current.c].state == 'closed' and self.blocks[opposite.r][opposite.c].state == 'closed':
                    # open path between the nodes
                    self.blocks[current.r][current.c].state = 'open'
                    self.blocks[opposite.r][opposite.c].state = 'open'

                    # store last node in order to mark it later
                    last = opposite
                    # iterate through direct neighbors of current node, same as earlier
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            if x*y == 0 and x+y != 0:
                                if opposite.r+x >= 0 and opposite.r+x < maze_r and opposite.c+y >= 0 and opposite.c+y < maze_c:
                                    frontier.append(
                                        Point(opposite.r+x, opposite.c+y, opposite))

        # if maze is finished, there will be no more neighbors
        if last:
            if hardPoints:
                # setting exit to be on the bottom right hand corner
                self.blocks[self.row-1][self.col-3].state = 'end'
                self.blocks[self.row-1][self.col-3].color = 'red'

                # set end block coordinates
                self.endBlockCoors.append(self.row-1)
                self.endBlockCoors.append(self.col-3)
            else:
                # If you want the exit to move around
                self.blocks[last.r][last.c].state = 'end'
                self.blocks[last.r][last.c].color = 'red'
                self.endBlockCoors.append(last.r)
                self.endBlockCoors.append(last.c)
    def setUpForSolving(self):
        # This function goes to the starting block and sets it up for someone to start finding a way to the end

        self.t.up()
        # To go back to starting block, move to starting coordinate and the away by how many blocks it started by
        x = self.startXCoor + (self.blockSize * self.startBlockCoors[0])
        y = self.startYCoor - (self.blockSize * self.startBlockCoors[1])

        self.t.goto(x , y)
        self.t.down()

        # change turtle color and turn drawing back on
        self.t.color("yellow")
        self.t.shape("turtle")
        self.t.speed(1)
        # Turn on animation
        self.t.screen.tracer(1)


# start Maze with 30x30 grid
maze = Maze(30, 30) 

# exit screen when you click it
maze.t.screen.exitonclick() 
"""
# For customizing the maze: 
maze = Maze(30, 30, -500, 400)  # Sets the X and Y coordinates of where to start the drawing

maze = Maze(30, 30, -500, 400, 20)  # Sets the individual blocks size

maze = Maze(30, 30, -500, 400, 20, False) # Randomly place the start and end points
"""