import itertools


class FarmStats:
    """
    Stores and manages farm statistics, providing methods to track movements, crops planted, and harvested.
    This class facilitates the collection of various statistics related to the farm's state, enabling level checks and performance tracking throughout the game.
    """

    def __init__(self, farm):
        """
        Initializes the FarmStats object, setting up various statistics related to farm activities.

        Args:
            farm: object representing the farm, used to access its properties and state.
        """
        self.farm = farm

        self.left_moves = 0
        self.right_moves = 0
        self.up_moves = 0
        self.down_moves = 0

        self.potatoes_planted = 0
        self.carrots_planted = 0
        self.pumpkins_planted = 0

        self.potatoes_harvested = 0
        self.carrots_harvested = 0
        self.pumpkins_harvested = 0

    # Moving Statistics
    # Setters
    def add_moves(self, direction):
        """
        Increments the count of moves in a specified direction.
        Function updates the corresponding movement counter based on the direction provided, allowing for tracking of player movements within the farm.

        Args:
            direction: A string indicating the direction of movement, which can be "left", "right", "up", or "down".
        """
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
        """
        Args:
            direction: A string indicating the direction of movement, which can be "left", "right", "up", or "down".

        Returns:
            int: The number of moves in the specified direction.
        """
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
        """
        Returns:
            int: The total number of moves made in all directions.
        """
        return (
            self.left_moves + self.right_moves + self.up_moves + self.down_moves
        )

    # Planting Statistics
    # Setters
    def add_crops_planted(self, crop):
        """
        Args:
            crop: A string indicating the type of crop being planted, which can be "potato", "carrot", or "pumpkin".
        """
        match crop:
            case "potato":
                self.potatoes_planted += 1
            case "carrot":
                self.carrots_planted += 1
            case "pumpkin":
                self.pumpkins_planted += 1

    # Getters
    def get_potatoes_planted(self):
        """
        Returns:
            int: The number of potatoes planted.
        """
        return self.potatoes_planted

    def get_carrots_planted(self):
        """
        Returns:
            int: The number of carrots planted.
        """
        return self.carrots_planted

    def get_pumpkins_planted(self):
        """
        Returns:
            int: The number of pumpkins planted.
        """
        return self.pumpkins_planted

    def get_total_planted(self):
        """
        Returns:
            int: The total number of crops planted.
        """
        return (
            self.potatoes_planted + self.carrots_planted + self.pumpkins_planted
        )

    # Harvesting Statistics
    # Setters
    def add_crops_harvested(self, crop):
        """
        Args:
            crop: A string indicating the type of crop being harvested, which can be "potato", "carrot", or "pumpkin".
        """
        match crop:
            case "potato":
                self.potatoes_harvested += 1
            case "carrot":
                self.carrots_harvested += 1
            case "pumpkin":
                self.pumpkins_harvested += 1

    def increment_harvested(self, crop_type):
        """
        Args:
            crop_type: An integer representing the type of crop being harvested, where 0 is for potato, 1 is for carrot, and 2 is for pumpkin.
        """
        match crop_type:
            case 0:  # Potato
                self.potatoes_harvested += 1
            case 1:  # Carrot
                self.carrots_harvested += 1
            case 2:  # Pumpkin
                self.pumpkins_harvested += 1

    # Getters
    def get_potatoes_harvested(self):
        """
        Returns:
            int: The number of potatoes harvested.
        """
        return self.potatoes_harvested

    def get_carrots_harvested(self):
        """
        Returns:
            int: The number of carrots harvested.
        """
        return self.carrots_harvested

    def get_pumpkins_harvested(self):
        """
        Returns:
            int: The number of pumpkins harvested.
        """
        return self.pumpkins_harvested

    def get_total_harvested(self):
        """
        Returns:
            int: The total number of crops harvested.
        """
        return (
            self.potatoes_harvested
            + self.carrots_harvested
            + self.pumpkins_harvested
        )

    ## stats and check functions specifically for the level checks found in Level class ##
    def count_crops(self, crop_type):
        """
        Counts the total number of specific crop types present on the farm.
        This function iterates through the farm's grid, checking each tile to determine if it matches the specified crop type, and returns the total count of matching tiles.

        Args:
            crop_type: An integer representing the type of crop to count.

        Returns:
            int: The total number of tiles containing the specified crop type.

        """
        count = 0
        for x in range(self.farm.width):
            for y in range(self.farm.height):
                tile = self.farm.grid[x][y]
                if (
                    tile.tile_type == 3 and tile.crop_type == crop_type
                ):  # Check tiles with specific crop
                    count += 1
        return count

    def count_total_crops(self):
        """
        Counts the total number of crop tiles present on the farm.
        This function iterates through the farm's grid, checking each tile to determine if it is a crop tile, and returns the total count of all crop tiles.

        Returns:
            int: The total number of crop tiles on the farm.
        """
        count = 0
        for x, y in itertools.product(
            range(self.farm.width), range(self.farm.height)
        ):
            tile = self.farm.grid[x][y]
            if tile.tile_type == 3:
                count += 1
        return count

    # level specific checks
    def check_crops_in_row(self, count, crop):
        """
        Checks if there are a specified number of consecutive crops in either a row or a column.
        This function iterates through the farm's grid to determine if the given crop type appears consecutively for the specified count, returning a boolean indicating the presence of such a sequence.

        Args:
            count: An integer representing the number of consecutive crops to check for.
            crop: An integer representing the type of crop to check for (0 for potato, 1 for carrot, 2 for pumpkin).

        Returns:
            bool: True if the specified number of consecutive crops is found, otherwise False.
        """
        ver = False
        hor = False
        for y in range(self.farm.height):
            consecutive = 0
            for x in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if (
                    tile.tile_type == 3 and tile.crop_type == crop
                ):  # 0=potato, 1=carrot, 2=pumpkin
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
    def check_diagonal(self, x_start, y_start, x_move, y_move):
        x, y = x_start, y_start
        while 0<= x<10 and 0<= y<10:
            if (self.farm.grid[x][y].tile_type == 0):
                return False
            x += x_move
            y += y_move
        return True

    def check_crops_adjacent_to_river(self):
        """
        Checks if there are crops planted adjacent to the river.
        This function iterates through the farm's grid to determine if any crop tiles are located next to river tiles, returning a boolean indicating the presence of such crops.

        Returns:
            bool: True if there are crops adjacent to the river, otherwise False.
        """
        for x,y in itertools.product(
            range(self.farm.width), range(self.farm.height)
        ):
            tile = self.farm.grid[x][y]
            adjacent = self.farm.grid[x][y-1]
            if tile.tile_type == 2 and adjacent.tile_type == 3:
                return True

    def check_alternating_pattern(self, count):
        """
        Checks for an alternating pattern of carrots and pumpkins in a row or column.
        This function iterates through the farm's grid to determine if a specified number of consecutive tiles alternate between carrots and pumpkins, returning a boolean indicating the presence of such a pattern.

        Args:
            count: An integer representing the number of consecutive alternating crops to check for.

        Returns:
            bool: True if the specified alternating pattern is found, otherwise False.
        """
        for y in range(self.farm.height):
            consecutive = 0
            for x in range(self.farm.width):
                tile = self.farm.grid[x][y]
                if tile.tile_type == 3:
                    if (consecutive % 2 == 0 and tile.crop_type == 1) or (
                        consecutive % 2 == 1 and tile.crop_type == 2
                    ):  # Carrot then Pumpkin
                        consecutive += 1
                    else:
                        consecutive = 0
                if consecutive == count:
                    return True
        return False

    def check_no_dirt_tiles(self):
        """
        Checks if there are any dirt tiles present in the farm grid.
        This function iterates through all tiles in the grid and returns False if any dirt tiles are found; otherwise, it returns True, indicating that the grid is free of dirt tiles.

        Returns:
            bool: True if no dirt tiles are present, otherwise False.
        """
        # Iterate through all tiles in the grid
        for x, y in itertools.product(
            range(self.farm.width), range(self.farm.height)
        ):
            tile = self.farm.grid[x][y]
            if tile.tile_type == 0:
                return False  # Found a dirt tile, return False

        return True

    def longest_dirt_row(self):
        """
        Finds the longest consecutive row of dirt tiles in the farm grid.
        This function iterates through the specified rows of the farm's grid to count and track the longest sequence of consecutive dirt tiles, returning the length of that sequence.

        Returns:
            int: The length of the longest consecutive row of dirt tiles.
        """
        longest = 0  # keeep track of the longest sequence of dirt tiles

        for y in range(10):
            current_dirt_count = (
                0  # count consecutive dirt tiles in the current row
            )

            for x in range(10):
                tile = self.farm.grid[x][y]

                if tile.tile_type == 0:  # If dirt
                    current_dirt_count += 1
                    longest = max(longest, current_dirt_count)
                else:
                    current_dirt_count = (
                        0  # reset count when encountering grass or otherr tile
                    )

        return longest
