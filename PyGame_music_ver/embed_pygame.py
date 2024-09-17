# embed_pygame.py
from tkinter import *
import pygame
import time
from farmgrid import FarmGrid
from tilegraphics import TileGraphics
class EmbedPygame:

    # general colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    BROWN = (140,69,20)

    # tile colors
    DIRT = (182, 137, 98)
    GRASS = (192, 212, 112)
    WATER = (155, 212, 195)
    CROP = (255,69,0)
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

    def __init__(self, config = "plain"):
        # Initialize farm with farmer  
        self.farm = FarmGrid(self.FARM_WIDTH, self.FARM_HEIGHT, config=config)

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("TopFarmer")
        self.surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Should the code execute step by step
        self.slow_mode = True
        
        # Initialize TileGraphics to handle loading images
        self.graphics = TileGraphics(self.SCALE_FACTOR)
        self.clock = pygame.time.Clock()

    def exit(self):
        pygame.QUIT


    def render_grid(self, width, height, cell_size):
        for x in range(0, width, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (0, y), (width, y))

    def render_farm(self):
        dt = self.clock.tick(60) # delta time for animation
        for y in range(self.FARM_HEIGHT):
            for x in range(self.FARM_WIDTH):
                tile = self.farm.grid[x][y]
                color = None
                if tile.tile_type == 0: # dirt tile
                    color = self.DIRT
                elif tile.tile_type == 1:  # grass tile
                    color = self.GRASS
                elif tile.tile_type == 2:  # water tile
                    color = self.WATER
                elif tile.tile_type == 3:  # crop tile
                    self.graphics.render_crop(self.surface, tile.crop_type, x, y)    
                elif tile.tile_type == 4:  # tree tile
                    self.graphics.render_tree(self.surface, x, y)
                
                 # Draw the tile with color if not crop,tree or farmer
                if color:
                    pygame.draw.rect(self.surface, color, pygame.Rect(
                    x * self.SCALE_FACTOR, y * self.SCALE_FACTOR, self.SCALE_FACTOR, self.SCALE_FACTOR))

                if self.farm.farmer is not None:
                    farmer_x, farmer_y = self.farm.farmer.get_pos()   
                    self.graphics.render_farmer(self.surface, farmer_x, farmer_y)
             
                #  re-render grid lines
                self.render_grid(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCALE_FACTOR)

    def execute_python_code(self, code):
        """injects user input code into program and executes it either line by line(slow mode) or all at once(slow mode off)"""
        code = code.replace('farmer.', 'farm.farmer.')
        code_lines = code.split("\n")
        final_code = ""
        indentation_stack = []

        if self.slow_mode: # slow mode on, execute line by line
            #loop through lines of userinput code
            for line in code_lines:
                stripped_line = line.strip()
                # Track indentation level by counting leading tabs
                indentation_level = len(line) - len(stripped_line) # remove trailing/leading whitespace
                if stripped_line.endswith(":") or stripped_line.startswith("else"):
                    # If the line ends with a colon or is an else statement, add it directly
                    final_code += line + '\n'
                    # Push indentation level to stack
                    indentation_stack.append(indentation_level)
                else:
                    # Add the line to final_code
                    final_code += line + '\n'
                    # Add update() and time.sleep() to final code with the same indentation level
                    final_code += '\t' * indentation_level + 'update()\n'
                    final_code += '\t' * indentation_level + 'time.sleep(0.4)\n'
                    # Pop from stack if the next line has less indentation
                    if indentation_stack and indentation_level < indentation_stack[-1]:
                        indentation_stack.pop() 
        else:
            final_code = code + '\ntime.sleep(1)\nupdate()\n'  # slow mode off, execute all at once
            
        # print full code to terminal
        print(final_code)
    
        # Execute final user python code
        try:
            exec(final_code, {'time': time, 'farm': self.farm, 'update': self.update, 'pygame': pygame})
        except Exception as e:
            print(f"Error: {e}")
 

    def update(self):
        self.render_farm()
        self.render_grid(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCALE_FACTOR)
        pygame.display.flip()
        pygame.event.pump()  # internally process pygame event handlers
