# stats.py

class FarmStats:
    """class for storing farm statistics for StatisticsPage and functions that 
    return information about farm state used in level checking"""
    def __init__(self,farm):
        self.farm = farm

        self.left_moves = 0
        self.right_moves = 0
        self.up_moves = 0
        self.down_moves = 0

        self.potatoes_planted = 0
        self.carrots_planted = 0
        self.pumpkins_planted = 0

        self.potatoes_harvested = 0
        self.carrots_harvested= 0
        self.pumpkins_harvested = 0

    # Moving Statistics
    # Setters
    def add_moves(self, direction):
        match direction:
            case "left":
                self.left_moves += 1
            case "right":
                self.right_moves += 1
            case "up":
                self.up_moves += 1
            case "down":
                self.down_moves += 1
    # Getters
    def get_moves(self, direction):
        match direction:
            case "left":
                return self.left_moves
            case "right":
                return self.right_moves
            case "up":
                return self.up_moves
            case "down":
                return self.down_moves
    
    def get_total_moves(self):
        return self.left_moves + self.right_moves + self.up_moves + self.down_moves
    
    # Planting Statistics
    # Setters
    def add_crops_planted(self, crop):
        match crop:
            case "potato":
                self.potatoes_planted += 1
            case "carrot":
                self.carrots_planted += 1
            case "pumpkin":
                self.pumpkins_planted += 1
    # Getters
    def get_potatoes_planted(self):
        return self.potatoes_planted
    def get_carrots_planted(self):
        return self.carrots_planted
    def get_pumpkins_planted(self):
        return self.pumpkins_planted
    def get_total_planted(self):
        return self.potatoes_planted + self.carrots_planted + self.pumpkins_planted
    
    # Harvesting Statistics
    # Setters
    def add_crops_harvested(self, crop):
        match crop:
            case "potato":
                self.potatoes_harvested += 1
            case "carrot":
                self.carrots_harvested += 1
            case "pumpkin":
                self.pumpkins_harvested += 1

    def increment_harvested(self, crop_type):
        match crop_type:
            case 0:  # Potato
                self.potatoes_harvested += 1
            case 1:  # Carrot
                self.carrots_harvested += 1
            case 2:  # Pumpkin
                self.pumpkins_harvested += 1
    # Getters
    def get_potatoes_harvested(self):
        return self.potatoes_harvested
    def get_carrots_harvested(self):
        return self.carrots_harvested
    def get_pumpkins_harvested(self):
        return self.pumpkins_harvested
    def get_total_harvested(self):
        return self.potatoes_harvested + self.carrots_harvested + self.pumpkins_harvested
    
## stats and check functions specifically for the level checks found in Level class ##
    def count_crops(self, crop_type):
        """Count the total number of specific crop type on the farm."""
        count = 0
        for x in range(self.farm.width):
            for y in range(self.farm.height):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3 and tile.crop_type == crop_type:  # Check tiles with specific crop
                    count += 1
        return count
    
    def count_total_crops(self):
        """Count the total number of all types of crop tiles on the farm."""
        count = 0
        for x in range(self.farm.width):
            for y in range(self.farm.height):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3:  
                    count += 1
        return count
    
    # level specific checks
    def check_crops_in_row(self, count, crop):
        """ check if there are 'count' crop in a row or col"""
        ver = False
        hor = False
        for y in range(self.farm.height):
            consecutive = 0
            for x in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3 and tile.crop_type == crop:  # 0=potato, 1=carrot, 2=pumpkin
                    consecutive += 1
                    if consecutive == count:
                        hor = True
                else:
                    consecutive = 0
        
        for x in range(self.farm.height):
            consecutive = 0
            for y in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3 and tile.crop_type == crop:  
                    consecutive += 1
                    if consecutive == count:
                        ver = True
                else:
                    consecutive = 0

        return ver or hor
    def check_crops_adjacent_to_river(self):
        """check if there are crops planted adjacent to the river"""
        for x in range(self.farm.width):
            for y in range(self.farm.height):
                tile = self.farm.grid[x][y]
                adjacent = self.farm.grid[x][y-1]
                if tile.tile_type == 2: 
                    if adjacent.tile_type == 3:
                        return True
                    

    def check_alternating_pattern(self, count):
        """Check for alternating carrots and pumpkins in a row or column."""
        for y in range(self.farm.height):
            consecutive = 0
            for x in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3:  
                    if (consecutive % 2 == 0 and tile.crop_type == 1) or (consecutive % 2 == 1 and tile.crop_type == 2):  # Carrot then Pumpkin
                        consecutive += 1
                    else:
                        consecutive = 0
                if consecutive == count:
                    return True
        
        return False
    def check_no_dirt_tiles(self):
        """checks that there are no dirt tiles in the farm grid"""
        # Iterate through all tiles in the grid
        for x in range(self.farm.width):
            for y in range(self.farm.height):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 0: 
                    return False  # Found a dirt tile, return False

        return True
    
    def longest_dirt_row(self):
        """Finds the longest consecutive row of dirt tiles in the farm grid."""
        longest = 0  #keeep track of the longest sequence of dirt tiles

        for y in range(10):  
            current_dirt_count = 0  #count consecutive dirt tiles in the current row

            for x in range(10):  
                tile = self.farm.grid[x][y] 

                if tile.tile_type == 0:  # If dirt
                    current_dirt_count += 1
                    longest = max(longest, current_dirt_count)
                else:
                    current_dirt_count = 0  # reset count when encountering grass or otherr tile

        return longest



    