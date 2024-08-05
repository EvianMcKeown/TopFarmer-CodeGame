import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK,GRAY, GREEN, font
from command_block import CommandBlock
from character import Character
from utils import *

pygame.init()

# draw screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GTA 6")

clock = pygame.time.Clock()

# code drag quence area
sequence_area = pygame.Rect(500, 50, 250, 500)
sequence = []

# available commands
commands = ["UP", "DOWN", "LEFT", "RIGHT"]
command_blocks = [CommandBlock(50, 50 + i * 60, commands[i]) for i in range(len(commands))]


execute_button = pygame.Rect(300, 500, 150, 50)
character = Character()

#move sequence and timing
move_sequence = []
move_index = 0
move_timer = 0

def draw_grid(screen, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, GRAY, (0, y), (width, y))


#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for block in command_blocks:
            block.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if execute_button.collidepoint(event.pos):
                move_sequence = sequence.copy()
                move_index = 0
                move_timer = 0
                sequence.clear()  # Clear sequence after starting execution
                

    # Handle dragging of command blocks
    handle_dragging(command_blocks, sequence_area, sequence)

    # Handle character animation
    if move_sequence and move_index < len(move_sequence):
        move_timer += clock.get_time()
        if move_timer >= 500:
            if not character.moving:
                character.set_target(move_sequence[move_index])
                move_index += 1
            move_timer = 0

    character.update()

    screen.fill(WHITE)
    
    #pygame.draw.rect(screen, WHITE, sequence_area)

    draw_grid(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 50)

   

    # Draw command blocks/buttons
    for block in command_blocks:
        block.draw(screen)

    # Draw code drag sequence area
    pygame.draw.rect(screen, BLACK, sequence_area , 3)
    for i, cmd in enumerate(sequence): #index of command and command type in sequence array
        text_surf = font.render(cmd, True, BLACK)
        screen.blit(text_surf, (sequence_area.x + 10, sequence_area.y + 10 + i*40))

    #draw execute button
    pygame.draw.rect(screen, GREEN, execute_button)
    text_surf = font.render("EXECUTE", True, BLACK)
    screen.blit(text_surf, (execute_button.x + 10, execute_button.y + 10))

    # Draw character
    character.draw(screen)
    


    pygame.display.flip()
    clock.tick(50)
    

pygame.quit()
sys.exit()
