from MazeGenerator import Maze
from random import shuffle
from time import sleep
# This files is used for moving the main function into a different file
"""
TODO: 

    Right now it gets a little bit messy when it is coming out of a corner and the intersection block has more visited than the corner
        Maybe make special condition for blocks that have more than 3 open pathways



    For redrawing the correct pathway, check for all yellow touching 

"""


def solveMaze(maze, animations = True):
    foundExit = False

    # Turn off animations to make it go fast
    if(animations is False):      
        maze.t.speed(0)
        maze.t.screen.tracer(0)
      
    while(foundExit is False):
        #get neighbor blocks, sorted by times visited
        choices = getChoices(maze)

        if(choices[0].state == 'end'):
            foundExit = True
            maze.moveDirection(choices[0].direction)
            break
        
        if(len(choices) > 1):
            # if visited == 0, then all choices in the list haven't been touched, so randomly shuffle
            if(choices[0].visited == 0):
                shuffle(choices)
            else:
                # all blocks in list have been moved on at least once
                choices = getChoices(maze, False)
                # take dead-ends out of the list
                for b in choices[:]:
                    if(b.deadEnd):
                        choices.remove(b)    
                    
                # If there is an intersection, add it back to the possible choices
                #TODO: not working correctly, especially when intersection visited count is high?
                allChoices = getChoices(maze, False)
                if(len(allChoices) == 2):
                    for b in allChoices:
                        if(b.availableMoves >= 3):
                            choices.append(b) # not reaching here when it should

                # choose the block that is the furthest from our current turn
                choices.sort(key=lambda choice: choice.turnMovedOn)

        # make the move
        maze.moveDirection(choices[0].direction)
        
        
    
    # Turn animations back on
    if(animations is False):  
        maze.t.screen.update() 
        maze.t.speed(0.5)
        maze.t.screen.tracer(1)


# Returns a list of blocks that are open and tied for least times visited if parameter is True
def getChoices(maze, topChoices = True):
    choices = list()
    directions = ['up','right','down','left']
    # currentBlock =  maze.blocks[maze.currentArrayLocation[0]][maze.currentArrayLocation[1]]

    # Looks through the blocks nearby and puts them into a list of possible choices if it is 
    for d in directions:
        if(maze.checkSpace(d) == 'end'): 
            maze.checkSpace(d, True).direction = d
            lastMove = list() 
            lastMove.append(maze.checkSpace(d, True))
            return lastMove # returns only the exit if we find it
            # return list(maze.checkSpace(d, True)) # returns only the exit if we find it

        elif(maze.checkSpace(d) in ['open','start']):
            maze.checkSpace(d, True).direction = d
            choices.append(maze.checkSpace(d, True))

    # mark how many blocks there are available on the current block
    maze.blocks[maze.currentArrayLocation[0]][maze.currentArrayLocation[1]].availableMoves = len(choices)

    # If there is only 1 open block and it has been visited then mark current as a dead-end
    if(len(choices) == 1 and choices[0].visited > 0):
        maze.blocks[maze.currentArrayLocation[0]][maze.currentArrayLocation[1]].deadEnd = True

    # sort by times visited
    choices.sort(key=lambda choice: choice.visited)

    #only returns the tied blocks for least times visited
    if((topChoices is True) and len(choices) > 1):
        bestChoices = list()
        leastVisited = choices[0].visited
        for b in choices:
            if(b.visited == leastVisited):
                bestChoices.append(b)
            else:
                break
        return bestChoices
    return choices


while(True):
    # start Maze with 30x30 grid
    maze = Maze(30, 30) 
    solveMaze(maze, True)
    sleep(5)
    maze.t.reset()






# sets up the binding to call function when button is pressed
maze.t.screen.onkey(maze.moveRight,"Right") 
maze.t.screen.onkey(maze.moveLeft,"Left")
maze.t.screen.onkey(maze.moveDown,"Down")
maze.t.screen.onkey(maze.moveUp,"Up")
maze.t.screen.listen()  # waits for button to be pressed, call coresponding function if needed

#only have one of these, this loops back and works with listen, put this at the end of your file if you are accepting movement through keys
maze.t.screen.mainloop() 

# exit screen when you click it, useful when not receiving input from keyboard
maze.t.screen.exitonclick()  

"""
# For customizing the maze: 
maze = Maze(30, 30, -500, 400)  # Sets the X and Y coordinates of where to start the drawing

maze = Maze(30, 30, -500, 400, 20)  # Sets the individual blocks size

maze = Maze(30, 30, -500, 400, 20, False) # Randomly place the start and end points (use this if you change the dimensions of the grid too much)
"""