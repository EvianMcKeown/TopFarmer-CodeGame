import random
from farmtile import FarmTile
from farmer import Farmer

class FarmGrid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.farmer = None
        self.grid = []
        self.generate_farm()

    def generate_farm(self):
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        river_location = random.randrange(1, self.height - 1)
        bridge_location = random.randrange(1, self.width - 1)
        for y in range(self.height):
            for x in range(self.width):
                self.grid[x][y] = FarmTile(x, y, 0)
                if y == river_location:
                    self.grid[x][y] = FarmTile(x, y, 2)
                    if x == bridge_location:
                        self.grid[x][y] = FarmTile(x, y, 0)

    def __str__(self):
        farmer_x, farmer_y = self.farmer.get_pos() if self.farmer else (-1, -1)
        string = "width={}, height={}\n".format(self.width, self.height)
        if self.farmer:
            string += "farmer_position={} ({})\n".format((farmer_x, farmer_y), self.grid[farmer_x][farmer_y])
            string += "farmer_inventory={}\n".format(self.farmer.get_inventory())
        for y in range(self.height):
            for x in range(self.width):
                if (farmer_x, farmer_y) == (x, y):
                    symbol = self.farmer.symbol if self.farmer else ' '
                else:
                    symbol = str(self.grid[x][y].tile_type)
                string += symbol + ' '
            string += '\n'
        return string

    def print(self):
        print(self)
    
    def out_of_bounds(self, pos):
        x, y = pos
        return not (0 <= x < self.width and 0 <= y < self.height)
    
    def walkable(self, pos):
        x, y = pos
        return not self.out_of_bounds((x, y)) and self.grid[x][y].tile_type < 2

    def add_farmer(self, x=0, y=0):
        if self.farmer is None and not self.out_of_bounds((x, y)) and self.grid[x][y].tile_type < 2:
            self.farmer = Farmer(self, x, y)
    
    def remove_farmer(self):
        if self.farmer is not None:
            self.farmer = None
