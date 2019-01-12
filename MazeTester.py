from MazeGenerator import Maze
# This files is used for moving the main function into a different file

# start Maze with 30x30 grid
maze = Maze(30, 30) 

# Can move turtle by calling function
maze.moveRight()

# This is how you can move the turtle with a keyboard press
maze.t.screen.onkey(maze.moveRight,"Right")
maze.t.screen.listen()
maze.t.screen.mainloop()

# exit screen when you click it, useful when not receiving input from keyboard
#maze.t.screen.exitonclick()  

"""
# For customizing the maze: 
maze = Maze(30, 30, -500, 400)  # Sets the X and Y coordinates of where to start the drawing

maze = Maze(30, 30, -500, 400, 20)  # Sets the individual blocks size

maze = Maze(30, 30, -500, 400, 20, False) # Randomly place the start and end points (use this if you change the dimensions of the grid too much)
"""