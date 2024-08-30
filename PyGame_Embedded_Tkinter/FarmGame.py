import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import threading
import embed_pygame

class FarmGame(tk.Tk):

    # __init__ function for class FarmGame 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        SCREEN_WIDTH=900
        SCREEN_HEIGHT=450
        self.title("FarmGame")
        self.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, GamePage, LevelsPage, SettingsPage):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="sky blue")
        self.controller = controller # for switching pages using class methods

        '''Label: Title'''
        lbl_title = tk.Label(self,text="TopFarmer", font=("Comic Sans MS", 20, "bold"), fg="white", bg="sky blue", anchor=tk.CENTER)
        lbl_title.pack(pady=20)

        '''"Button: New Game'''
        btn_new_game = tk.Button(self, text= "New Game", bg="white", width=10, anchor=tk.CENTER, command=self.handle_new_game)
        btn_new_game.pack(pady=20)

        '''Button: Continue'''
        btn_continue = tk.Button(self, text= "Continue", bg="white", width=10, anchor=tk.CENTER, command=self.handle_continue)
        btn_continue.pack(pady=20)

        '''Button: Levels'''
        btn_levels = tk.Button(self, text= "Levels", bg="white", width=10, anchor=tk.CENTER, command=self.handle_levels)
        btn_levels.pack(pady=20)

        '''Button: Settings'''
        btn_settings = tk.Button(self, text= "Settings", bg="white", width=10, anchor=tk.CENTER, command=self.handle_settings)
        btn_settings.pack(pady=20)

    def handle_new_game(self):
        print("new game")

        '''Ask user if user wants to start new game. If yes, start new game. If no, do nothing.'''
        answer = messagebox.askquestion("Start New Game", "Starting a new game will reset your progress. Do you want to continue?")
        if answer == "yes":
            self.controller.frames[GamePage].txt_code.delete("1.0", "end-1c") # clear input text box
            self.controller.frames[GamePage].embed_pygame_o.farm.__init__() # initialise farm
            '''The above line accesses the parent controller
            which accesses the frames dictionary and
            then accesses the GamePage frame that contains 
            the instance of embed_pygame that contains
            the farm data. I will forget how this works.'''
            self.controller.show_frame(GamePage) # switch to game page
        else:
            pass

    def handle_continue(self):
        print("continue")
        self.controller.show_frame(GamePage)

    def handle_levels(self):
        print("levels")
        self.controller.show_frame(LevelsPage)
        # TODO: show list of levels

    def handle_settings(self):
        print("settings")
        self.controller.show_frame(SettingsPage)
        # TODO: show settings

class GamePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # frame for user input
        frm_input = tk.Frame(self)

        # label for text box
        lbl_code = tk.Label(frm_input, text="Enter code here:")
        lbl_code.pack(anchor="w")

        # text box for user code input
        self.txt_code = tk.Text(frm_input, width=50, height=20)
        self.txt_code.pack(anchor="w")

        # buttons for control/navigation
        btn_run = tk.Button(frm_input, text="Run", width=5, command=self.handle_run)
        btn_clear = tk.Button(frm_input, text="Clear", width=5, command=self.handle_clear)
        btn_restart = tk.Button(frm_input, text="Restart",width=5, command=self.handle_restart)
        btn_help = tk.Button(frm_input, text="Help", width=5, command=self.handle_help)
        btn_home = tk.Button(frm_input, text="Home", width=5, command=self.handle_home)

        btn_run.pack(anchor="s", side="left", pady=5)
        btn_clear.pack(anchor="s", side="left", pady=5)
        btn_restart.pack(anchor="s", side="left", pady=5)
        btn_help.pack(anchor="s", side="left", pady=5)
        btn_home.pack(anchor="s", side="left", pady=5)

        frm_input.pack(anchor="nw", side="left", padx=20, pady=20) # pack input frame

        # frame for embedded pygame display (do not question its magic)
        frm_embed = tk.Frame(self, width=400, height=400)
        frm_embed.pack(anchor="ne", side="top", padx=20, pady=20)
        self.grid()
        os.environ['SDL_WINDOWID'] = str(frm_embed.winfo_id())
        self.update()
        self.embed_pygame_o = embed_pygame.EmbedPygame() # create instance of embed_pygame
        
        # a cheap/lazy way of preventing deadlock
        def pygame_loop():
            while True:
                self.embed_pygame_o.update()
        thread = threading.Thread(target=pygame_loop)
        thread.start()

    def handle_run(self):
        print("run")
        code = self.txt_code.get(1.0, "end-1c") # get user code from text box
        if code == "": # check if user has entered code
            messagebox.showerror(title="ERROR!", message="There is no code to run.")
        else:
            self.embed_pygame_o.execute_python_code(code) # execute user code

    def handle_clear(self):
        print("clear")
        self.txt_code.delete("1.0", "end-1c") # clear user code input text box

    def handle_restart(self):
        print("restart")
        self.txt_code.delete("1.0", "end-1c") # clear input text box
        self.embed_pygame_o.farm.__init__() # initialise farm

    def handle_help(self):
        print("help")
        messagebox.showinfo(title="How to play", message="How to play...\n(coming soon)")

    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage) # switch to home page

# TODO : Add level functionality
class LevelsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_home = tk.Button(self, text="Home", command=self.handle_home)
        btn_home.pack(anchor="nw")
    
    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage)

# TODO : Add settings functionality 
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        btn_home = tk.Button(self, text="Home", command=self.handle_home)
        btn_home.pack(anchor="nw")
    
    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage)

# Driver code
farmgame = FarmGame()
farmgame.mainloop()