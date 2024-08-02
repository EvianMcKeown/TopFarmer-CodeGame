# Text based farm game demo (main)
# By Mustafa Mohamed
# 2 August 2024

from time import sleep
from Farm import *

def main():
    fg = FarmGrid(10, 10)
    fg.add_farmer()
    fg.display()

    while True:
        instructions = input("Enter intructions: ").lower().split()
        for i in instructions:
            match i:
                case "up":
                    fg.farmer.move_up()
                case "down":
                    fg.farmer.move_down()
                case "left":
                    fg.farmer.move_left()
                case "right":
                    fg.farmer.move_right()
                case "exit":
                    sys.exit(0)
                case _:
                    print("Invalid instruction(s)")
            fg.display()
            sleep(0.5)

if __name__ == "__main__":
    main()
