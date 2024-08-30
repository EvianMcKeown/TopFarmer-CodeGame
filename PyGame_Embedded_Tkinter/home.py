import tkinter as tk
import os

def init():

    def click_new_game():
        root.destroy()

    def click_continue():
        pass

    def click_levels():
        pass

    def click_settings():
        pass

    SCREEN_WIDTH=900
    SCREEN_HEIGHT=450

    root = tk.Tk()
    root.title("FarmGame")
    root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))
    root.configure(background='sky blue')

    title_label = tk.Label(text="TopFarmer", font=("Comic Sans MS", 20, "bold"), fg="white", bg="sky blue", anchor=tk.CENTER)
    title_label.pack(pady=20)

    newgame_button = tk.Button(text= "New Game", bg="white", width=10, anchor=tk.CENTER, command=click_new_game)
    newgame_button.pack(pady=20)

    continue_button = tk.Button(text= "Continue", bg="white", width=10, anchor=tk.CENTER, command=click_continue)
    continue_button.pack(pady=20)

    levels_button = tk.Button(text= "Levels", bg="white", width=10, anchor=tk.CENTER, command=click_levels)
    levels_button.pack(pady=20)

    settings_button = tk.Button(text= "Settings", bg="white", width=10, anchor=tk.CENTER, command=click_settings)
    settings_button.pack(pady=20)

    root.mainloop()