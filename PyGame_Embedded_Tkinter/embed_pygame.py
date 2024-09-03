# to be embedded in tkinter

import pygame
import time
from farmgrid import FarmGrid

class EmbedPygame:

    # general colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)

    # tile colors
    DIRT = (139,69,19)
    GRASS = (148, 180, 5)
    WATER = (30,144,255)
    CROP = (255,69,0)
    TREE = (18, 55, 11)

    # crop colors
    POTATO = (183, 146, 104)
    CARROT = (255, 117, 24)
    PUMPKIN = (237, 145, 33)

    # constants
    SCALE_FACTOR = 40
    FARM_WIDTH = 10
    FARM_HEIGHT = 10
    SCREEN_WIDTH = FARM_WIDTH * SCALE_FACTOR
    SCREEN_HEIGHT = FARM_HEIGHT * SCALE_FACTOR

    def __init__(self):
        # Initialize farm with farmer  
        self.farm = FarmGrid(self.FARM_WIDTH, self.FARM_HEIGHT)

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("TopFarmer")
        self.surface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Should the code execute step by step
        self.slow_mode = True

    def exit(self):
        pygame.QUIT


    def render_grid(self, width, height, cell_size):
        for x in range(0, width, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (x, 0), (x, height))
        for y in range(0, height, cell_size):
            pygame.draw.line(self.surface, self.GRAY, (0, y), (width, y))

    def render_farm(self):
        for y in range(self.FARM_HEIGHT):
            for x in range(self.FARM_WIDTH):
                tile = self.farm.grid[x][y]
                color = self.WHITE
                if tile.tile_type == 0:
                    color = self.DIRT
                elif tile.tile_type == 1:
                    color = self.GRASS
                elif tile.tile_type == 2:
                    color = self.WATER
                elif tile.tile_type == 3:
                    crop_colors = [self.POTATO, self.CARROT, self.PUMPKIN]
                    color = crop_colors[tile.crop_type]
                elif tile.tile_type == 4:
                    color = self.TREE
                
                if self.farm.farmer.get_pos() == (x, y):
                    color = self.RED
                pygame.draw.rect(self.surface, color, pygame.Rect(x*self.SCALE_FACTOR, y*self.SCALE_FACTOR, self.SCALE_FACTOR, self.SCALE_FACTOR))

    def execute_python_code(self, code):
        code = code.replace('farmer.', 'farm.farmer.')
        code_lines = code.split("\n")
        final_code = ""
        if self.slow_mode:
            for line in code_lines:
                final_code += line + '\n'
                if line[-1] != ':' and "else" not in line:
                    if line[0] == "\t":
                        final_code += "\t"
                    if line[1] == "\t":
                        final_code += "\t"
                    final_code += "update()\n"
                    if line[0] == "\t":
                        final_code += "\t"
                    if line[1] == "\t":
                        final_code += "\t"
                    final_code += "time.sleep(1)\n"
        else:
            final_code = code
        print(final_code)
        try:
            exec(final_code, { 'time': time, 'farm': self.farm, 'update': self.update})
        except Exception as e:
            print(f"Error: {e}")

    def update(self):
        self.render_farm()
        self.render_grid(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCALE_FACTOR)
        pygame.display.flip()
