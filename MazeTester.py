from MazeGenerator import Maze
# This files is used for moving the main function into a different file
"""
If you have a fresh install and need to import numpy, install pip first

download pip by running the python file which you can find online,
then in command line, run : pip install numpy

That should install numpy if your python download didn't include it
"""

# start Maze with 30x30 grid
maze = Maze(30, 30) 

# Can move turtle by calling function
maze.moveRight()


# This is how you can move the turtle with a keyboard press (For fun, solving program probably won't use this)
maze.t.screen.onkey(maze.moveRight,"Right") # sets up the binding to call function when button is pressed
maze.t.screen.listen()  # waits for button to be pressed, call coresponding function if needed

#only have one of these, this loops back and works with listen, put this at the end of your file if you are accepting movement through keys
maze.t.screen.mainloop() 

# exit screen when you click it, useful when not receiving input from keyboard
#maze.t.screen.exitonclick()  

"""
# For customizing the maze: 
maze = Maze(30, 30, -500, 400)  # Sets the X and Y coordinates of where to start the drawing

maze = Maze(30, 30, -500, 400, 20)  # Sets the individual blocks size

maze = Maze(30, 30, -500, 400, 20, False) # Randomly place the start and end points (use this if you change the dimensions of the grid too much)
"""