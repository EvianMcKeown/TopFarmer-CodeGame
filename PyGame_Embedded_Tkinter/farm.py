# Text based farm game demo (farm module)
# By Mustafa Mohamed
# modified 13 Aug 2024 by Zahra Bawa
import random
from stats import FarmStats

class Farmer:
    crop_desc = {0: "potato", 1: "carrot", 2: "pumpkin"}
    
    def __init__(self, farm, x=0, y=0):
        self.farm = farm
        self.symbol = '$'
        self.x = x
        self.y = y
        
        # Give the farmer 5 of each crop
        self.inventory = [0, 1, 2] * 5

    def __str__(self):
        return self.symbol

    def get_pos(self):
        return (self.x, self.y)
    
    def add_inventory(self, crop):
        self.inventory.append(crop)
    
    def remove_inventory(self, crop):
        self.inventory.remove(crop)

    def get_inventory(self):
        return {self.crop_desc[crop]: self.inventory.count(crop) for crop in set(self.inventory)}
    
    def move(self, direction):
        '''Move to a non-obstacle tile next to the farmer'''
        dest = {
            'up': (self.x, self.y - 1),
            'down': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'right': (self.x + 1, self.y)
        }.get(direction, self.get_pos())
        
        if self.farm.walkable(dest) and not self.farm.out_of_bounds(dest):
            self.x, self.y = dest
            self.farm.stats.add_moves(direction)

    def plant(self, crop, direction):
        '''Plant a crop on a dirt tile next to the farmer'''
        crop = {v: k for k, v in self.crop_desc.items()}.get(crop) # invert dictionary
        dest = {
            'up': (self.x, self.y - 1),
            'down': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'right': (self.x + 1, self.y)
        }.get(direction, self.get_pos())
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 0 and crop in self.inventory:
            self.inventory.remove(crop)
            self.farm.grid[dest[0]][dest[1]] = CropTile(dest[0], dest[1], crop)
            self.farm.stats.add_crops_planted(self.crop_desc[crop])


    def harvest(self, direction):
        '''Harvest a crop from a crop tile next to the farmer'''
        dest = {
            'up': (self.x, self.y - 1),
            'down': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'right': (self.x + 1, self.y)
        }.get(direction, self.get_pos())
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 3:
            crop = self.farm.grid[dest[0]][dest[1]].crop_type
            self.inventory.append(crop)
            self.farm.grid[dest[0]][dest[1]].tile_type = 0
            self.farm.stats.add_crops_harvested(self.crop_desc[crop])
            print("HARVEST POTATO:  ", self.farm.stats.get_potatoes_harvested())
            print("HARVEST CARROT:  ", self.farm.stats.get_carrots_harvested())
            print("HARVEST PUMPKIN: ", self.farm.stats.get_pumpkins_harvested())
            print("HARVEST TOTAL:   ", self.farm.stats.get_total_harvested())

class FarmTile:
    tile_desc = {0: "dirt", 1: "grass", 2: "water", 3: "crop", 4: "tree"}

    def __init__(self, x, y, tile_type=0):
        self.tile_type = tile_type
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.tile_desc[self.tile_type])
    
    def get_pos(self):
        return (self.x, self.y)

class CropTile(FarmTile):
    def __init__(self, x, y, crop_type=0):
        super().__init__(x, y, 3)
        self.crop_type = crop_type

class FarmGrid:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.farmer = None
        self.grid = []
        self.stats = FarmStats()
        self.generate_farm()
        self.add_farmer(0, 0)

    def generate_farm(self):
        # initialise empty grid
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]

        # determine river orientation (0=horizontal, 1=vertical)
        river_orientation = random.randrange(2)
        if river_orientation == 0:
            river_range = self.height
        else:
            river_range = self.width
        
        # determine start and end point of river
        river_start = random.randrange(3, river_range - 3)
        river_end = random.randrange(3, river_range - 3)

        # generate farm with river and dirt next to river
        for y in range(self.height):
            for x in range(self.width):
                if river_orientation == 0:
                    if y == int(x*(river_start-river_end)/(self.width)+river_start):
                        self.grid[x][y] = FarmTile(x, y, 2) # water
                        self.grid[x][y-1] = FarmTile(x, y, 0) # dirt
                    else:
                        self.grid[x][y] = FarmTile(x, y, 1) # grass
                else:
                    if x == int(y*(river_start-river_end)/(self.width)+river_start):
                        self.grid[x][y] = FarmTile(x, y, 2) # water
                        self.grid[x-1][y] = FarmTile(x, y, 0) # dirt
                    else:
                        self.grid[x][y] = FarmTile(x, y, 1) # grass
        
        # place a tree somwhere on the grass
        while True:
            tree_x = random.randrange(1, self.width - 1)
            tree_y = random.randrange(1, self.height - 1)
            if self.grid[tree_x][tree_y].tile_type == 1:
                break
        self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4) # tree

    def __str__(self):
        '''Returns a text representation of the farm'''
        farmer_x, farmer_y = self.farmer.get_pos()
        string = "width={}, height={}\n".format(self.width, self.height)
        string += "farmer_position={} ({})\n".format((farmer_x, farmer_y), self.grid[farmer_x][farmer_y])
        string += "farmer_inventory={}\n".format(self.farmer.get_inventory())
        for y in range(self.height):
            for x in range(self.width):
                if (farmer_x, farmer_y) == (x, y):
                    symbol = self.farmer.symbol
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
        if self.farmer is None:
            if self.grid[x][y].tile_type < 2 and not self.out_of_bounds((x, y)):
                self.farmer = Farmer(self, x, y)
    
    def remove_farmer(self):
        if self.farmer is not None:
            self.farmer = None
