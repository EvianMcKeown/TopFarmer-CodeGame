#farmgamegui.py

import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
import os
import threading
import embed_pygame
from saveandload import SaveAndLoad
from level import Levels
from farmgrid import FarmGrid
import time
from musicplayer import MusicPlayer

class FarmGameGUI(tk.Tk):

    # __init__ function for class FarmGame 
    def __init__(self, *args, **kwargs): 
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        SCREEN_WIDTH=1000
        SCREEN_HEIGHT=500
        self.title("FarmGame")
        self.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.saveandload = SaveAndLoad()
        self.levels = Levels()

        # creating a container
        container = tk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (HomePage, GamePage, LevelsPage, StatisticsPage, SettingsPage):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(HomePage)

        # audio files paths
        bg_music = "assets/music/Lively Meadow (Song Loop) B 118.wav"
        completion_sound = "assets/music/Lively Meadow Victory Fanfare.wav"
        fail_sound = "assets/music/death.wav"

        # create music player
        self.music_player = MusicPlayer(bg_music, completion_sound, fail_sound)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def on_closing(self):
        self.music_player.stop_background_music()
        self.saveandload.save_code(self.frames[GamePage].txt_code.get(1.0, "end-1c"))
        self.frames[GamePage].embed_pygame_o.exit()
        self.destroy()
        exit(0)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg="sky blue")
        self.controller = controller # for switching pages using class methods

        '''Label: Title'''
        lbl_title = tk.Label(self,text="TopFarmer", font=("Comic Sans MS", 20, "bold"), fg="white", bg="sky blue", anchor=tk.CENTER)
        lbl_title.pack(pady=20)

        '''Button: New Game'''
        btn_new_game = tk.Button(self, text= "New Game", bg="white", width=10, anchor=tk.CENTER, command=self.handle_new_game)
        btn_new_game.pack(pady=20)

        '''Button: Continue'''
        btn_continue = tk.Button(self, text= "Continue", bg="white", width=10, anchor=tk.CENTER, command=self.handle_continue)
        btn_continue.pack(pady=20)

        '''Button: Levels'''
        btn_levels = tk.Button(self, text= "Levels", bg="white", width=10, anchor=tk.CENTER, command=self.handle_levels)
        btn_levels.pack(pady=20)

        '''Button: Statistics'''
        btn_statistics = tk.Button(self, text= "Statistics", bg="white", width=10, anchor=tk.CENTER, command=self.handle_statistics)
        btn_statistics.pack(pady=20)

        '''Button: Settings'''
        btn_settings = tk.Button(self, text= "Settings", bg="white", width=10, anchor=tk.CENTER, command=self.handle_settings)
        btn_settings.pack(pady=20)

    def handle_new_game(self):
        print("new game")

        '''Ask user if user wants to start new game. If yes, start new game. If no, do nothing.'''
        answer = messagebox.askquestion("Start New Game", "Starting a new game will reset your progress. Do you want to continue?")
        if answer == "yes":
            if os.path.exists("level_progress.json"):
                os.remove("level_progress.json")
                print(f"Save file deleted.")
            else:
                print(f"No save file yet.") 
            self.controller.frames[GamePage].txt_code.delete("1.0", "end-1c") # clear input text box
            self.controller.frames[GamePage].embed_pygame_o.farm.__init__() # initialise farm
            '''The above line accesses the parent controller
            which accesses the frames dictionary and
            then accesses the GamePage frame that contains 
            the instance of embed_pygame that contains
            the farm data. I will forget how this works.'''
            self.controller.show_frame(GamePage) # switch to game page
            self.controller.frames[GamePage].start_level(1)
        else:
            pass

    def handle_continue(self):
        print("continue")
        self.controller.frames[GamePage].handle_restart()
        self.controller.show_frame(GamePage)
        #self.controller.frames[GamePage].display_level_task()

    def handle_levels(self):
        print("levels")
        self.controller.show_frame(LevelsPage)
    
    def handle_statistics(self):
        print("statistics")
        self.controller.show_frame(StatisticsPage)
        self.controller.frames[StatisticsPage].refresh()
        # TODO: show statistics

    def handle_settings(self):
        print("settings")
        self.controller.show_frame(SettingsPage)
        # TODO: show settings

