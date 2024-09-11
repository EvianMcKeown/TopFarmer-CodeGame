# stats.py

class FarmStats:
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
    
    def check_potatoes_in_row(self, count):
        #  check if there are 'count' potatoes in a row
        ver = False
        hor = False
        for y in range(self.farm.height):
            consecutive = 0
            for x in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3 and tile.crop_type == 0:  # 0 for potato
                    consecutive += 1
                    if consecutive == count:
                        hor = True
                else:
                    consecutive = 0
        
        for x in range(self.farm.height):
            consecutive = 0
            for y in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3 and tile.crop_type == 0:  # 0 for potato
                    consecutive += 1
                    if consecutive == count:
                        ver = True
                else:
                    consecutive = 0

        return ver or hor