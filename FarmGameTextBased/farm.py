# Text based farm game demo (farm module)
# By Mustafa Mohamed
# 2 August 2024

import random

class Farmer:
    crop_desc = {0:"potato", 1:"carrot", 2:"pumpkin"}
    def __init__(self, farm, x=0, y=0):
        self.farm = farm
        self.symbol = '$'
        self.x = x
        self.y = y
        
        # give farmer 5 of each crop
        self.inventory = []
        for i in range(5):
            self.inventory.append(0)
            self.inventory.append(1)
            self.inventory.append(2)

    def __str__(self):
        return self.symbol

    def get_pos(self):
        return (self.x, self.y)
    
    def add_inventory(self, crop):
        self.inventory.append(crop)
    
    def remove_inventory(self, crop):
        #TODO Check if there is something to remove before doing it
        self.inventory.remove(crop)

    def get_inventory(self):
        return {self.crop_desc[crop]:self.inventory.count(crop) for crop in self.inventory}
    
    def move(self, direction):
        '''Move to a non-obstacle tile next to the farmer'''
        match direction:
            case 'u':
                dest = (self.x, self.y-1)
            case 'd':
                dest = (self.x, self.y+1)
            case 'l':
                dest = (self.x-1, self.y)
            case 'r':
                dest = (self.x+1, self.y)
        
        if self.farm.walkable(dest) and not self.farm.out_of_bounds(dest):
            self.x, self.y = dest

    def plant(self, direction, crop):
        '''Plant a crop on a dirt tile next to the farmer'''
        match direction:
            case 'u':
                dest = (self.x, self.y-1)
            case 'd':
                dest = (self.x, self.y+1)
            case 'l':
                dest = (self.x-1, self.y)
            case 'r':
                dest = (self.x+1, self.y)
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 0 and crop in self.inventory:
            #TODO Check if plant is in inventory before planting
            self.inventory.remove(crop)
            self.farm.grid[dest[0]][dest[1]] = CropTile(dest[0], dest[1], crop)

    def harvest(self, direction):
        ''' Harvest a crop from a crop tile next to the farmer'''
        match direction:
            case 'u':
                dest = (self.x, self.y-1)
            case 'd':
                dest = (self.x, self.y+1)
            case 'l':
                dest = (self.x-1, self.y)
            case 'r':
                dest = (self.x+1, self.y)
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 3:
            self.inventory.append(self.farm.grid[dest[0]][dest[1]].crop_type)
            self.farm.grid[dest[0]][dest[1]].tile_type = 0


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
        self.generate_farm()

    def generate_farm(self):
        '''Generates dirt farm with river and bridge'''
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        river_location = random.randrange(1, self.height -1)
        bridge_location = random.randrange(1, self.width - 1)
        for y in range(self.height):
            for x in range(self.width):
                # Start with dirt
                self.grid[x][y] = FarmTile(x, y, 0)
                # Place river somehere along farm height
                if y == river_location:
                    self.grid[x][y] = FarmTile(x, y, 2)
                    # Place bridge somewhere along river
                    if x == bridge_location:
                        self.grid[x][y] = FarmTile(x, y, 0)

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
        return not((0 <= x < self.width) and (0 <= y < self.height))
    
    def walkable(self, pos):
        x, y = pos
        return not self.out_of_bounds((x, y)) and self.grid[x][y].tile_type < 2

    def add_farmer(self, x=0, y=0):
        if self.farmer == None:
            if self.grid[x][y].tile_type < 2 and not self.out_of_bounds((x, y)):
                self.farmer = Farmer(self, x, y)
    
    def remove_farmer(self):
        if self.farmer != None:
            self.farmer = None