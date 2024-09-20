# embed_pygame.py
import ast
from tkinter import *
import pygame
import time
from farmgrid import FarmGrid
from tilegraphics import TileGraphics


class EmbedPygame:
    """
    EmbedPygame is responsible for initializing and managing the Pygame environment
    for the farm game. This class handles the rendering of the farm grid, the execution
    of user-provided Python code, and the management of game graphics, allowing for an
    interactive gameplay experience.
    """

    # general colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    BROWN = (140, 69, 20)

    # tile colors
    DIRT = (182, 137, 98)
    GRASS = (192, 212, 112)
    WATER = (155, 212, 195)
    CROP = (255, 69, 0)
    TREE = (18, 55, 11)

    # crop colors
    POTATO = (183, 146, 104)
    CARROT = (255, 117, 24)
    PUMPKIN = (237, 145, 33)

    # constants
    SCALE_FACTOR = 41
    FARM_WIDTH = 10
    FARM_HEIGHT = 10
    SCREEN_WIDTH = FARM_WIDTH * SCALE_FACTOR
    SCREEN_HEIGHT = FARM_HEIGHT * SCALE_FACTOR

    MAX_ITERATIONS = 350

    def __init__(self, config="plain"):
        """
        Initializes the EmbedPygame class, setting up the farm grid and the Pygame environment for the game.
        This constructor creates a farm instance, initializes Pygame, sets the display properties,
        and prepares the graphics and clock for rendering, allowing for an interactive gameplay experience.

        Args:
            config: A string that specifies the configuration of the farm (default is "plain").
        """

        # Initialize farm with farmer
        self.farm = FarmGrid(self.FARM_WIDTH, self.FARM_HEIGHT, config=config)

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("TopFarmer")
        self.surface = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )

        # Should the code execute step by step
        self.slow_mode = True

        # Initialize TileGraphics to handle loading images
        self.graphics = TileGraphics(self.SCALE_FACTOR)
        self.clock = pygame.time.Clock()

    def exit(self):
        """
        Exits the Pygame environment and closes the application.
        This function ensures that all Pygame resources are properly released, allowing for a clean shutdown of the game.
        """

        pygame.quit()

    def render_grid(self, width, height, cell_size):
        """
        Draws a grid on the Pygame surface using specified dimensions and cell size.
        This function creates vertical and horizontal lines to visually separate the grid cells, aiding in the representation of the farm layout.

        Args:
            width: The total width of the grid.
            height: The total height of the grid.
            cell_size: The size of each individual cell in the grid.
        """

        for x in range(0, width, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (0, y), (width, y))

    def render_farm(self):
        """
        Renders the farm grid on the Pygame surface, displaying various tile types and the farmer.
        This function iterates through the farm's grid, drawing each tile according to its type, and updates the display with the current state of the farm, including crops and the farmer's position.
        """

        dt = self.clock.tick(60)  # delta time for animation
        for y in range(self.FARM_HEIGHT):
            for x in range(self.FARM_WIDTH):
                tile = self.farm.grid[x][y]
                color = None
                if tile.tile_type == 0:  # dirt tile
                    color = self.DIRT
                elif tile.tile_type == 1:  # grass tile
                    color = self.GRASS
                elif tile.tile_type == 2:  # water tile
                    color = self.WATER
                elif tile.tile_type == 3:  # crop tile
                    self.graphics.render_crop(
                        self.surface, tile.crop_type, x, y
                    )
                elif tile.tile_type == 4:  # tree tile
                    self.graphics.render_tree(self.surface, x, y)

                # Draw the tile with color if not crop,tree or farmer
                if color:
                    pygame.draw.rect(
                        self.surface,
                        color,
                        pygame.Rect(
                            x * self.SCALE_FACTOR,
                            y * self.SCALE_FACTOR,
                            self.SCALE_FACTOR,
                            self.SCALE_FACTOR,
                        ),
                    )

                if self.farm.farmer is not None:
                    farmer_x, farmer_y = self.farm.farmer.get_pos()
                    self.graphics.render_farmer(
                        self.surface, farmer_x, farmer_y
                    )

                #  re-render grid lines
                self.render_grid(
                    self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCALE_FACTOR
                )

    def check_infinite_loop(self):
        """
        Checks if iteration count exceeds maximum allowed iterations and raises an exception if
        if iteration count exceeds MAX_ITERATIONS
        This function is used to prevent possible infinite loops.
        """
        self.iteration_count += 1
        if self.iteration_count > self.MAX_ITERATIONS:
            raise Exception(
                "Loop exceeded maximum iterations! Check your code for a possible infinite loop."
            )

    def direction_helper(self, code):
        """
        Analyses the provided code to check for direction arguments in farmer.move, farmer.plant or farmer.harvest calls.

        Args:
            code: String of Python code to analyse.

        Returns:
            list: A list of tuples containing the function name and line number where the direction argument is missing (or misspelled).
        """
        valid_directions = {
            '"up"',
            '"down"',
            '"left"',
            '"right"',
            "'up'",
            "'down'",
            "'left'",
            "'right'",
        }
        missing_directions = []
        lines = code.splitlines()

        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if (
                "farmer.move" in line
                or "farmer.plant" in line
                or "farmer.harvest" in line
            ):
                func_call = ""
                # case 1: move
                if "farmer.move" in line:
                    func_call = "move"
                # case 2: plant
                if "farmer.plant" in line:
                    func_call = "plant"
                # case 3: harvest
                if "farmer.harvest" in line:
                    func_call = "harvest"

                # Check the function call has a direction argument
                if "(" in line and ")" in line:
                    # Extract the part inside parentheses
                    start_index = line.index("(") + 1
                    end_index = line.index(")")
                    args = line[start_index:end_index].split(",")

                    # Check if the first argument is a direction (string) and is not empty
                    if not any(
                        arg.strip().startswith("'")
                        and arg.strip().endswith("'")
                        for arg in args
                    ) and (
                        not any(
                            arg.strip().startswith('"')
                            and arg.strip().endswith('"')
                            for arg in args
                        )
                    ):
                        function_name = line.split("(")[0].strip()
                        missing_directions.append((function_name, line_number))
                    elif func_call in {"move", "harvest"}:
                        # Check that there is only one arg
                        if len(args) == 1 and (
                            args[0].strip() not in valid_directions
                        ):
                            function_name = line.split("(")[0].strip()
                            missing_directions.append(
                                (function_name, line_number)
                            )
                    elif func_call == "plant":
                        if (
                            len(args) == 2
                            and args[1].strip() not in valid_directions
                        ):
                            function_name = line.split("(")[0].strip()
                            missing_directions.append(
                                (function_name, line_number)
                            )

        return missing_directions

    def execute_python_code(self, code):
        """
        Injects user-provided Python code into the program and executes it, either line by line in slow mode or all at once in normal mode.
        This function modifies the input code to ensure proper context, manages indentation for execution, and handles any errors that may arise during execution.

        Args:
            code: A string containing the Python code to be executed.

        Raises:
            Exception: If there is an error during the execution of the provided code.
        """

        # Initialize iteration count for loop checking
        self.iteration_count = 0

        for i, missing_direction in enumerate(self.direction_helper(code)):
            print(
                f"function {self.direction_helper(code)[i][0]} on line {self.direction_helper(code)[i][1]} has a missing or incorrect direction."
            )

        # Inject check for infinite loops
        code = code.replace("farmer.", "farm.farmer.")

        code_lines = code.split("\n")
        final_code = ""
        indentation_stack = []

        if self.slow_mode:  # slow mode on, execute line by line
            for line in code_lines:
                stripped_line = line.strip()
                indentation_level = len(line) - len(stripped_line)
                # Detect loops: `for` and `while` statements
                if stripped_line.startswith("for") or stripped_line.startswith(
                    "while"
                ):
                    # Inject loop check to prevent infinite loops
                    final_code += line + "\n"
                    final_code += (
                        "\t" * (indentation_level + 1)
                        + "check_infinite_loop()\n"
                    )
                    indentation_stack.append(indentation_level)
                elif stripped_line.endswith(":") or stripped_line.startswith(
                    "else"
                ):
                    # colon-ending statements eg: `if`, `else`, `def`, etc.
                    final_code += line + "\n"
                    indentation_stack.append(indentation_level)
                else:
                    # Normal code lines, add update and time.sleep for slow mode
                    final_code += line + "\n"
                    final_code += "\t" * indentation_level + "update()\n"
                    final_code += "\t" * indentation_level + "time.sleep(0.4)\n"
                    if (
                        indentation_stack
                        and indentation_level < indentation_stack[-1]
                    ):
                        indentation_stack.pop()
        else:
            # In normal mode, inject the infinite loop check in a similar way
            for line in code_lines:
                stripped_line = line.strip()
                indentation_level = len(line) - len(stripped_line)
                if stripped_line.startswith("for") or stripped_line.startswith(
                    "while"
                ):
                    # Inject loop check to prevent infinite loops
                    final_code += line + "\n"
                    final_code += (
                        "\t" * (indentation_level + 1)
                        + "check_infinite_loop()\n"
                    )
                else:
                    final_code += line + "\n"

            # Add a global check for loop iterations at the end of the code block
            final_code += "\ncheck_infinite_loop()\ntime.sleep(1)\nupdate()\n"

        # Inject infinite loop check function at the start of the code
        infinite_loop_checker = (
            f"def check_infinite_loop():\n"
            f"\tglobal iteration_count\n"
            f"\titeration_count += 1\n"
            f"\tif iteration_count > MAX_ITERATIONS:\n"
            f"\t\traise Exception('Loop exceeded maximum iterations! Check your code for a possible infinite loop')\n"
        )
        final_code = infinite_loop_checker + final_code

        # execute final user Python code
        try:
            exec(
                final_code,
                {
                    "time": time,
                    "farm": self.farm,
                    "update": self.update,
                    "pygame": pygame,
                    "check_infinite_loop": self.check_infinite_loop,
                    "iteration_count": self.iteration_count,
                    "MAX_ITERATIONS": self.MAX_ITERATIONS,
                },
            )
        except Exception as e:
            print(f"Error: {e}")

    def update(self):
        """
        Updates the Pygame display by rendering the current state of the farm and the grid.
        This function calls the rendering methods to draw the farm and grid, refreshes the display to show the updated visuals, and processes any pending events to ensure smooth interaction.
        """

        self.render_farm()
        self.render_grid(
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCALE_FACTOR
        )
        pygame.display.flip()
        pygame.event.pump()  # internally process pygame event handlers
