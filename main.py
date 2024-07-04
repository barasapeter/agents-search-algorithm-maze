# main.py

# _____________________________________PSEUDOCODE___________________________________

# The code imports several modules, including shelve, pygame, os, sys, subprocess, and tkinter.
# It also defines a list of database files and three functions: record_user_data(), view_scores(), and StartGame.

# The record_user_data() function stores user data in a database file named ".gamedata" using the shelve module
# If the platform is Windows, it also sets the hidden attribute for the database files.

# The view_scores() function displays a pop-up window using the tkinter module that shows the score data recorded in the ".gamedata" file.

# The StartGame class is initialized with a width and height parameter and is responsible for
# running a Pygame game that counts down from ten minutes. Once the time is up, a message is displayed using the tkinter.messagebox.showinfo() function.

# The MainMenu class is also initialized with a caption, size, and font size parameter.
# It displays a menu screen using the Pygame module that includes two buttons: "Start Game" and
# "View Scores." If the "Start Game" button is clicked, the os.startfile() function 
# is used to launch the "puzzleinterphase.pyw" file. 
# If the "View Scores" button is clicked, the view_scores() function is called to display the score data.

# The NamePrompt class is similar to the MainMenu class in that it displays a Pygame window.
# However, it is used to prompt the user for their name before starting the game. The user's input is recorded in a text box and can be submitted using the "SUBMIT" button.


# ___________________________OBJECT CLASS DIAGRAM________________________________________________________
# +------------------+        +----------------+         +----------------+         +-----------------+
# |                  |        |                |         |                |         |                 |
# | MainMenu         |        | NamePrompt     |         | StartGame      |         |                 |
# |------------------|        |----------------|         |----------------|         |-----------------|
# | - screen         |        | - screen       |         | - width        |         |                 |
# | - clock          |        | - clock        |         | - height       |         | - remaining_time|
# | - font           |        | - font         |         | - screen       |         |                 |
# | - start_button   |        | - input_box    |         | - clock        |         |                 |
# | - scores_button  |        | - color_active |         | - font         |         |                 |
# |                  |        | - color_inactive           | - start_button |         |                 |
# | + handle_events()|        |                |         |                |         | + run()          |
# | + draw()         |        |                |         |                |         |                 |
# | + run()          |        | + run()         |         | + run()         |         |                 |
# |                  |        |                |         |                |         |                 |
# +------------------+        +----------------+         +----------------+         +-----------------+
        
# The object classes in the diagram are as follows:

# - MainMenu: This class is responsible for creating the main menu window, handling button click events, and displaying the buttons. It has attributes such as `screen`, `clock`, `font`, `start_button`, `scores_button`, and methods such as `handle_events()`, `draw()`, and `run()`.

# - NamePrompt: This class is responsible for creating the window to prompt for a username. It has attributes such as `screen`, `clock`, `font`, `input_box`, `color_active`, `color_inactive`, and methods such as `run()`.

# - StartGame: This class is responsible for creating the game window, initializing variables, and running the game. It has attributes such as `width`, `height`, `screen`, `clock`, `font`, `remaining_time`, and methods such as `run()`.


# Import the required libraries
import shelve, pygame, os, sys, subprocess
import tkinter.messagebox
import tkinter as tk

# State the database file names
database_files = [".gamedata.bak", ".gamedata.dat", ".gamedata.dir"]

# Take keys and values of data, write them in a shelve
def record_user_data(**kwargs):
    with shelve.open(".gamedata") as game_database:
        for key, value in kwargs.items():
            game_database[key] = value
    if "win" in sys.platform:
        for file in database_files:
            subprocess.check_call(["attrib", "+H", file])  

# View scores
def view_scores():
    popup = tk.Tk()
    popup.title("Pygame-VIEW SCORES")
    popup.geometry("500x400")
    popup.wm_attributes("-topmost", True)
    tk.Button(popup, text="OK", font=(None, 25, "bold"), command=popup.destroy, width=5, background="#20BEBE").pack(side="bottom", pady=10)
    
    game_score = tk.Text(popup, font=(None, 10, "bold"))
    game_score.pack(expand="yes")

    # Open database
    with shelve.open(".gamedata") as gamedata:
        if not gamedata["showreport"]:
            game_score.insert("0.0", "NO SCORE HAS BEEN RECORDED YET")
        else:
            game_score.insert("0.0", gamedata["report"])

    popup.mainloop()

