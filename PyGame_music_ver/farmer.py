# farmer.py

from farmtile import *


class Farmer:
    """
    Updates the Pygame display by rendering the current state of the farm and the grid.
    This function calls the rendering methods to draw the farm and grid, refreshes the display to show the updated visuals, and processes any pending events to ensure smooth interaction.
    """

    crop_desc = {0: "potato", 1: "carrot", 2: "pumpkin"}

    def __init__(self, farm, x=0, y=0):
        """
        Initializes a Farmer object with a specified farm and starting position.
        This constructor sets the farmer's symbol, position coordinates, and initializes the inventory with a predefined quantity of each crop type, allowing the farmer to interact with the farm environment.

        Args:
            farm: The farm object that the farmer will interact with.
            x: The initial x-coordinate of the farmer's position (default is 0).
            y: The initial y-coordinate of the farmer's position (default is 0).

        Returns:
            None
        """

        self.farm = farm
        self.symbol = "$"
        self.x = x
        self.y = y

        # Give the farmer 10 of each crop
        self.inventory = [0, 1, 2] * 10

    def __str__(self):
        """
        Returns a string representation of the Farmer object.
        This method provides a simple way to display the farmer's symbol, which is used to represent the farmer visually in the game.

        Args:
            None

        Returns:
            str: The symbol representing the farmer.
        """

        return self.symbol

    def get_pos(self):
        """
        Retrieves the current position of the farmer on the farm grid.
        This function returns the x and y coordinates of the farmer, allowing other components of the game to know the farmer's location.

        Args:
            None

        Returns:
            tuple: A tuple containing the x and y coordinates of the farmer.
        """

        return (self.x, self.y)

    def add_inventory(self, crop):
        """
        Adds a specified crop to the farmer's inventory.
        This function appends the given crop to the inventory list, allowing the farmer to collect and manage their crops throughout the game.

        Args:
            crop: The type of crop to be added to the inventory.

        Returns:
            None
        """

        self.inventory.append(crop)

    def remove_inventory(self, crop):
        """
        Removes a specified crop from the farmer's inventory.
        This function deletes the given crop from the inventory list, allowing the farmer to manage their collection of crops throughout the game.

        Args:
            crop: The type of crop to be removed from the inventory.

        Returns:
            None

        Raises:
            ValueError: If the specified crop is not found in the inventory.
        """

        self.inventory.remove(crop)

    def get_inventory(self):
        """
        Retrieves the current inventory of crops held by the farmer.
        This function returns a dictionary that maps each crop type to the quantity of that crop in the inventory, providing an overview of the farmer's collected resources.

        Args:
            None

        Returns:
            dict: A dictionary where the keys are crop names and the values are the counts of each crop in the inventory.
        """

        return {
            self.crop_desc[crop]: self.inventory.count(crop)
            for crop in set(self.inventory)
        }

    def move(self, direction):
        """
        Moves the farmer to an adjacent tile in the specified direction if the tile is walkable and within bounds.
        This function updates the farmer's position based on the provided direction and records the move in the farm's statistics.

        Args:
            direction: A string indicating the direction to move ('up', 'down', 'left', or 'right').

        Returns:
            None
        """

        dest = {
            "up": (self.x, self.y - 1),
            "down": (self.x, self.y + 1),
            "left": (self.x - 1, self.y),
            "right": (self.x + 1, self.y),
        }.get(direction, self.get_pos())

        if self.farm.walkable(dest) and not self.farm.out_of_bounds(dest):
            self.x, self.y = dest
            self.farm.stats.add_moves(direction)

    def plant(self, crop, direction):
        """
        Plants a specified crop on an adjacent dirt tile next to the farmer in the given direction.
        This function checks if the destination tile is a dirt tile and if the farmer has the crop in their inventory; if both conditions are met, it removes the crop from the inventory and updates the farm grid accordingly.

        Args:
            crop: The type of crop to be planted (e.g., 'potato', 'carrot', 'pumpkin').
            direction: A string indicating the direction to plant the crop ('up', 'down', 'left', or 'right').

        Returns:
            None

        Raises:
            ValueError: If the specified crop is not found in the inventory or if the destination tile is not a dirt tile.
        """

        crop = {v: k for k, v in self.crop_desc.items()}.get(
            crop
        )  # invert dictionary
        dest = {
            "up": (self.x, self.y - 1),
            "down": (self.x, self.y + 1),
            "left": (self.x - 1, self.y),
            "right": (self.x + 1, self.y),
        }.get(direction, self.get_pos())

        if (
            self.farm.grid[dest[0]][dest[1]].tile_type == 0
            and crop in self.inventory
        ):
            self.inventory.remove(crop)
            self.farm.grid[dest[0]][dest[1]] = CropTile(dest[0], dest[1], crop)
            self.farm.stats.add_crops_planted(self.crop_desc[crop])

    def harvest(self, direction):
        """
        Harvests a crop from an adjacent crop tile next to the farmer in the specified direction.
        This function checks if the destination tile contains a crop, adds the harvested crop to the farmer's inventory, resets the tile to dirt, and updates the farm's statistics accordingly.

        Args:
            direction: A string indicating the direction to harvest the crop ('up', 'down', 'left', or 'right').

        Returns:
            None

        Raises:
            ValueError: If the destination tile does not contain a crop or is out of bounds.
        """

        dest = {
            "up": (self.x, self.y - 1),
            "down": (self.x, self.y + 1),
            "left": (self.x - 1, self.y),
            "right": (self.x + 1, self.y),
        }.get(direction, self.get_pos())

        if self.farm.grid[dest[0]][dest[1]].tile_type == 3:
            crop = self.farm.grid[dest[0]][dest[1]].crop_type
            self.inventory.append(crop)
            self.farm.grid[dest[0]][dest[1]] = FarmTile(
                dest[0], dest[1], 0
            )  # Reset to dirt
            self.farm.stats.add_crops_harvested(self.crop_desc[crop])
            # Update harvested crops count
            self.farm.stats.increment_harvested(crop)
            print("HARVEST POTATO:  ", self.farm.stats.get_potatoes_harvested())
            print("HARVEST CARROT:  ", self.farm.stats.get_carrots_harvested())
            print("HARVEST PUMPKIN: ", self.farm.stats.get_pumpkins_harvested())
            print("HARVEST TOTAL:   ", self.farm.stats.get_total_harvested())