class GamePage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="sky blue")
        self.lock = threading.Lock()

        # Frame for user input
        frm_input = tk.Frame(self, bg="sky blue", width=400, height=300)
        frm_input.pack_propagate(False)  # prevent frame from resizing

        # Label for text box
        lbl_code = tk.Label(frm_input, text="Enter code here:", bg="sky blue")
        lbl_code.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Scrollbar creation (vertical and horizontal)
        scrollbar_y = tk.Scrollbar(frm_input)
        scrollbar_x = tk.Scrollbar(frm_input, orient="horizontal")

        # Text box for user code input ( vertically and horizontally scrollable, no text wrapping)
        self.txt_code = tk.Text(frm_input, width=50, height=24, wrap="none",yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        font = tkfont.Font(font=self.txt_code['font'])  # Tab config
        tab = font.measure('    ')                      # Tab config
        self.txt_code.config(tabs=tab)                  # Tab config
        self.txt_code.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Scrollbars config
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")
        scrollbar_y.config(command=self.txt_code.yview)
        scrollbar_x.config(command=self.txt_code.xview)

        # Configure gui grid to allow expansion of text box
        frm_input.grid_rowconfigure(1, weight=1)
        frm_input.grid_columnconfigure(0, weight=1)

        # Load saved code
        self.txt_code.insert("1.0", controller.saveandload.load_code())

        # Frame for buttons
        frm_buttons = tk.Frame(self, bg="sky blue")
        frm_buttons.pack(side="bottom", fill="x", padx=15, pady=10)

        # Buttons for control/navigation
        btn_run = tk.Button(frm_buttons, text="Run", width=5, command=self.handle_run)
        btn_clear = tk.Button(frm_buttons, text="Clear", width=5, command=self.handle_clear)
        btn_restart = tk.Button(frm_buttons, text="Restart", width=5, command=self.handle_restart)
        btn_task = tk.Button(frm_buttons, text="Task", width=5, command=self.handle_task)
        btn_help = tk.Button(frm_buttons, text="Help", width=5, command=self.handle_help)
        btn_home = tk.Button(frm_buttons, text="Home", width=5, command=self.handle_home)

        # Pack buttons under input text box
        btn_run.pack(side="left", padx=5)
        btn_clear.pack(side="left", padx=5)
        btn_restart.pack(side="left", padx=5)
        btn_task.pack(side="left", padx=5)
        btn_help.pack(side="left", padx=5)
        btn_home.pack(side="left", padx=5)

        # Pack input frame
        frm_input.pack(anchor="nw", side="left", padx=20, pady=10, fill="both", expand=True)

        # Label with farmer inventory
        self.lbl_inventory = tk.Label(self)
        self.lbl_inventory.pack(side="top", padx=5, pady=5)

        # Frame for embedded Pygame display
        frm_embed = tk.Frame(self, width=410, height=410)
        frm_embed.pack(anchor="ne", side="top", padx=20, pady=0)
        self.grid()
        os.environ['SDL_WINDOWID'] = str(frm_embed.winfo_id())
        self.update()

        # Create an instance of embed_pygame
        self.embed_pygame_o = embed_pygame.EmbedPygame()

         # Start pygame loop in separate thread
        self.thread = threading.Thread(target=self.pygame_loop)
        self.thread.start()

        
    # a cheap/lazy way of preventing deadlock
    def pygame_loop(self):
        while True:
            with self.lock:
                self.embed_pygame_o.update()
                self.update_inventory()
            time.sleep(0.03)

    def start_level(self, level_number):   
        self.controller.levels.current_level = level_number
        self.current_farm_config = self.controller.levels.get_current_config()
        self.embed_pygame_o.farm = FarmGrid(config=self.current_farm_config)  # Reinitialize farm with new config
        self.display_level_task()

    def display_level_task(self):
        task = self.controller.levels.get_current_task()
        messagebox.showinfo(f"Level {self.controller.levels.current_level} Task", task)
        
    def update_inventory(self):
        if self.embed_pygame_o.farm and self.embed_pygame_o.farm.farmer:
            potatoes = self.embed_pygame_o.farm.farmer.inventory.count(0)
            carrots = self.embed_pygame_o.farm.farmer.inventory.count(1)                
            pumpkins = self.embed_pygame_o.farm.farmer.inventory.count(2)
            def update_label():
                self.lbl_inventory.config(
                    text="  INVENTORY:  Potatoes: {},  Carrots: {},  Pumpkins: {}  ".format(potatoes, carrots, pumpkins))

            self.lbl_inventory.after(0, update_label) # scheduling

    def handle_run(self):
        print("run")
        code = self.txt_code.get(1.0, "end-1c") # get user code from text box
        if code == "": # check if user has entered code
            messagebox.showerror(title="ERROR!", message="There is no code to run.")
        else:
            if self.controller.levels.get_test_cases()==False:  #handle single test cases
                self.embed_pygame_o.execute_python_code(code)  # execute user code

                if self.controller.levels.check_current_level_completion(self.embed_pygame_o.farm.stats): # check if level is completed
                    self.level_completed()
                    self.controller.frames[LevelsPage].update_level_buttons() 
                else:
                    self.level_failed()
            else:  # Handle multiple test cases
                # Retrieve the number of test cases for the current level
                num_test_cases = 3  # You want to run 3 test cases
                all_passed = True

                for _ in range(num_test_cases):
                    # Execute the user code
                    self.embed_pygame_o.execute_python_code(code)
                    
                    # Check if the level is completed for the current test case
                    if not self.controller.levels.check_current_level_completion(self.embed_pygame_o.farm.stats):
                        all_passed = False
                        break  # Exit loop if any test case fails

                    # Restart the farm for the next test case
                    self.embed_pygame_o.farm = FarmGrid(self.embed_pygame_o.FARM_WIDTH, self.embed_pygame_o.FARM_HEIGHT, config=self.controller.levels.get_current_config())
                
                # Call the appropriate method based on whether all test cases passed
                if all_passed:
                    self.level_completed()
                    self.controller.frames[LevelsPage].update_level_buttons()
                else:
                    self.level_failed()
                       

    def level_completed(self):
        self.controller.music_player.play_level_completion_sound()
        response = messagebox.askyesno("Level Complete", "Woohoo! Great job. Proceed to the next level?")
        if response:
            self.controller.levels.advance_to_next_level()
            self.start_level(self.controller.levels.current_level)
            self.controller.frames[LevelsPage].update_level_buttons()
        else:
            # Stay on the current level
            pass

    def level_failed(self):
        self.controller.music_player.play_level_fail_sound()
        response = messagebox.askretrycancel("Level Failed", "Oops! You didn't quite complete the task. Retry?")
        if response:
            # Reset the level
            self.start_level(self.controller.levels.current_level)
        else:
            # Go back to LevelsPage or stay on the GamePage
            pass

    def handle_clear(self):
        print("clear")
        self.txt_code.delete("1.0", "end-1c") # clear user code input text box

    def handle_restart(self):
        print("restart (farmgamegui)")
        if self.embed_pygame_o.farm:
            self.embed_pygame_o.farm.restart() # restart farm
            self.start_level(self.controller.levels.current_level)
        #self.controller.frames[GamePage].embed_pygame_o.farm = self.controller.levels.start_level(self.controller.levels.current_level) #stuf
        
    def handle_help(self):
        print("help")
        try:
            file = open("tutorial.txt", "r")
            win_tut = tk.Tk()
            win_tut.title("Tutorial")
            lbl_tut = tk.Label(win_tut, text=file.read(), justify="left", font=('Arial', 9))
            lbl_tut.pack()
            win_tut.mainloop()
            file.close()
        except IOError:
            print("Error: Could not write file")
    
    def handle_task(self):
        print("task")
        self.display_level_task()

    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage) # switch to home page

