# saveandload.py


class SaveAndLoad:
    """Handles the saving and loading of game code to and from a specified file.
    This class provides methods to write code to a file and read code from a file, facilitating persistent data management for the game state.
    """

    def __init__(self):
        """Initializes the SaveAndLoad object, setting the default file path for saving and loading game code.
        This constructor defines the file name used for storing the game's state.
        """
        self.code_file = "code_save.txt"

    def save_code(self, code):
        """
        Saves the provided game code to a specified file.
        This function attempts to write the given code to the designated file.

        Args:
            code: A string representing the game code to be saved.

        Raises:
            IOError: If there is an error writing to the file.
        """
        try:
            with open(self.code_file, "w") as file:
                file.write(code)
        except IOError:
            print("Error: Could not write file")

    def load_code(self):
        """
        Loads the game code from a specified file.
        This function attempts to read the contents of the designated file and returns the code, allowing for the restoration of the game's state. If an error occurs during the file reading process, it handles the exception gracefully.

        Returns:
            str: The game code read from the file, or an empty string if an error occurs.

        Raises:
            IOError: If there is an error reading the file.
        """

        code = ""  # Initialize with a default value
        try:
            file = open(self.code_file, "r")
            code = file.read()
            file.close()
        except IOError:
            print("Error: Could not read file")
        return code
