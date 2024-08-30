# to be embedded in tkinter

import pygame
import time
from farm import FarmGrid

#color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

DIRT = (139,69,19)
GRASS = (148, 180, 5)
WATER = (30,144,255)
CROP = (255,69,0)

POTATO = (183, 146, 104)
CARROT = (255, 117, 24)
PUMPKIN = (237, 145, 33)

SCALE_FACTOR = 40
FARM_WIDTH = 10
FARM_HEIGHT = 10
SCREEN_WIDTH = FARM_WIDTH * SCALE_FACTOR
SCREEN_HEIGHT = FARM_HEIGHT * SCALE_FACTOR

# Initialize farm with farmer  
farm = FarmGrid(FARM_WIDTH, FARM_HEIGHT)
farm.add_farmer()

# Initialize pygame
pygame.init()
pygame.display.set_caption("TopFarmer")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def render_grid(width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, GRAY, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, GRAY, (0, y), (width, y))

def render_farm():
    for y in range(FARM_HEIGHT):
        for x in range(FARM_WIDTH):
            tile = farm.grid[x][y]
            color = WHITE
            if tile.tile_type == 0:
                color = DIRT
            elif tile.tile_type == 1:
                color = GRASS
            elif tile.tile_type == 2:
                color = WATER
            elif tile.tile_type == 3:
                crop_colors = [POTATO, CARROT, PUMPKIN]
                color = crop_colors[tile.crop_type]
            
            if farm.farmer.get_pos() == (x, y):
                color = RED
            pygame.draw.rect(surface, color, pygame.Rect(x*SCALE_FACTOR, y*SCALE_FACTOR, SCALE_FACTOR, SCALE_FACTOR))

def execute_python_code(code):
    code_lines = code.split("\n")
    print(code_lines)
    final_code = ""
    for line in code_lines:
        final_code += line + '\n'
        if line[-1] != ':':
            if line[0] == "\t":
                final_code += "\t"
            final_code += "update()\n"
            if line[0] == "\t":
                final_code += "\t"
            final_code += "time.sleep(1)\n"
    print(final_code)
    try:
        exec(final_code, {'farm': farm, 'print': print}, globals())
    except Exception as e:
        print(f"Error: {e}")

def update():
    render_farm()
    render_grid(SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR)
    pygame.display.flip()
