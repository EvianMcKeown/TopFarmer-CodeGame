# levels.py
from farmgrid import FarmGrid
from farmer import Farmer
from farmtile import FarmTile, CropTile
import json


class Levels:
    """
    Levels manages the game's levels, including their tasks, unlock status, and progress tracking.
    This class initializes the levels with specific tasks and configurations, provides methods to save and load progress, and checks for level completion based on player actions.
    """

    def __init__(self):
        """
        Initializes the Levels class, setting up the levels dictionary with tasks, completion checks, and unlock statuses.
        This constructor establishes the current level and loads any previously saved progress, allowing the game to track player advancement through various challenges.
        """

        # initialises levels dictionary with data and sets current level to lvl 1
        self.levels = {
            1: {
                "task": "Plant 5 potatoes in a single row or column.\n\n  HINT: try using a for loop",  # just 5 consecvtive potatoes
                "check_completion": self.check_level_1_completion,
                "config": "plain",
                "requires_multiple_test_cases": False,  #  false if code is to be run on only one farm instance
                "unlocked": True,
            },
            2: {  # a pattern.. must be in row
                "task": "Plant 4 carrots and 4 pumpkins in an alternating pattern. eg: carrot, pumpkin, carrot, pumpkin, etc",
                "check_completion": self.check_level_2_completion,
                "config": "plain",  # dirt only
                "requires_multiple_test_cases": False,
                "unlocked": False,
            },
            3: {
                "task": "Plant 2 diagonal lines of crops across the farm where possible so that it forms an X shape. You may use any crops you like.\n\nHINT: Grass is not plantable on",
                "check_completion": self.check_level_3_completion,
                "config": "grass",
                "requires_multiple_test_cases": False,  # true if level requires multiple test cases to pass
                "unlocked": False,
            },
            4: {
                "task": "plant pumpkins along the river (all dirt tiles adjacent to river). Your code must now pass all 3 randomised farm cases.\n\n HINT: think. How can you check the type of tile?",
                "check_completion": self.check_level_4_completion,
                "config": "river_horizontal",
                "requires_multiple_test_cases": True,
                "unlocked": False,
            },
            5: {
                "task": "Replace every pumpkin with a carrot\n\n  HINT: How do you check the type of crop?",
                "check_completion": self.check_level_5_completion,
                "config": "crop_row",
                "requires_multiple_test_cases": True,
                "unlocked": False,
            },
            6: {
                "task": "harvest every crop on the farm.\n\n  HINT: consider trying to move in a zig-zag pattern to optimise the pathing of the farmer ",
                "check_completion": self.check_level_6_completion,
                "config": "crops",
                "requires_multiple_test_cases": False,
                "unlocked": False,
            },
            7: {
                "task": "find the longest consecutive row of dirt and fill it with carrots.",
                "check_completion": self.check_level_7_completion,
                "config": "grass",
                "requires_multiple_test_cases": False,
                "unlocked": False,
            },
            8: {
                "task": "find the longest consecutive row of dirt and fill it with carrots (no hardcoding; several random test cases apply).\n\n HINT: consider defining functions in your solution perhaps to find the longest dirt row's position and length \n\n NOTE: for this level, slow mode is automatically turned off in order to execute your code without waiting for too long ",
                "check_completion": self.check_level_8_completion,
                "config": "grass",
                "requires_multiple_test_cases": True,
                "unlocked": False,
            },
        }
        self.current_level = 1
        self.load_progress()

    def save_progress(self):
        """
        Saves the current game progress, including the current level and the
        unlock status of all levels, to a JSON file. This function creates a
        dictionary representing the progress and writes it to
        'level_progress.json', allowing the game to restore the player's state
        in future sessions.
        """

        # Save the current level and unlocked levels to a JSON file
        progress = {
            "current_level": self.current_level,
            "levels": {k: v["unlocked"] for k, v in self.levels.items()},
        }
        with open("level_progress.json", "w") as file:
            json.dump(progress, file)
            print("Progress saved")

    def load_progress(self):
        """
        Loads the saved game progress from a JSON file, restoring the current
        level and the unlock status of all levels.
        This function attempts to read from 'level_progress.json' and updates
        the game state accordingly; if the file does not exist, it initializes
        the game to default settings.

        Raises:
            FileNotFoundError: If the level progress file does not exist.
        """

        # Load saved progress from json file
        try:
            with open("level_progress.json", "r") as file:
                print("loading progress...")
                progress = json.load(file)
                self.current_level = progress.get("current_level", 1)
                unlocked_levels = progress.get("levels", {})
                for level_str, unlocked in unlocked_levels.items():
                    level = int(level_str)  # Convert level string to int
                    if level in self.levels:
                        self.levels[level]["unlocked"] = unlocked
        except FileNotFoundError:
            # if file does not exist, initialize to default
            print("no saved game found. creating new save")

    def get_current_task(self):
        """
        Retrieves the objective description for the current level in the game.
        This function accesses the levels dictionary to return the task associated
        with the active level, providing players with the information needed to
        complete their objectives.

        Returns:
            str: The task description for the current level.
        """

        # returns level objective description
        return self.levels[self.current_level]["task"]

    def get_current_config(self):
        """
        Retrieves the farm configuration for the current level in the game.
        This function accesses the levels dictionary to return the configuration associated with the active level, which determines the layout and conditions of the farm environment.

        Returns:
            str: The configuration type for the current level.
        """

        # returns farm config for level
        return self.levels[self.current_level]["config"]

    def get_test_cases(self):
        """
        Determines whether the current level requires multiple test cases to complete.
        This function checks the levels dictionary to return a boolean indicating if the active level has been configured to necessitate multiple test cases for successful completion.

        Returns:
            bool: True if the current level requires multiple test cases, otherwise False.
        """

        return self.levels[self.current_level]["requires_multiple_test_cases"]

    def is_level_unlocked(self, level_number):
        """
        Checks whether a specified level is unlocked for the player.
        This function retrieves the unlock status of the given level number from the levels dictionary, indicating if the level can be accessed or is currently locked.

        Args:
            level_number: The number of the level to check for unlock status.

        Returns:
            bool: True if the level is unlocked, otherwise False.
        """

        return self.levels.get(level_number, {}).get("unlocked", False)

    def unlock_next_level(self):
        """
        Unlocks the next level in the game, allowing the player to access it.
        This function checks if the next level exists in the levels dictionary and sets its unlock status to True, enabling the player to progress further in the game.

        Returns:
            None
        """

        next_level = self.current_level + 1
        if next_level in self.levels:
            self.levels[next_level]["unlocked"] = True

    def advance_to_next_level(self):
        """
        Advances the player to the next level and unlocks it for access.
        This function checks if the current level is not the last level, unlocks the next level, increments the current level, and saves the progress to ensure that the player's state is maintained.
        """

        if self.current_level != 8:
            self.unlock_next_level()
            self.current_level += 1
            self.save_progress()

    def check_current_level_completion(self, farm_stats):
        """
        Checks if the current level has been completed by invoking the level-specific completion function.
        This function retrieves the appropriate completion check for the active level and executes it using the provided farm statistics, returning the result of the check.

        Args:
            farm_stats: An object containing the current state of the farm, used to evaluate level completion.

        Returns:
            bool: True if the current level is completed, otherwise False.
        """

        check_function = self.levels[self.current_level]["check_completion"]
        return check_function(farm_stats)

    """
    Contains level-specific completion check functions that evaluate the state of the farm grid. 
    These functions utilize the provided farm statistics to determine if the objectives for each level have been met, allowing for the reuse of common checks across different levels.

    Args:
        farm_stats: An object containing the current state of the farm, used to evaluate level completion.

    Returns:
        bool: True if the level's completion criteria are satisfied, otherwise False.
    """

    def check_level_1_completion(self, farm_stats):
        # Check if 5 potatoes are planted in a row/col
        return farm_stats.check_crops_in_row(5, 0) and farm_stats.count_crops(0) ==5

    def check_level_2_completion(self, farm_stats):
        # check for 4 carrots and 4 pumpkins in an alternating pattern.
        return farm_stats.check_alternating_pattern(4)

    def check_level_3_completion(self, farm_stats):
        # check for 2 diagonal lines of crops across the farm
        return farm_stats.check_diagonal(0,0,1,1) and farm_stats.check_diagonal(0,9,-1,1)

    def check_level_4_completion(self, farm_stats):
        return (
            farm_stats.check_crops_in_row(10, 2)
            and farm_stats.check_crops_adjacent_to_river()
        )

    def check_level_5_completion(self, farm_stats):
        if (
            farm_stats.count_crops(2) == 0
            and farm_stats.count_total_crops() == 10
        ):
            return True

    def check_level_6_completion(self, farm_stats):
        return farm_stats.count_total_crops() == 0

    def check_level_7_completion(self, farm_stats):
        longest = farm_stats.longest_dirt_row()
        print("longest dirt row = ", longest)
        return farm_stats.check_crops_in_row(longest, 1)

    def check_level_8_completion(self, farm_stats):
        longest = farm_stats.longest_dirt_row()
        print("longest dirt row = ", longest)
        return farm_stats.check_crops_in_row(longest, 1)