# Create a window to start Game
class StartGame:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 22)
        self.remaining_time = 600 # 10 minutes in seconds
    
    # Run the game
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Fill the screen white
            self.screen.fill((255, 255, 255))
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            label = self.font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
            self.screen.blit(label, (10, 10))
            pygame.display.flip()
            self.remaining_time -= 1
            self.clock.tick(1)
            
            # Check if countdown has ended
            if self.remaining_time == 0:
                running = False
        
        tkinter.messagebox.showinfo("Pygame", "Time is up!\n[Results will show here...]")

# Create a main menu window
class MainMenu:
    def __init__(self, caption, size=(400, 300), font_size=32):
        # Initialize the variables
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, font_size)
        self.start_button = pygame.Rect(100, 100, 200, 50)
        self.start_button_text = self.font.render('Start Game', True, pygame.Color('white'))
        self.start_button_color = pygame.Color('deepskyblue')
        self.scores_button = pygame.Rect(100, 200, 200, 50)
        self.scores_button_text = self.font.render('View Scores', True, pygame.Color('white'))
        self.scores_button_color = pygame.Color('deepskyblue')

    # Handle button click events   
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    # print('Starting game...')
                    os.startfile("puzzleinterphase.pyw")
                elif self.scores_button.collidepoint(event.pos):
                    # print('Viewing scores...')
                    view_scores()
        return True

    # Draw Start Game button
    def draw(self):
        self.screen.fill(pygame.Color('white'))
        
        pygame.draw.rect(self.screen, self.start_button_color, self.start_button)
        self.start_button_text = self.font.render('Start Game', True, pygame.Color('white'))
        self.screen.blit(self.start_button_text, (140, 110))
        
        pygame.draw.rect(self.screen, self.scores_button_color, self.scores_button)
        self.scores_button_text = self.font.render('View Scores', True, pygame.Color('white'))
        self.screen.blit(self.scores_button_text, (135, 210))
        
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        pygame.quit()

# Create a window to prompt username
class NamePrompt:
    def __init__(self, caption, size=(400, 300), font_size=32):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, font_size)
        self.input_box = pygame.Rect(100, 100, 200, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''
        self.button = pygame.Rect(150, 200, 100, 50)
        self.button_text = self.font.render('SUBMIT', True, pygame.Color('white'))
        self.button_color = pygame.Color('deepskyblue')
        self.blink = True     

    # Handle button clicks and keyboard bindings
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = True
                    self.color = self.color_active
                elif self.button.collidepoint(event.pos):
                    print("Username entered: ", self.text)
                    if self.text != "":
                        record_user_data(username=self.text, showreport=False, report="")
                        self.menu = MainMenu('Main Menu, PLAYER:')
                        self.menu.run()
                    else:
                        tkinter.messagebox.showerror("Pygame", "Name cannot be left blank!")
                    self.text = ''
                else:
                    self.active = False
                    self.color = self.color_inactive
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        print("Username entered: ", self.text)
                        if self.text != "":
                            record_user_data(username=self.text, showreport=False, report="")
                            self.menu = MainMenu('Main Menu, PLAYER:')
                            self.menu.run()
                        else:
                            tkinter.messagebox.showerror("Pygame", "Name cannot be left blank!")
                        self.text = ''
                        self.active = False
                        self.color = self.color_inactive
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
        return True

    # Create a blinking cursor event
    def draw(self):
        self.screen.fill(pygame.Color('white'))
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        txt_surface = self.font.render(self.text, True, pygame.Color('black'))
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        prompt_text = self.font.render("Enter your name:", True, pygame.Color('black'))
        self.screen.blit(prompt_text, (100, 50))
        
        # Blinking cursor
        if self.active and self.blink:
            cursor_pos = self.font.size(self.text)[0] + self.input_box.x + 5
            pygame.draw.line(self.screen, pygame.Color('black'), (cursor_pos, self.input_box.y + 5), (cursor_pos, self.input_box.y + self.input_box.height - 5), 2)
        if pygame.time.get_ticks() % 1000 < 500:
            self.blink = True
        else:
            self.blink = False
        
        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
        pygame.quit()

# Run the game instance
if __name__ == '__main__':
    existing_confirmed = []    
    for file in database_files:
        if os.path.exists(file):
            existing_confirmed.append(file)
    if existing_confirmed != database_files:
        # Remove the available files cause they have been either altered or corrupted.
        [os.remove(file) for file in existing_confirmed]
        prompt = NamePrompt('Name Prompt')
        prompt.run() 
    else:
        menu = MainMenu('Main Menu, PLAYER:')
        menu.run() 
