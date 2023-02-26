# __________________________________PSEUDOCODE__________________________________

# puzzleinterphase.pyw

# implements a maze game using the Pygame library. The program generates a random maze, and 
# the player must navigate it to reach the exit. The program creates a window with buttons to navigate through the maze, and the player can move by using the arrow keys on the keyboard.

# The program imports necessary libraries and modules such 
# as threading, pygame, datetime, and shelve. It also imports functions from other files such as the maze_generator, maze_solver, and utils.

# The program initializes Pygame, sets up the game window, sets the frames per second, 
# defines some colors that will be used in the game, sets the font size and type, creates an empty list to hold buttons, and sets up the solve thread variable.

# The program defines several functions to draw rectangles, buttons, and the maze, 
# refresh the maze, and create a random maze. It also defines a dispatcher function to handle button clicks.

# The program then starts the game by generating a random-sized maze and starting a 
# new solve thread for it. It also opens a database file and appends records to it.

# If the program is not imported, it runs the game.


# __________________________OBJECT CLASS DIAGRAM RELATIONSHIP DESCRIPTION__________________________________

# MazeGame: This class would represent the main game logic and handle the initialization of 
# Pygame and game window, setting up colors and fonts, and creating a random maze. It would also define the draw_maze() function to draw the maze,
# and the refresh() function to generate a new maze and start a new solve thread for it.
# MazeGenerator: This class would handle the maze generation logic and be responsible for the generate_maze() function.
# MazeSolver: This class would handle the maze solving logic and be responsible for the solve_maze() function.
# Utils: This class would provide utility functions to the game, including the stop_thread() function.
# Button: This class would represent a button in the game window and store its position, size, and text. 
# It would also have a click() function to handle button clicks.
# TextSurface: This class would represent a text surface in the game window and store its position, size, and text.
# Color: This class would represent a color in RGB format and store its red, green, and blue values.
# __________________________________________________________________________________________________________________________


# Import necessary libraries and modules
import threading
import pygame
import datetime, shelve

# Import functions from other files
from maze_generator import generate_maze
from maze_solver import solve_maze
from utils import stop_thread
import random

# Initialize pygame
pygame.init()

# Set window dimensions and other variables
WIDTH = 400
HEADER = 30
HEIGHT = WIDTH + HEADER
WINDOW = (WIDTH, HEIGHT)

TITLE = "Maze Game"

# Set up the game window
SCREEN = pygame.display.set_mode(WINDOW)
pygame.display.set_caption(TITLE)

# Set the game's frames per second
FPS = 60
CLOCK = pygame.time.Clock()

# Define some colors that will be used in the game
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_CYAN = (0, 255, 255)

# Set the font size and type
FONT_SIZE = 16
FONT = pygame.font.Font("ext/fonts/msyh.ttf", FONT_SIZE)

# Create an empty list to hold buttons
BUTTONS = []

# Set up the solve thread variable
SOLVE_THREAD = None

# Set the font size and type for a text surface
FONT = pygame.font.Font(None, 36)

# Create a text surface with a rect object and position it
TEXT_SURFACE = FONT.render("My Text", True, (255, 255, 255))
TEXT_RECT = TEXT_SURFACE.get_rect()
TEXT_RECT.topleft = (20, 20)

# Define a function to draw a rectangle with a given position, size, and color
def draw_rect(x, y, len, color):
    pygame.draw.rect(SCREEN, color, [x, y, len, len], 0)

# Define a function to draw a button with a given position, size, and text
def draw_button(x, y, len, height, text):
    pygame.draw.rect(SCREEN, COLOR_BLACK, [x, y, len, height], 1)
    text_surface = FONT.render(text, True, COLOR_BLACK)
    text_len = text.__len__() * FONT_SIZE
    
    SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))

# Define a function to refresh the maze
def refresh():
    global MAZE, ENTRANCE, EXIT, SOLVE_THREAD
    # If there is already a solve thread running, stop it
    if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
        stop_thread(SOLVE_THREAD)
        SOLVE_THREAD = None
    
    # Generate a new random-sized maze and start a new solve thread for it
    size = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    SOLVE_THREAD.start()

# Draw maze
def draw_maze(maze, cur_pos):
    SCREEN.fill(COLOR_WHITE)
    draw_button(2, 2, WIDTH - 4, HEADER - 4, 'NEXT LEVEL')
    if len(BUTTONS) == 0:
        BUTTONS.append({
            'x': 2,
            'y': 2,
            'length': WIDTH - 4,
            'height': HEADER - 4,
            'click': refresh
        })

    # get size
    size = len(maze)
    cell_size = int(WIDTH / size)
    cell_padding = (WIDTH - (cell_size * size)) / 2
    for y in range(size):
        for x in range(size):
            cell = maze[y][x]
            color = COLOR_BLACK if cell == 1 else COLOR_RED if cell == 3 else COLOR_CYAN if cell == 2 else COLOR_WHITE
            if x == cur_pos[1] and y == cur_pos[2]:
                color = COLOR_GREEN
            draw_rect(cell_padding + x * cell_size, HEADER + cell_padding + y * cell_size, cell_size - 1, color)
    pygame.display.flip()

# Dispatcher
def dispatcher_click(pos):
    for button in BUTTONS:
        x, y, length, height = button['x'], button['y'], button['length'], button['height']
        pos_x, pos_y = pos
        if x <= pos_x <= x + length and y <= pos_y <= y + height:
            button['click']()

# Create a random maze
def random_maze_size():
    return random.randint(5, 20) * 2 + 1

# Run the code if module is not imported
if __name__ == '__main__':
    size = random_maze_size()
    MAZE, ENTRANCE, EXIT = generate_maze(size, size)
    SOLVE_THREAD = threading.Thread(target=solve_maze, args=(MAZE, ENTRANCE, EXIT, draw_maze))
    SOLVE_THREAD.start()
    # Open database, append records
    with shelve.open(".gamedata") as game:
        today = datetime.date.today().strftime("%d/%m/%Y")
        now = datetime.datetime.now().strftime("%H:%M:%S")
        ls, rs = int(random.choice([str(i) for i in range(1, 50)])), int(random.choice(["1", "5", "7", "3", "8", "6"]))
        existing_report = game["report"]
        report_thread = "Date: %s\nTime: %s\nLevel: %s\nNO. of retries: %s\n\n" % (today, now, ls, rs)
        existing_report += report_thread
        game["report"] = existing_report
        game["showreport"] = True
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                if SOLVE_THREAD is not None and SOLVE_THREAD.is_alive():
                    stop_thread(SOLVE_THREAD)
                    SOLVE_THREAD = None
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                dispatcher_click(mouse_pos)
