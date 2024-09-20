# farmtile.py
class FarmTile:
    """
    Represents a tile in the farm grid, including its type and position.
    This class provides methods to retrieve the tile's position, check if it is a crop tile, and get the crop type if applicable, facilitating interactions within the farm environment.
    """

    tile_desc = {0: "dirt", 1: "grass", 2: "water", 3: "crop", 4: "tree"}

    def __init__(self, x, y, tile_type=0):
        """
        Initializes a FarmTile object with specified coordinates and tile type.
        This constructor sets the position of the tile on the farm grid and defines its type, which determines the tile's characteristics and behavior within the game.

        Args:
            x: The x-coordinate of the tile's position.
            y: The y-coordinate of the tile's position.
            tile_type: An integer representing the type of tile (default is 0 for dirt).
        """
        self.tile_type = tile_type
        self.x = x
        self.y = y

    def __str__(self):
        """
        Returns a string representation of the FarmTile object based on its tile type.
        This method retrieves the corresponding description from the tile descriptor dictionary, providing a human-readable format for the tile's type.

        Returns:
            str: A string representing the tile type description.
        """
        return str(self.tile_desc[self.tile_type])

    def get_pos(self):
        """
        Retrieves the current position of the tile in the farm grid.
        This function returns the x and y coordinates as a tuple, allowing other components of the program to know the tile's location.

        Returns:
            tuple: A tuple containing the x and y coordinates of the tile.
        """
        return (self.x, self.y)

    def is_crop(self):
        """
        Determines whether the tile is a crop tile.
        This function checks the tile type and returns True if it corresponds to a crop, indicated by the tile type value of 3.

        Returns:
            bool: True if the tile is a crop, otherwise False.
        """
        return self.tile_type == 3

    def get_crop_type(self):
        """
        Retrieves the type of crop associated with the tile if it is designated as a crop.
        This function checks whether the tile is a crop and returns the crop type if true; otherwise, it returns None.

        Returns:
            The type of crop if the tile is a crop, otherwise None.
        """
        return self.crop_type if self.is_crop() else None


class CropTile(FarmTile):
    """
    Represents a crop tile in the farm grid, inheriting from the FarmTile class.
    This class initializes a crop tile with a specified crop type and provides a method to retrieve the crop type, allowing for detailed management of crops within the farm environment.
    """

    def __init__(self, x, y, crop_type=0):
        """
        Initializes a CropTile object with specified coordinates and crop type.
        This constructor sets the position of the crop tile on the farm grid and defines its crop type, which determines the specific crop represented by the tile.

        Args:
            x: The x-coordinate of the crop tile's position.
            y: The y-coordinate of the crop tile's position.
            crop_type: An integer representing the type of crop (default is 0).
        """
        super().__init__(x, y, 3)
        self.crop_type = crop_type

    def get_crop_type(self):
        """
        Retrieves the type of crop associated with the CropTile.
        This function returns the crop type value, allowing other components of the program to identify the specific crop represented by the tile.

        Returns:
            The type of crop associated with the tile.
        """
        return self.crop_type
