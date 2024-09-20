import itertools
import random
from farmer import Farmer
from farmtile import FarmTile, CropTile
from stats import FarmStats


class FarmGrid:
    """
    The FarmGrid class represents the grid layout of the farm, managing the placement of tiles, crops, and the farmer.
    This class provides methods for generating various farm configurations, handling the farmer's position, and checking the walkability of tiles, allowing for dynamic interactions within the farm environment.
    """

    def __init__(self, width=10, height=10, config="plain"):
        """
        Initializes a FarmGrid object with specified dimensions and configuration.
        This constructor sets up the farm grid, initializes the farmer, and generates the farm layout based on the provided configuration, allowing for a structured environment for gameplay.

        Args:
            width: The width of the farm grid (default is 10).
            height: The height of the farm grid (default is 10).
            config: A string that specifies the configuration of the farm (default is "plain").
        """

        self.width = width
        self.height = height
        self.farmer = None
        self.grid = []
        self.stats = FarmStats(self)
        self.config = config
        self.generate_farm()
        self.add_farmer(0, 0)

    def generate_farm(self):
        """
        Generates the farm layout based on the specified configuration type.
        This function checks the configuration and calls the appropriate method to create the farm grid, ensuring that the farm is set up according to the desired design.

        Raises:
            ValueError: If the specified configuration type is unknown.
        """

        config_methods = {
            "plain": self.generate_plain,
            "river": self.generate_river,
            "river_horizontal": self.generate_river_horizontal,
            "tree_river": self.generate_tree_river,
            "grass": self.generate_grass,
            "crops": self.generate_crops,
            "tree_dirt": self.generate_tree_dirt,
            # "tree_grass": self.generate_tree_grass,
            "crop_row": self.generate_crop_row,
        }

        try:
            config_methods[self.config]()
        except KeyError as e:
            raise ValueError("Unknown farm configuration") from e

    def generate_plain(self):
        """
        Generates a uniform farm grid consisting entirely of dirt tiles.
        This function initializes the grid by creating a specified number of FarmTile objects, each representing a dirt tile, based on the defined width and height of the farm.
        """
        self.grid = [
            [FarmTile(x, y, 0) for y in range(self.height)]
            for x in range(self.width)
        ]

    def generate_river(self):
        """
        Generates a farm layout that includes a river and adjacent dirt tiles, with the remainder of the farm being grass.
        This function randomly determines the orientation of the river and populates the farm grid accordingly, ensuring that the river is represented by water tiles and the area next to it is dirt, while the rest of the farm consists of grass tiles.
        """
        self.grid = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]
        river_orientation = random.randrange(2)
        river_range = self.height if river_orientation == 0 else self.width

        river_start = random.randrange(3, river_range - 3)
        river_end = random.randrange(3, river_range - 3)

        def is_river_tile(x, y):
            if river_orientation == 0:
                return y == int(
                    x * (river_start - river_end) / self.width + river_start
                )
            else:
                return x == int(
                    y * (river_start - river_end) / self.height + river_start
                )

        for y in range(self.height):
            for x in range(self.width):
                if is_river_tile(x, y):
                    self.grid[x][y] = FarmTile(x, y, 2)  # water
                    if river_orientation == 0:
                        self.grid[x][y - 1] = FarmTile(x, y, 0)  # dirt
                    else:
                        self.grid[x][y] = FarmTile(x, y, 1)  # grass
                else:
                    self.grid[x][y] = FarmTile(x, y, 1)  # grass

    def generate_river_horizontal(self):
        """
        Generates a farm layout featuring a horizontal river, with dirt tiles above the river and grass tiles below.
        This function initializes the farm grid, randomly selects a row for the river, and populates the grid with water, dirt, and grass tiles based on their respective positions relative to the river.
        """
        self.grid = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]

        river_y = random.randrange(
            2, self.height - 1
        )  # Pick a single row for the river

        for x in range(self.width):
            for y in range(self.height):
                if y == river_y:
                    self.grid[x][y] = FarmTile(
                        x, y, 2
                    )  # water (single row for the river)
                elif y < river_y:
                    self.grid[x][y] = FarmTile(
                        x, y, 0
                    )  # dirt (entire side above the river)
                else:
                    self.grid[x][y] = FarmTile(
                        x, y, 1
                    )  # grass (below the river)

        num_trees = random.randint(4, 10)  # random number of trees
        for _ in range(num_trees):
            tree_x = random.randint(0, self.width - 1)
            tree_y = random.randint(
                river_y + 1, self.height - 1
            )  # place trees below the river
            self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4)

    def generate_tree_river(self):
        """
        Generates a farm layout that includes a river, dirt tiles along one side, and a randomly placed tree, with the remainder of the farm being grass.
        This function initializes the farm grid, creates a river, and places a tree on a grass tile, ensuring that the tree is not placed on an existing tile.
        """
        self.grid = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]
        self.generate_river()
        while True:
            tree_x = random.randrange(1, self.width - 1)
            tree_y = random.randrange(1, self.height - 1)
            if self.grid[tree_x][tree_y].tile_type == 1:
                break
        self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4)  # tree

    def generate_tree_dirt(self):
        """
        Generates a farm layout consisting entirely of dirt tiles with three randomly placed trees.
        This function initializes the farm grid with dirt tiles and places three trees at random positions within the grid, ensuring a varied layout.
        """
        self.grid = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]
        # Initialize the grid with plain dirt
        self.grid = [
            [FarmTile(x, y, 0) for y in range(self.height)]
            for x in range(self.width)
        ]

        tree_count = 0
        while tree_count < 3:
            tree_x = random.randrange(1, self.width - 1)
            tree_y = random.randrange(1, self.height - 1)

            # CHECK IF tile is not already a tree
            if self.grid[tree_x][tree_y].tile_type == 0:
                self.grid[tree_x][tree_y] = FarmTile(tree_x, tree_y, 4)
                tree_count += 1

    def generate_grass(self, grass_percentage=0.4):
        """
        Generates a farm grid consisting of dirt tiles with randomly placed grass patches based on a specified probability.
        This function initializes the grid with dirt tiles and then populates it with grass tiles according to the given grass percentage, allowing for a varied landscape.

        Args:
            grass_percentage: A float value between 0 and 1 representing the probability that a tile will be grass (default is 0.4).
        """
        self.grid = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]
        self.grid = [
            [FarmTile(x, y, 0) for y in range(self.height)]
            for x in range(self.width)
        ]  # Initialize grid with dirt
        for x in range(self.width):
            for y in range(1):
                self.grid[x][y] = FarmTile(x, y, 1)  # Grass tile
        for x in range(self.width):
            for y in range(self.height):
                if random.random() < grass_percentage:  # Randomly assign grass
                    self.grid[x][y] = FarmTile(x, y, 1)  # Grass tile

    def generate_crops(self):
        """
        Generates a farm layout consisting of a plain dirt grid with randomly placed crops, while ensuring the first row is grass.
        This function initializes the farm by resetting any existing crops, populating the first row with grass, and randomly placing crops in available dirt tiles, accounting for a specified percentage of the grid.
        """
        self.generate_plain()

        # Reset any existing crops to dirt
        for x, y in itertools.product(range(self.width), range(self.height)):
            if self.grid[x][y].tile_type == 3:  # If the tile is a crop
                self.grid[x][y].tile_type = 0  # Reset it to dirt

        # Make the first row grass (assuming tile_type 1 represents grass)
        for x in range(self.width):
            self.grid[x][
                0
            ].tile_type = 1  # Set tile_type to grass for the first row

        # Generate a list of available positions excluding the first row and farmer's initial position
        avail_positions = [
            (x, y)
            for x in range(self.width)
            for y in range(1, self.height)
            if (x, y) != (0, 0)
        ]

        crop_count = int(
            self.width * self.height * 0.2
        )  # 20% of the grid will have crops
        random.shuffle(
            avail_positions
        )  # Shuffle the available positions to randomize crop placement

        for _ in range(crop_count):
            if avail_positions:
                x, y = avail_positions.pop()  # Get a random available position
                if self.grid[x][y].tile_type == 0:  # Ensure the tile is dirt
                    self.grid[x][y] = CropTile(
                        x, y, random.randrange(100) % 3
                    )  # Randomly select a crop (0-2)

    def generate_crop_row(self):
        """
        Generates a farm layout with a single row of randomly placed crops.
        This function initializes the farm grid with dirt tiles, randomly selects a row for the crops, and assigns random crop types to the tiles in that row, creating a varied crop layout.
        """
        self.grid = [
            [FarmTile(x, y, 0) for y in range(self.height)]
            for x in range(self.width)
        ]  # Initialize grid with dirt

        # Randomly select a row position for the crops
        crop_row = random.randrange(1, self.height - 1)

        # Randomly assign crop types to tiles in the selected row
        for x in range(self.width):
            crop_type = random.randrange(
                3
            )  # Randomly choose a crop type (0 = potato, 1 = carrot, 2 = pumpkin)
            self.grid[x][crop_row] = CropTile(x, crop_row, crop_type)

    def restart(self):
        """
        Restarts the farm grid by regenerating it and resetting the farmer's position.
        This function clears the existing grid, creates a new farm layout, and repositions the farmer to the starting location, ensuring a fresh state for gameplay.
        """
        print("RESTART(farmgrid)")
        self.grid = []
        self.generate_farm()  # Regenerate the farm grid
        if self.farmer is None:
            self.add_farmer(0, 0)  # Add farmer back at the starting position
        else:
            self.farmer.x, self.farmer.y = 0, 0  # Reset farmer position

    def __str__(self):
        """
        Returns a string representation of the farm's current state, including dimensions, farmer position, and inventory.
        This method constructs a visual layout of the farm grid, displaying the types of tiles and indicating the farmer's location with a specific symbol.

        Returns:
            str: A formatted string representing the farm's attributes and layout.
        """
        farmer_x, farmer_y = self.farmer.get_pos()
        string = "width={}, height={}\n".format(self.width, self.height)
        string += "farmer_position={} ({})\n".format(
            (farmer_x, farmer_y), self.grid[farmer_x][farmer_y]
        )
        string += "farmer_inventory={}\n".format(self.farmer.get_inventory())
        for y in range(self.height):
            for x in range(self.width):
                if (farmer_x, farmer_y) == (x, y):
                    symbol = self.farmer.symbol
                else:
                    symbol = str(self.grid[x][y].tile_type)

                string += symbol + " "
            string += "\n"
        return string

    def print(self):
        """
        Prints the string representation of the farm grid.
        This method calls the built-in print function on the farm grid object, allowing for a quick display of its current state.
        """
        print(self)

    def out_of_bounds(self, pos):
        """
        Checks whether a given position is outside the boundaries of the farm grid.
        This function evaluates the x and y coordinates of the provided position and returns a boolean indicating if the position is out of the defined grid dimensions.

        Args:
            pos: A tuple containing the x and y coordinates to check.

        Returns:
            bool: True if the position is out of bounds, otherwise False.
        """
        x, y = pos
        return not (0 <= x < self.width and 0 <= y < self.height)

    def walkable(self, pos):
        """
        Determines whether a given position on the farm grid is walkable.
        This function checks if the position is within the grid boundaries and verifies that the tile type at that position is either grass, dirt, or a crop, indicating that it can be traversed.

        Args:
            pos: A tuple containing the x and y coordinates to check.

        Returns:
            bool: True if the position is walkable, otherwise False.
        """
        x, y = pos
        return not self.out_of_bounds((x, y)) and (
            self.grid[x][y].tile_type < 2 or self.grid[x][y].tile_type == 3
        )

    def add_farmer(self, x=0, y=0):
        """
        Adds a farmer to the farm grid at the specified coordinates if no farmer currently exists.
        If a farmer already exists, this function updates the farmer's position to the new coordinates, ensuring that the new position is valid and not out of bounds.

        Args:
            x: The x-coordinate where the farmer should be placed (default is 0).
            y: The y-coordinate where the farmer should be placed (default is 0).
        """
        if self.farmer is None:
            if self.grid[x][y].tile_type < 2 and not self.out_of_bounds((x, y)):
                self.farmer = Farmer(self, x, y)
                print(f"farmer added at ({x}, {y})")
        else:  # farmer already exists
            self.farmer.x, self.farmer.y = x, y

    def remove_farmer(self):
        """
        Removes the farmer from the farm grid.
        This function sets the farmer attribute to None, effectively removing the farmer from the game if one exists.
        """
        self.farmer = None
