
from farmtile import  CropTile


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

    def plant(self, crop, direction):
        '''Plant a crop on a dirt tile next to the farmer'''
        crop = {v: k for k, v in self.crop_desc.items()}.get(crop)
        dest = {
            'up': (self.x, self.y - 1),
            'down': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'right': (self.x + 1, self.y)
        }.get(direction, self.get_pos())
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 0 and crop in self.inventory:
            self.inventory.remove(crop)
            self.farm.grid[dest[0]][dest[1]] = CropTile(dest[0], dest[1], crop)

    def harvest(self, direction):
        '''Harvest a crop from a crop tile next to the farmer'''
        dest = {
            'up': (self.x, self.y - 1),
            'down': (self.x, self.y + 1),
            'left': (self.x - 1, self.y),
            'right': (self.x + 1, self.y)
        }.get(direction, self.get_pos())
        
        if self.farm.grid[dest[0]][dest[1]].tile_type == 3:
            self.inventory.append(self.farm.grid[dest[0]][dest[1]].crop_type)
            self.farm.grid[dest[0]][dest[1]].tile_type = 0

