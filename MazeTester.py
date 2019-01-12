from MazeGenerator import Maze

# start Maze with 30x30 grid
maze = Maze(30, 30)

maze.t.screen.exitonclick()  # exit screen when you click it

"""
# For customizing the maze: 
maze = Maze(30, 30, -500, 400)  # Sets the X and Y coordinates of where to start the drawing

maze = Maze(30, 30, -500, 400, 20)  # Sets the individual blocks size

maze = Maze(30, 30, -500, 400, 20, False) # Randomly place the start and end points
"""
