import random
from farmer import Farmer
from farmtile import FarmTile, CropTile
from stats import FarmStats

class FarmGrid:
    def __init__(self, width=10, height=10, config='plain'):
        self.width = width
        self.height = height
        self.farmer = None
        self.grid = []
        self.stats = FarmStats(self)
        self.config = config
        self.generate_farm()
        self.add_farmer(0, 0)


    def generate_farm(self):        # generates farm based on chosen config type
        if self.config == 'plain':
            self.generate_plain()
        elif self.config == 'river':
            self.generate_river()
        elif self.config == 'tree_river':
            self.generate_tree_river()
        elif self.config == 'grass':
            self.generate_grass()
        elif self.config == 'crops':
            self.generate_crops()
        elif self.config == 'tree_dirt':
            self.generate_tree_dirt()
        elif self.config == 'tree_grass':
            self.generate_tree_grass()
        elif self.config == 'crop_row':
            self.generate_crop_row()
        else:
            raise ValueError("Unknown farm configuration")

    def generate_plain(self): 
        """generates plain dirt farm"""
        self.grid = [[FarmTile(x, y, 0) for y in range(self.height)] for x in range(self.width)]

    def generate_river(self):
        """"generates farm with river and dirt along one side of the river. rest of farm is grass"""
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        river_orientation = random.randrange(2)
        if river_orientation == 0:
            river_range = self.height
        else:
            river_range = self.width
        
        river_start = random.randrange(3, river_range - 3)
        river_end = random.randrange(3, river_range - 3)

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

    def generate_tree_river(self):
        """"generates a farm with river, dirt along one side, and a tree. rest of farm is grass"""
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.generate_river()
        while True:
            tree_x = random.randrange(1, self.width - 1)
            tree_y = random.randrange(1, self.height - 1)
            if self.grid[tree_x][tree_y].tile_type == 1:
                break
        self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4) # tree

    def generate_tree_dirt(self):
        """Generates a dirt farm with three randomly placed trees."""
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        # Initialize the grid with plain dirt
        self.grid = [[FarmTile(x, y, 0) for y in range(self.height)] for x in range(self.width)]

        tree_count = 0
        while tree_count < 3:
            tree_x = random.randrange(1, self.width - 1)
            tree_y = random.randrange(1, self.height - 1)
            
            # CHECK IF tile is not already a tree
            if self.grid[tree_x][tree_y].tile_type == 0:  
                self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4)  
                tree_count += 1


    def generate_grass(self, grass_percentage=0.4):
        """Generate a grid with dirt and random grass patches.
        grass_percentage (float): A value between 0 and 1 representing the probability that a tile will be grass.
        """
        self.grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.grid = [[FarmTile(x, y, 0) for y in range(self.height)] for x in range(self.width)]  # Initialize grid with dirt

        for x in range(self.width):
            for y in range(self.height):
                if random.random() < grass_percentage:  # Randomly assign grass
                    self.grid[x][y] = FarmTile(x, y, 1)  # Grass tile
    
    def generate_crops(self):
        """Generates a plain dirt farm with randomly placed crops."""
        self.generate_plain()
        
        # Initialize grid with plain dirt
        #self.grid = [[FarmTile(x, y, 0) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y].tile_type == 3:  # If the tile is a crop
                    self.grid[x][y].tile_type = 0  # Reset it to dirt
        
        avail_positions = [(x, y) for x in range(self.width) for y in range(self.height) if ((x,y) != (0,0))]  # possible positions except farmer initial position
        
        crop_count = int(self.width * self.height * 0.2)  # 20% of the grid will have crops on it
        random.shuffle(avail_positions)  # Shuffle the available positions to randomize crop placement
        
        for _ in range(crop_count):
            if avail_positions:
                
                x, y = avail_positions.pop()  # pop from list and get random available position
                if self.grid[x][y].tile_type == 0 and self.grid[x][y].tile_type != 3:
                    self.grid[x][y] = CropTile(x, y, random.randrange(100) % 3) 
    def generate_crop_row(self):
        """Generates a farm with a single row of randomly placed crops. The row position and crop types are random."""
        self.grid = [[FarmTile(x, y, 0) for y in range(self.height)] for x in range(self.width)]  # Initialize grid with dirt

        # Randomly select a row position for the crops
        crop_row = random.randrange(1,self.height-1)

        # Randomly assign crop types to tiles in the selected row
        for x in range(self.width):
            crop_type = random.randrange(3)  # Randomly choose a crop type (0 = potato, 1 = carrot, 2 = pumpkin)
            self.grid[x][crop_row] = CropTile(x, crop_row, crop_type)  

        
    def restart(self):
        print("RESTART(farmgrid)")
        #self.farmer.x, self.farmer.y = 0, 0
        #for x in range(self.width):
         #   for y in range(self.height):
          #      if self.grid[x][y].tile_type == 3:
           #         self.grid[x][y].tile_type = 0
        self.grid = []
        self.generate_farm()  # Regenerate the farm grid
        if self.farmer is None: 
            self.add_farmer(0, 0)  # Add farmer back at the starting position
        else:
            self.farmer.x, self.farmer.y = 0, 0  # Reset farmer position
        
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
        return not self.out_of_bounds((x, y)) and (self.grid[x][y].tile_type < 2 or self.grid[x][y].tile_type==3)

    def add_farmer(self, x=0, y=0):
        if self.farmer is None:
            if self.grid[x][y].tile_type < 2 and not self.out_of_bounds((x, y)):
                self.farmer = Farmer(self, x, y)
                print("farmer added at ({}, {})".format(x, y))
        else: # farmer already exists
            self.farmer.x, self.farmer.y = x, y

    def remove_farmer(self):
        if self.farmer is not None:
            self.farmer = None
