# Text based farm game demo (main)
# By Mustafa Mohamed
# 2 August 2024

from time import sleep
from farm import *

def main():
    fg = FarmGrid(10, 10)
    fg.add_farmer()
    fg.display()

    while True:
        instructions = input("Enter intructions: ").lower().split()
        for ins in instructions:
            match ins:
                case "up" | "down" | "left" | "right":
                    fg.farmer.move(ins)
                case "exit":
                    sys.exit(0)
                case _:
                    print("Invalid instruction(s)")
            sleep(0.5)
            fg.display()

if __name__ == "__main__":
    main()
