import sys
import time
import pygame
import farm
from colors import *

SCALE_FACTOR = 50 # feel free to change this to any reasonable value

FARM_WIDTH = 10 # number of farm grid array columns
FARM_HEIGHT = 10 # number of farm grid array rows

SIDE_WIDTH = SCALE_FACTOR * 8 # the side panel for user input

BUTTON_WIDTH = SCALE_FACTOR * 2
BUTTON_HEIGHT = SCALE_FACTOR * 1

SCREEN_WIDTH = FARM_WIDTH * SCALE_FACTOR + SIDE_WIDTH
SCREEN_HEIGHT = FARM_HEIGHT * SCALE_FACTOR

# initialise farm with farmer  
farm = farm.FarmGrid(FARM_WIDTH, FARM_HEIGHT)
farm.add_farmer()

# initialise pygame
pygame.init()
pygame.display.set_caption("TopFarmer")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

user_input = "" # the list of instructions to control the farmer

# draw grid lines on the screen
def draw_grid(surface, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(surface, GRAY, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(surface, GRAY, (0, y), (width, y))

# render farm
def render_farm():
    for y in range(FARM_HEIGHT):
        for x in range(FARM_WIDTH):
            match farm.grid[x][y].tile_type:
                case 0:
                    color = DIRT
                case 1:
                    color = GRASS
                case 2:
                    color = WATER
                case 3:
                    color = CROP
                case _:
                    color = BLACK
            if farm.farmer.get_pos() == (x, y):
                color = RED
            pygame.draw.rect(surface, color, pygame.Rect(x*SCALE_FACTOR + SIDE_WIDTH, y*SCALE_FACTOR, SCALE_FACTOR, SCALE_FACTOR))

def render_text_input(text):
    pygame.draw.rect(surface, BLACK, pygame.Rect(0, 0, SIDE_WIDTH, SCREEN_HEIGHT))
    text = text.split('\n')
    for line_num in range(len(text)):
        text_image = pygame.font.SysFont(None, 24).render(text[line_num], True, GREEN)
        pygame.draw.rect(surface, BLACK, pygame.Rect(0, line_num * 24, SIDE_WIDTH, 24 * line_num))
        surface.blit(text_image, (0, (line_num) * 24))

def render_button_run():
    text_image = pygame.font.SysFont(None, int(SCALE_FACTOR / 2)).render("RUN CODE", True, WHITE)
    pygame.draw.rect(surface, BLUE, pygame.Rect(0, SCREEN_HEIGHT - SCALE_FACTOR, BUTTON_WIDTH, BUTTON_HEIGHT))
    surface.blit(text_image, (SCREEN_WIDTH*0.005, (SCREEN_HEIGHT - SCALE_FACTOR)*1.04))

def render_button_reset():
    text_image = pygame.font.SysFont(None, int(SCALE_FACTOR / 2)).render("RESTART", True, WHITE)
    pygame.draw.rect(surface, RED, pygame.Rect(SCALE_FACTOR * 2, SCREEN_HEIGHT - SCALE_FACTOR, BUTTON_WIDTH, BUTTON_HEIGHT))
    surface.blit(text_image, (25*SCREEN_WIDTH*0.005, (SCREEN_HEIGHT - SCALE_FACTOR)*1.04))

def handle_button_run(instructions):
    instructions = instructions.lower().split('\n')
    for ins in instructions:
        match ins:
            case "move up" | "move down" | "move left" | "move right":
                farm.farmer.move(ins[5])
            case "plant up" | "plant down" | "plant left" | "plant right":
                farm.farmer.plant(ins[6])
            case "harvest up" | "harvest down" | "harvest left" | "harvest right":
                farm.farmer.harvest(ins[8])
        render_all()
        time.sleep(1)
    user_input = ""

def handle_button_reset():
    farm.__init__()
    farm.add_farmer()
    user_input = ""

def render_all():
    render_farm()
    draw_grid(surface, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR)
    render_text_input(user_input)
    render_button_run()
    render_button_reset()
    pygame.display.flip()

# main loop
running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            elif event.key == pygame.K_RETURN:
                user_input += '\n'
            elif event.key == pygame.K_LSHIFT:
                pass
            else:
                user_input += chr(event.key)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 0 <= mouse[0] <= SCALE_FACTOR*2 and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT:
                handle_button_run(user_input)
            if SCALE_FACTOR*2 <= mouse[0] <= SCALE_FACTOR*4 and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT:
                handle_button_reset()
        
        render_all()
pygame.quit()
sys.exit()