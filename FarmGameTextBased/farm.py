# Text based farm game demo (farm module)
# By Mustafa Mohamed
# 2 August 2024

import sys

class Crop:
    def __int__(self, x, y):
        self.symbol = '#'
        self.x = x
        self.y = y

class Farmer:
    def __init__(self, farm, x=0, y=0):
        self.farm = farm
        self.symbol = '$'
        self.x = x
        self.y = y
    def __str__(self):
        return self.symbol
    def get_pos(self):
        return (self.x, self.y)
    def move(self, direction):
        if direction == "up" and self.farm.grid[self.x][self.y-1].tile_type != 2:
            self.y -= 1
        if direction == "down" and self.farm.grid[self.x][self.y+1].tile_type != 2:
            self.y += 1
        if direction == "left" and self.farm.grid[self.x-1][self.y].tile_type != 2:
            self.x -= 1
        if direction == "right" and self.farm.grid[self.x+1][self.y].tile_type != 2:
            self.x += 1
    def plant(self, crop):
        pass
    def harvest(self):
        pass

'''
For example:
tile_type:
    0 = dirt (can walk and plant)
    1 = grass (can only walk)
    2 = water (cannot walk or plant)
'''
class FarmTile:
    def __init__(self, x, y, tile_type=0):
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
        self.grid = [[None for _ in range(height)] for _ in range(width)]
        for y in range(self.height):
            for x in range(self.width):
                self.grid[x][y] = FarmTile(x, y, 0)

                # Place river half way through farm height
                if y == int(self.height / 2):
                    self.grid[x][y] = FarmTile(x, y, 2)

    def __str__(self):
        # Returns a string with information about the farm
        # and a text representation of the farm
        string = "width={}, height={}\n".format(self.width, self.height)
        string += "farmer_pos={}\n".format(self.farmer.get_pos())
        for y in range(self.height):
            for x in range(self.width):
                if self.farmer.get_pos() == (x, y):
                    symbol = self.farmer.symbol
                else:
                    symbol = str(self.grid[x][y])
                    
                string += symbol + ' '
            string += '\n'
        if self.out_of_bounds():
            string += "The farmer fell off the farm. He is dead.\n"
        return string

    def display(self):
        print(self)

    def add_farmer(self, x=0, y=0):
        self.farmer = Farmer(self, x, y)

    def out_of_bounds(self):
        x, y = self.farmer.get_pos()
        if not((0 <= x < self.width) and (0 <= y < self.height)):
            self.farmer = None
            return True
        return False
