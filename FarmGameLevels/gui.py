# gui popups stuffs
import tkinter as tk

def show_task_window(task, start_level_callback):
    root = tk.Tk()
    root.geometry("400x200")
    label = tk.Label(root, text=task, font=("consolas", 16))
    label.pack(pady=20)
    button = tk.Button(root, text="Start", command=lambda: start_level_callback(root))
    button.pack()
    root.mainloop()

def show_congratulations_window(next_level_callback):
    root = tk.Tk()
    root.geometry("400x200")
    label = tk.Label(root, text="Yippee! You did the thing!", font=("consolas", 16))
    label.pack(pady=20)
    button = tk.Button(root, text="Next Level", command=lambda: next_level_callback(root))
    button.pack()
    root.mainloop()

def show_failure_window(retry_level_callback):
    root = tk.Tk()
    root.geometry("400x200")
    label = tk.Label(root, text="Womp womp! Try again.", font=("consolas", 16))
    label.pack(pady=20)
    button = tk.Button(root, text="Try Again", command=lambda: retry_level_callback(root))
    button.pack()
    root.mainloop()

def show_help_window():
    message = "Move the farmer: farmer.move(\"direction\")\n"
    message +="direction can be left, right, up, down\n\n"
    message +="Plant a crop: farmer.plant(\"crop\", \"direction\")\n"
    message +="crop can be potato, carrot, pumpkin\n\n"
    message +="Harvest a crop: farmer.harvest(\"direction\")\n\n"
    root = tk.Tk()
    root.geometry("400x200")
    w = tk.Label(root, text ='How to play', font = "50")  
    w.pack() 
    msg = tk.Message(root, text=message, width=600)   
    msg.pack()
    root.mainloop()