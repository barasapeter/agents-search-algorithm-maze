# _________________________________PSEUDOCODE__________________________________

# maze_generator.py

# I define two classes, CellType and Direction, to represent the two types of cells (road and wall) 
# in the maze and the four directions (left, up, right, down) that can be taken to navigate through the maze.

# A Maze class is then defined, which initializes the maze with the given width 
# and height and creates an empty maze with walls. It provides methods to reset all cells in the maze with the given value, set a cell in the maze at the given coordinate with the given value, and check if a cell in the maze has been visited (i.e., is not a wall cell).

# The check_neighbors function takes the current cell and checks if there
# are any unvisited neighbors to visit. If there is an unvisited neighbor in a particular direction,
# it adds the direction to a list of directions to choose from. It randomly selects a direction from the list of directions and sets the appropriate cells as a road and adds the corresponding neighbor to the checklist. The function returns True to indicate that a neighbor was added to the maze and False to indicate that no neighbor was added to the maze.

# The random_prime function selects a random starting point in the maze, 
# adds it to the maze, and adds it to the checklist. It then repeatedly selects a random
# entry from the checklist and checks its neighbors until there are no more unvisited neighbors to visit.

# The do_random_prime function resets the maze, runs the 
# random_prime function, and generates a random maze.

# __________________________OBJECT CLASS DIAGRAM________________________
#  +----------+
#  | Direction|
#  +----------+
#  | LEFT     |
#  | UP       |
#  | RIGHT    |
#  | DOWN     |
#  +----------+
#         |
#         |
#  +----------+
#  | CellType |
#  +----------+
#  | ROAD     |
#  | WALL     |
#  +----------+
#         |
#         |
#  +-----+----------+
#  | Maze            |
#  +-----+----------+
#  | - width:int     |
#  | - height:int    |
#  | - maze:List[List[int]] |
#  +-----------------+
#  | + __init__()    |
#  | + reset_maze(value:int)|
#  | + set_maze(x:int, y:int, value:int)|
#  | + visited(x:int, y:int)|
#  +-----------------+
#         |
#         |
#  +-----------------+
#  | - check_neighbors(maze:Maze, x:int, y:int, width:int, height:int, checklist:List[Tuple[int, int]]) |
#  +-----------------+
#  | + __init__()    |
#  +-----------------+


# Import the required libraries
from random import randint, choice

# Define two classes for the two cell types and four directions
class CellType:
    ROAD = 0  # A road cell
    WALL = 1  # A wall cell

class Direction:
    LEFT = 0   # Left direction
    UP = 1     # Up direction
    RIGHT = 2  # Right direction
    DOWN = 3   # Down direction

# Define a class for the maze
class Maze:
    
    # Initialize the maze with given width and height
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Create an empty maze with walls
        self.maze = [[0 for x in range(self.width)] for y in range(self.height)]
    
    # Reset all cells in the maze with the given value
    def reset_maze(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.set_maze(x, y, value)
    
    # Set a cell in the maze at the given coordinate with the given value
    def set_maze(self, x, y, value):
        self.maze[y][x] = CellType.ROAD if value == CellType.ROAD else CellType.WALL
    
    # Check if a cell in the maze has been visited (i.e., is not a wall cell)
    def visited(self, x, y):
        return self.maze[y][x] != 1

def check_neighbors(maze, x, y, width, height, checklist):
    # Create an empty list to store directions
    directions = []

    # Check if there is an unvisited cell to the left
    if x > 0:
        if not maze.visited(2 * (x - 1) + 1, 2 * y + 1):
            # If there is an unvisited cell to the left, add LEFT direction to the list
            directions.append(Direction.LEFT)

    # Check if there is an unvisited cell above
    if y > 0:
        if not maze.visited(2 * x + 1, 2 * (y - 1) + 1):
            # If there is an unvisited cell above, add UP direction to the list
            directions.append(Direction.UP)

    # Check if there is an unvisited cell to the right
    if x < width - 1:
        if not maze.visited(2 * (x + 1) + 1, 2 * y + 1):
            # If there is an unvisited cell to the right, add RIGHT direction to the list
            directions.append(Direction.RIGHT)

    # Check if there is an unvisited cell below
    if y < height - 1:
        if not maze.visited(2 * x + 1, 2 * (y + 1) + 1):
            # If there is an unvisited cell below, add DOWN direction to the list
            directions.append(Direction.DOWN)

    # Check if there is at least one direction in the list
    if len(directions):
        # Randomly choose a direction from the list
        direction = choice(directions)

        # Depending on the chosen direction, set the appropriate cells as ROAD and add the corresponding neighbor to the checklist
        if direction == Direction.LEFT:
            maze.set_maze(2 * (x - 1) + 1, 2 * y + 1, CellType.ROAD)
            maze.set_maze(2 * x, 2 * y + 1, CellType.ROAD)
            checklist.append((x - 1, y))
        elif direction == Direction.UP:
            maze.set_maze(2 * x + 1, 2 * (y - 1) + 1, CellType.ROAD)
            maze.set_maze(2 * x + 1, 2 * y, CellType.ROAD)
            checklist.append((x, y - 1))
        elif direction == Direction.RIGHT:
            maze.set_maze(2 * (x + 1) + 1, 2 * y + 1, CellType.ROAD)
            maze.set_maze(2 * x + 2, 2 * y + 1, CellType.ROAD)
            checklist.append((x + 1, y))
        elif direction == Direction.DOWN:
            maze.set_maze(2 * x + 1, 2 * (y + 1) + 1, CellType.ROAD)
            maze.set_maze(2 * x + 1, 2 * y + 2, CellType.ROAD)
            checklist.append((x, y + 1))

        # Return True to indicate that a neighbor was added to the maze
        return True

    # Return False to indicate that no neighbor was added to the maze
    return False



def random_prime(map, width, height):
    start_x, start_y = (randint(0, width - 1), randint(0, height - 1))
    map.set_maze(2 * start_x + 1, 2 * start_y + 1, CellType.ROAD)
    checklist = [(start_x, start_y)]
    while len(checklist):
        entry = choice(checklist)
        if not check_neighbors(map, entry[0], entry[1], width, height, checklist):
            checklist.remove(entry)


def do_random_prime(map):
    map.reset_maze(CellType.WALL)
    random_prime(map, (map.width - 1) // 2, (map.height - 1) // 2)


def set_entrance_exit(maze):
    # Find the entrance and exit of the maze by checking the edges of the maze
    entrance = []
    for i in range(maze.height):
        if maze.maze[i][1] == 0:
            maze.set_maze(0, i, 0)
            entrance = [0, i]
            break
    exit = []
    for i in range(maze.height - 1, 0, -1):
        if maze.maze[i][maze.width - 2] == 0:
            maze.set_maze(maze.width - 1, i, 0)
            exit = [maze.width - 1, i]
            break
    return entrance, exit


def generate_maze(width=21, height=21):
    # Create a maze object and generate a maze
    maze = Maze(width, height)
    do_random_prime(maze)

    # Find the entrance and exit of the maze
    entrance, exit = set_entrance_exit(maze)
    
    # Return the maze as a 2D array, along with the entrance and exit coordinates
    return maze.maze, entrance, exit

if __name__ == "__main__":
    print(generate_maze())
