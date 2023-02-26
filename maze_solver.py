# __________________________________PSEUDOCODE__________________________________

# maze_solver.py

# defines two classes: CellType and Direction. 
# CellType has four attributes that represent the types of cells that can exist in a maze: 
# ROAD, WALL, WALKED, and DEAD. Direction has four attributes that represent the directions in which the algorithm can move: LEFT, UP, RIGHT, and DOWN.

# The valid function checks if a given position (x, y) is a valid position in the maze. 
# It does this by checking if x or y are negative or greater than or equal to the length of the maze, and if the value of the cell at (x, y) is a wall or dead end. If the position is valid, it returns a tuple containing the value of the cell at (x, y) and its coordinates.

# The neighbors function takes a maze and a position and returns a tuple 
# containing the valid neighbors of the cell at that position. It uses the valid function to check if the cell to the top, right, bottom, and left of the current position is valid.

# The mark_walked function marks a given position in the maze as walked by setting its 
# value to CellType.WALKED.

# The mark_dead function marks a given position in the maze as 
# a dead end by setting its value to CellType.DEAD.

# The suggest_pos function takes a list of cells and returns 
# the cell with the lowest value. It does this by iterating over the list and adding the value of the cell to a new list. If a cell is None, it adds CellType.DEAD to the new list. It then returns the position with the lowest value.

# The solve_maze function recursively solves the maze. 
# It takes a maze, a starting position, an end position, and a callback function. It starts by sleeping for a short period of time to slow down the algorithm for visualization purposes.

# It then checks if the current position is the end position. 
# If it is, it marks the position as walked and returns True.

# If the current position is not the end position, it gets the valid neighbors 
# of the current position and chooses the one with the lowest value using the suggest_pos function. If there is a valid neighbor, it marks the current position as walked and moves to the next position by recursively calling solve_maze with the next position as the new starting position. If there is no valid neighbor, it marks the current position as a dead end and moves back to the previous position by returning False.

# The callback function is called with the current state of the maze and the next 
# # position to be walked. It can be used to visualize the algorithm as it solves the maze.


# ___________________________OBJECT CLASS DIAGRAM_______________________________________
# +-----------------------------------+
# |           CellType                |
# +-----------------------------------+
# | - ROAD: int                       |
# | - WALL: int                       |
# | - WALKED: int                     |
# | - DEAD: int                       |
# +-----------------------------------+
# | + ROAD: int                       |
# | + WALL: int                       |
# | + WALKED: int                     |
# | + DEAD: int                       |
# +-----------------------------------+

# +-----------------------------------+
# |           Direction               |
# +-----------------------------------+
# | - LEFT: int                       |
# | - UP: int                         |
# | - RIGHT: int                      |
# | - DOWN: int                       |
# +-----------------------------------+
# | + LEFT: int                       |
# | + UP: int                         |
# | + RIGHT: int                      |
# | + DOWN: int                       |
# +-----------------------------------+

# +-----------------------------------+
# |            MazeSolver             |
# +-----------------------------------+
# | - maze: list of list of int        |
# | - end: tuple of int               |
# +-----------------------------------+
# | + valid(x: int, y: int) -> bool   |
# | + neighbors(pos: tuple) -> tuple  |
# | + mark_walked(pos: tuple) -> None |
# | + mark_dead(pos: tuple) -> None   |
# | + suggest_pos(cells: list) -> tuple|
# | - solve_maze(pos: tuple, callback) -> bool|
# +-----------------------------------+


# Import the required libraries
import time

# Define constants for cell types and directions
class CellType:
    ROAD = 0
    WALL = 1
    WALKED = 2
    DEAD = 3

class Direction:
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3,

# Check if the given position (x, y) is a valid position in the maze
def valid(maze, x, y):
    # Check if x or y are negative
    if x < 0 or y < 0:
        return False
    # Check if x or y are greater than or equal to the length of the maze
    if x >= len(maze) or y >= len(maze):
        return False
    # Check if the value of the cell at (x, y) is a wall or dead end
    val = maze[y][x]
    if val == CellType.WALL or val == CellType.DEAD:
        return False
    # Return the value of the cell at (x, y) and its coordinates if it is valid
    return val, x, y

# Return a tuple containing the valid neighbors of the cell at the given position
def neighbors(maze, pos):
    x, y = pos
    # Check if the cell to the top, right, bottom, and left of the current position is valid
    t, r, d, l = valid(maze, x, y - 1), valid(maze, x + 1, y), valid(maze, x, y + 1), valid(maze, x - 1, y)
    # Return a tuple containing the valid neighbors
    return t, r, d, l

# Mark the given position as walked
def mark_walked(maze, pos):
    maze[pos[1]][pos[0]] = CellType.WALKED

# Mark the given position as a dead end
def mark_dead(maze, pos):
    maze[pos[1]][pos[0]] = CellType.DEAD

# Given a list of cells, return the cell with the lowest value
def suggest_pos(cells):
    arr = []
    for cell in cells:
        if cell:
            arr.append(cell[0])
        else:
            arr.append(CellType.DEAD)
    # Return the position with the lowest value
    return cells[arr.index(min(arr))]

# Recursively solve the maze by choosing the next valid neighbor with the lowest value
def solve_maze(maze, pos, end, callback):
    # Sleep for a short period of time to slow down the algorithm for visualization purposes
    time.sleep(0.05)

     # Check if the current position is the end position
    if pos[0] == end[0] and pos[1] == end[1]:
        mark_walked(maze, pos)
        return True
    
     # Get the valid neighbors of the current position and choose the one with the lowest value
    t, r, d, l = neighbors(maze, pos)
    next_pos = suggest_pos((t, r, d, l))

    # If there is a valid neighbor, mark the current position as walked and move to the next position
    if next_pos:
        if next_pos[0] == CellType.WALKED:
            mark_dead(maze, pos)
        else:
            mark_walked(maze, pos)
        callback(maze, next_pos)
        return solve_maze(maze, (next_pos[1], next_pos[2]), end, callback)
    else:
        mark_dead(maze, pos)
        callback(maze, next_pos)
        return False
