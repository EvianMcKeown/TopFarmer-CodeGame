import tkinter as tk
import os

SCREEN_WIDTH=800
SCREEN_HEIGHT=400

root = tk.Tk()
root.title("FarmGame")
root.geometry("{}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))

l_input = tk.Label(text="Enter code here:")
t_input = tk.Text(width=47, height=20)
l_input.place(x=0, y=0)
t_input.place(x=0, y=20)

def handle_button():
    code = t_input.get(1.0, "end-1c")
    pygamegui.execute_python_code(code)

b_run = tk.Button(text="Run", width=5, command=handle_button)
b_clear = tk.Button(text="Clear", width=5)
b_restart = tk.Button(text="Restart",width=5)
b_help = tk.Button(text="Help", width=5)

b_run.place(x=0, y=366)

embed = tk.Frame(root, width=400, height=400)
embed.pack(side="right")
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
root.update()

import pygamegui

while True:
    pygamegui.update()
    root.update()