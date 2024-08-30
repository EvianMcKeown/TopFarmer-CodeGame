import tkinter as tk
from tkinter import messagebox
import os

import home

home.init()

def init():
    SCREEN_WIDTH=900
    SCREEN_HEIGHT=450

    root = tk.Tk()
    root.title("FarmGame")
    root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

    f_input = tk.Frame()

    l_input = tk.Label(f_input, text="Enter code here:")
    l_input.pack(anchor="w")

    t_input = tk.Text(f_input, width=50, height=20)
    t_input.pack(anchor="w")

    def handle_run():
        code = t_input.get(1.0, "end-1c")
        if code == "":
            messagebox.showerror(title="ERROR!", message="You tried to run code but there is no code to run.")
        pygamegui.execute_python_code(code)

    def handle_clear():
        t_input.delete("1.0", "end-1c")

    def handle_restart():
        handle_clear()
        pygamegui.farm.__init__()

    def handle_help():
        messagebox.showinfo(title="How to play", message="How to play...\n(coming soon)")

    def handle_home():
        root.destroy()
        home.init()

    b_run = tk.Button(f_input, text="Run", width=5, command=handle_run)
    b_clear = tk.Button(f_input, text="Clear", width=5, command=handle_clear)
    b_restart = tk.Button(f_input, text="Restart",width=5, command=handle_restart)
    b_help = tk.Button(f_input, text="Help", width=5, command=handle_help)
    b_home = tk.Button(f_input, text="Home", width=5, command=handle_home)

    b_run.pack(anchor="s", side="left", pady=5)
    b_clear.pack(anchor="s", side="left", pady=5)
    b_restart.pack(anchor="s", side="left", pady=5)
    b_help.pack(anchor="s", side="left", pady=5)
    b_home.pack(anchor="s", side="left", pady=5)

    f_input.pack(anchor="nw", side="left", padx=20, pady=20)

    embed = tk.Frame(root, width=400, height=400)
    embed.pack(anchor="ne", side="top", padx=20, pady=20)
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    root.update()
    import pygamegui

    while True:
        pygamegui.update()
        root.update()

init()