# Text based farm game demo (farm module)
# By Mustafa Mohamed
# 2 August 2024

import random

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
        if direction == "u" and self.farm.grid[self.x][self.y-1].tile_type < 2:
            self.y -= 1
        if direction == "d" and self.farm.grid[self.x][self.y+1].tile_type < 2:
            self.y += 1
        if direction == "l" and self.farm.grid[self.x-1][self.y].tile_type < 2:
            self.x -= 1
        if direction == "r" and self.farm.grid[self.x+1][self.y].tile_type < 2:
            self.x += 1
    def plant(self, direction):
        if direction == "u" and self.farm.grid[self.x][self.y-1].tile_type == 0:
            self.farm.grid[self.x][self.y-1].tile_type = 3
            return
        if direction == "d" and self.farm.grid[self.x][self.y+1].tile_type == 0:
            self.farm.grid[self.x][self.y+1].tile_type = 3
            return
        if direction == "l" and self.farm.grid[self.x-1][self.y].tile_type == 0:
            self.farm.grid[self.x-1][self.y].tile_type = 3
            return
        if direction == "r" and self.farm.grid[self.x+1][self.y].tile_type == 0:
            self.farm.grid[self.x+1][self.y].tile_type = 3
            return
    def harvest(self, direction):
        if direction == "u" and self.farm.grid[self.x][self.y-1].tile_type == 3:
            self.farm.grid[self.x][self.y-1].tile_type = 0
            return
        if direction == "d" and self.farm.grid[self.x][self.y+1].tile_type == 3:
            self.farm.grid[self.x][self.y+1].tile_type = 0
            return
        if direction == "l" and self.farm.grid[self.x-1][self.y].tile_type == 3:
            self.farm.grid[self.x-1][self.y].tile_type = 0
            return
        if direction == "r" and self.farm.grid[self.x+1][self.y].tile_type == 3:
            self.farm.grid[self.x+1][self.y].tile_type = 0
            return


class FarmTile:
    tile_desc = {0:"dirt",1:"grass",2:"water",3:"crop"}
    def __init__(self, x, y, tile_type=0):
        self.tile_type = tile_type
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.tile_desc[self.tile_type])
    def get_pos(self):
        return (self.x, self.y)

class FarmGrid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.farmer = None
        self.grid = []
        self.generate_farm()

    def generate_farm(self):
        # Initialise empty grid and populate it with tiles
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        bridge_location = random.randrange(1, self.width - 1)
        for y in range(self.height):
            for x in range(self.width):
                # Start with dirt
                self.grid[x][y] = FarmTile(x, y, 0)
                # Place river half way through farm height
                if y == int(self.height / 2):
                    self.grid[x][y] = FarmTile(x, y, 2)
                    # Place bridge somewhere along the river
                    if x == bridge_location:
                        self.grid[x][y] = FarmTile(x, y, 0)

    def __str__(self):
        # Returns a string with information about the farm
        farmer_x, farmer_y = self.farmer.get_pos()
        string = "width={}, height={}\n".format(self.width, self.height)
        string += "farmer_position={}\n".format((farmer_x, farmer_y))
        string += "farmer_on={}\n".format(self.grid[farmer_x][farmer_y])
        for y in range(self.height):
            for x in range(self.width):
                if (farmer_x, farmer_y) == (x, y):
                    symbol = self.farmer.symbol
                else:
                    symbol = str(self.grid[x][y].tile_type)
                    
                string += symbol + ' '
            string += '\n'
        if self.out_of_bounds():
            string += "The farmer fell off the farm. He is dead.\n"
        return string

    def print(self):
        print(self)

    def add_farmer(self, x=0, y=0):
        self.farmer = Farmer(self, x, y)

    def out_of_bounds(self):
        x, y = self.farmer.get_pos()
        if not((0 <= x < self.width) and (0 <= y < self.height)):
            self.farmer = None
            return True
        return False