# TODO : Add level functionality
class LevelsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        #self.config(bg="green")
        self.controller = controller

        self.level_buttons = []

        btn_home = tk.Button(self, text="Home", command=self.handle_home)
        btn_home.pack(anchor="nw")
        max_levels = 8 # change this when adding more levels
        for level_number in range(1, max_levels+1):  # level buttons
            btn = tk.Button(self, text=f"Level {level_number}", command=lambda ln=level_number: self.start_level(ln))
            self.level_buttons.append(btn)
            btn.pack(anchor="center")

        self.update_level_buttons()
    
    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage)

    def update_level_buttons(self):
        for i, btn in enumerate(self.level_buttons):
            level_number = i + 1
            if self.controller.levels.is_level_unlocked(level_number):
                btn.config(state='normal')
            else:
                btn.config(state='disabled')

    def start_level(self, level_number):
        print("start level:", level_number)
        self.controller.frames[GamePage].start_level(level_number)
        self.controller.show_frame(GamePage)
    
class StatisticsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.config(bg="lime green")
        self.controller = controller

        '''Button: Home'''
        btn_home = tk.Button(self, text="Home", command=self.handle_home)
        btn_home.pack(anchor="nw")

        '''Lable: Title'''
        lbl_title = tk.Label(self, text="Statistics", font=("Comic Sans MS", 20, "bold"), fg="white", bg="lime green", anchor=tk.CENTER)
        lbl_title.pack(anchor="center", side="top", pady=20)

        '''Frame: Statistics'''
        self.frm_stats = tk.Frame(self, bg="lime green",padx=10, pady=10)

        PADX = 1
        PADY = 1
        WIDTH = 10
        BORDERWIDTH = 2
        RELIEF = "ridge"

        '''Label: Moves'''
        self.lbl_movement = tk.Label(self.frm_stats, text="Moves", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_movement.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky="ew")

        '''Label: Left Moves'''
        self.lbl_left_moves = tk.Label(self.frm_stats, text="Left", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_left_moves.grid(row=1, column=0, padx=PADX, pady=PADY)

        '''Label: Left Moves Value'''
        self.left_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("left"))
        self.lbl_left_moves_value = tk.Label(self.frm_stats, text=self.left_moves_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_left_moves_value.grid(row=1, column=1, padx=PADX, pady=PADY)

        '''Label: Right Moves'''
        self.lbl_right_moves = tk.Label(self.frm_stats, text="Right", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_right_moves.grid(row=2, column=0, padx=PADX, pady=PADY)

        '''Label: Right Moves Value'''
        self.right_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("right"))
        self.lbl_right_moves_value = tk.Label(self.frm_stats, text=self.right_moves_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_right_moves_value.grid(row=2, column=1, padx=PADX, pady=PADY)

        '''Label: Up Moves'''
        self.lbl_up_moves = tk.Label(self.frm_stats, text="Up", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_up_moves.grid(row=3, column=0, padx=PADX, pady=PADY)

        '''Label: Up Moves Value'''
        self.up_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("up"))
        self.lbl_up_moves_value = tk.Label(self.frm_stats, text=self.up_moves_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_up_moves_value.grid(row=3, column=1, padx=PADX, pady=PADY)

        '''Label: Down Moves'''
        self.down_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("down"))
        self.lbl_down_moves = tk.Label(self.frm_stats, text="Down", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_down_moves.grid(row=4, column=0, padx=PADX, pady=PADY)

        '''Label: Down Moves Value'''
        self.down_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("down"))
        self.lbl_down_moves_value = tk.Label(self.frm_stats, text=self.down_moves_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_down_moves_value.grid(row=4, column=1, padx=PADX, pady=PADY)

        '''Label: Crops'''
        self.lbl_crops = tk.Label(self.frm_stats, text="Crops", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_crops.grid(row=0, column=2, padx=PADX, pady=PADY)

        '''Label: Planted'''
        self.lbl_planting = tk.Label(self.frm_stats, text="Planted", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_planting.grid(row=0, column=3, padx=PADX, pady=PADY)

        '''Label: Potatoes Planted'''
        self.lbl_potatoes_planted = tk.Label(self.frm_stats, text="Potatoes", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_potatoes_planted.grid(row=1, column=2, padx=PADX, pady=PADY)

        '''Label: Potatoes Planted Value'''
        self.potatoes_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_potatoes_planted())
        self.lbl_potatoes_planted_value = tk.Label(self.frm_stats, text=self.potatoes_planted_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_potatoes_planted_value.grid(row=1, column=3, padx=PADX, pady=PADY)

        '''Label: Carrots Planted'''
        self.lbl_carrots_planted = tk.Label(self.frm_stats, text="Carrots", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_carrots_planted.grid(row=2, column=2, padx=PADX, pady=PADY)

        '''Label: Carrots Planted Value'''
        self.carrots_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_carrots_planted())
        self.lbl_carrots_planted_value = tk.Label(self.frm_stats, text=self.carrots_planted_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_carrots_planted_value.grid(row=2, column=3, padx=PADX, pady=PADY)

        '''Label: Pumpkins Planted'''
        self.lbl_pumpkins_planted = tk.Label(self.frm_stats, text="Pumpkins", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_pumpkins_planted.grid(row=3, column=2, padx=PADX, pady=PADY)

        '''Label: Pumpkins Planted Value'''
        self.pumpkins_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_pumpkins_planted())
        self.lbl_pumpkins_planted_value = tk.Label(self.frm_stats, text=self.pumpkins_planted_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_pumpkins_planted_value.grid(row=3, column=3, padx=PADX, pady=PADY)

        '''Label: Harvested'''
        self.lbl_harvesting = tk.Label(self.frm_stats, text="Harvested", width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_harvesting.grid(row=0, column=4, padx=PADX, pady=PADY)

        '''Label: Potatoes Planted Value'''
        self.potatoes_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_potatoes_harvested())
        self.lbl_potatoes_harvested_value = tk.Label(self.frm_stats, text=self.potatoes_harvested_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_potatoes_harvested_value.grid(row=1, column=4, padx=PADX, pady=PADY)

        '''Label: Carrots Planted Value'''
        self.carrots_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_carrots_harvested())
        self.lbl_carrots_harvested_value = tk.Label(self.frm_stats, text=self.carrots_harvested_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_carrots_harvested_value.grid(row=2, column=4, padx=PADX, pady=PADY)

        '''Label: Pumpkins Planted Value'''
        self.pumpkins_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_pumpkins_harvested())
        self.lbl_pumpkins_harvested_value = tk.Label(self.frm_stats, text=self.pumpkins_harvested_value, width=WIDTH, borderwidth=BORDERWIDTH, relief=RELIEF)
        self.lbl_pumpkins_harvested_value.grid(row=3, column=4, padx=PADX, pady=PADY)

        '''Pack Statistics Frame'''
        self.frm_stats.pack(anchor="center", padx=20, pady=20)
    
    def refresh(self):
        '''Refresh Left Moves'''
        self.left_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("left"))
        self.lbl_left_moves_value.config(text=self.left_moves_value)

        '''Refresh Right Moves'''
        self.right_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("right"))
        self.lbl_right_moves_value.config(text=self.right_moves_value)

        '''Refresh Up Moves'''
        self.up_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("up"))
        self.lbl_up_moves_value.config(text=self.up_moves_value)

        '''Refesh Down Moves'''
        self.down_moves_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_moves("down"))
        self.lbl_down_moves_value.config(text=self.down_moves_value)

        '''Refresh Potatoes Planted'''
        self.potatoes_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_potatoes_planted())
        self.lbl_potatoes_planted_value.config(text=self.potatoes_planted_value)

        '''Refresh Carrots Planted'''
        self.carrots_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_carrots_planted())
        self.lbl_carrots_planted_value.config(text=self.carrots_planted_value)

        '''Refresh Pumpkins Planted'''
        self.pumpkins_planted_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_pumpkins_planted())
        self.lbl_pumpkins_planted_value.config(text=self.pumpkins_planted_value)

        '''Refresh Potatoes Harvested'''
        self.potatoes_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_potatoes_harvested())
        self.lbl_potatoes_harvested_value.config(text=self.potatoes_harvested_value)

        '''Refresh Carrots Harvested'''
        self.carrots_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_carrots_harvested())
        self.lbl_carrots_harvested_value.config(text=self.carrots_harvested_value)

        '''Refresh Pumpkins Harvested'''
        self.pumpkins_harvested_value = str(self.controller.frames[GamePage].embed_pygame_o.farm.stats.get_pumpkins_harvested())
        self.lbl_pumpkins_harvested_value.config(text=self.pumpkins_harvested_value)

    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage)

