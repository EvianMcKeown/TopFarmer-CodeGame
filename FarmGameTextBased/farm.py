# Text based farm game demo (farm module)
# By Mustafa Mohamed
# 2 August 2024

import sys

class Farmer:
    def __init__(self, x=0, y=0):
        self.symbol = '$'
        self.x = x
        self.y = y
    def __str__(self):
        return self.symbol
    def get_pos(self):
        return (self.x, self.y)
    def move_up(self):
        self.y -= 1
    def move_down(self):
        self.y += 1
    def move_left(self):
        self.x -= 1
    def move_right(self):
        self.x += 1

'''
For example:
tile_type:
    0 = dirt
    1 = grass
    2 = water
'''
class FarmTile:
    def __init__(self, x=0, y=0, tile_type=0):
        self.tile_type = tile_type
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.tile_type)
    def get_pos(self):
        return (self.x, self.y)

class FarmGrid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.farmer = None
        
        # Initialise empty grid and populate it with tiles
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = FarmTile(x, y, 0)

    def __str__(self):
        # Returns a string with information about the farm
        # and a text representation of the farm
        string = "width={}, height={}\n".format(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                symbol = str(self.grid[y][x])
                if self.farmer.get_pos() == (x, y):
                    symbol = self.farmer.symbol
                string += symbol + ' '
            string += '\n'
        self.check_bounds()
        return string

    def display(self):
        print(self)

    def add_farmer(self, x=0, y=0):
        self.farmer = Farmer(x, y)

    def check_bounds(self):
        x, y = self.farmer.get_pos()
        if not((0 <= x < self.width) and (0 <= y < self.height)):
            self.farmer = None
            print("The farmer fell off the farm. He is dead.")
            sys.exit(0)
