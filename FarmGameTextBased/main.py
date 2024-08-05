# Text based farm game demo (main)
# By Mustafa Mohamed
# 2 August 2024

import sys
from time import sleep
from farm import *

def main():
    fg = FarmGrid(10, 10)
    fg.add_farmer()
    fg.print()

    while True:
        instructions = input("Enter intructions: ").lower().split()
        for ins in instructions:
            match ins:
                case "u" | "d" | "l" | "r":
                    fg.farmer.move(ins[0])
                case "pu" | "pd" | "pl" | "pr":
                    fg.farmer.plant(ins[1])
                case "hu" | "hd" | "hl" | "hr":
                    fg.farmer.harvest(ins[1])
                case "exit":
                    sys.exit(0)
                case _:
                    print("Invalid instruction(s)")
            sleep(0.5)
            fg.print()

if __name__ == "__main__":
    main()
