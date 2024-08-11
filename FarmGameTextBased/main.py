# Text-based farm game demo
# Author: Mustafa Mohamed
# Created: 2 August 2024
# Modified: 10 August 2024

import sys
from time import sleep
from farm import *

FARM_WIDTH = 10
FARM_HEIGHT = 10

# Initialise farm
fg = FarmGrid(FARM_WIDTH, FARM_HEIGHT)
fg.add_farmer(0, 0)
fg.print()

# Terminal input/output
while True:
    instructions = input("Enter intructions:").lower().split()
    for ins in instructions:
        match ins:
            case "mu" | "md" | "ml" | "mr":
                fg.farmer.move(ins[1])
            case "pu" | "pd" | "pl" | "pr":
                fg.farmer.plant(ins[1], 0)
            case "hu" | "hd" | "hl" | "hr":
                fg.farmer.harvest(ins[1])
            case "exit":
                sys.exit(0)
            case _:
                print("Invalid instruction(s)")
        sleep(0.5)
        fg.print()