# TODO : Add settings functionality 
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg="LightBlue4")

        '''Button: Home'''
        btn_home = tk.Button(self, text="Home", command=self.handle_home)
        btn_home.pack(anchor="nw")

        '''Lable: Title'''
        lbl_title = tk.Label(self, text="Settings", font=("Comic Sans MS", 20, "bold"), fg="white", bg="LightBlue4", anchor=tk.CENTER)
        lbl_title.pack(anchor="center", side="top", pady=20)

        '''Checkbutton: Slow Mode'''
        self.slow_mode = tk.IntVar(value=1)
        self.chk_slow_mode = tk.Checkbutton(self, text="Slow Mode", variable=self.slow_mode, onvalue=1, offvalue=0, command=self.handle_slow_mode)
        self.chk_slow_mode.config(fg="black", bg="LightBlue4")
        self.chk_slow_mode.pack(anchor="center")

        '''Checkbutton: Mute background music'''
        self.mute = tk.IntVar(value=1)
        self.chk_mute = tk.Checkbutton(self, text="Music off", variable=self.mute, onvalue=1, offvalue=0, command=self.handle_mute)
        self.chk_mute.config(fg="black", bg="LightBlue4")
        self.chk_mute.pack(anchor="center")
    
    def handle_home(self):
        print("home")
        self.controller.show_frame(HomePage)

    def handle_mute(self):
        if self.mute.get() == 1:
            self.controller.music_player.stop_background_music()
            print("MUTED")
        else:
            self.controller.music_player.play_background_music()
            print("MUSIC ON")
    
    def handle_slow_mode(self):
        if self.slow_mode.get() == 1:
            self.controller.frames[GamePage].embed_pygame_o.slow_mode = True
            print("SLOWMODE ON")
        else:
            self.controller.frames[GamePage].embed_pygame_o.slow_mode = False
            print("SLOWMODE OFF")