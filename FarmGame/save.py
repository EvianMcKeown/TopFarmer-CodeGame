from farm import *
import json

def save(filename, farm, code):
    file = open(filename, "w")
    file.write("farm:\n{}\ncode:\n{}".format(farm, code))
    file.close()

def load(filename, farm, code):
    file = open(filename, "r")
    for num, line in enumerate(file, 1):
        if line.startswith("width="):
            width = int(line.strip("\n")[6:])
        if line.startswith("height="):
            height = int(line.strip("\n")[7:])
        if line.startswith("farmer_x="):
            farmer_x = int(line.strip("\n")[9:])
        if line.startswith("farmer_y="):
            farmer_y = int(line.strip("\n")[9:])
        if line.startswith("farmer_inventory="):
            inventory = json.loads(line.strip("\n")[17:])
        if line.startswith("code:"):
            code_starts = num
    file.close()
    file2 = open(filename, "r")
    code = "".join(file2.readlines()[code_starts:])
    farmer = Farmer().load_save(farmer_x, farmer_y, inventory)
    return width, height, farmer, code,  [[None for _ in range(height)] for _ in range(width)]