# Text based farm game demo (main)
# By Mustafa Mohamed
# modified: 13 Aug 2024 by Zahra Bawa

# exec func used, user text box functions expanded, loops and conditionals possible

import pygame
import sys
import time
import tkinter
from farm import FarmGrid
from sprites import *

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

DIRT = (139, 69, 19)
GRASS = (148, 180, 5)
WATER = (30, 144, 255)
CROP = (255, 69, 0)

POTATO = (183, 146, 104)
CARROT = (255, 117, 24)
PUMPKIN = (237, 145, 33)

SCALE_FACTOR = 50
FARM_WIDTH = 10
FARM_HEIGHT = 10
SIDE_WIDTH = SCALE_FACTOR * 8
BUTTON_WIDTH = SCALE_FACTOR * 2
BUTTON_HEIGHT = SCALE_FACTOR * 1
SCREEN_WIDTH = FARM_WIDTH * SCALE_FACTOR + SIDE_WIDTH
SCREEN_HEIGHT = FARM_HEIGHT * SCALE_FACTOR

# Initialize farm with farmer
farm = FarmGrid(FARM_WIDTH, FARM_HEIGHT)
farm.add_farmer()

# Initialize pygame
pygame.init()
pygame.display.set_caption("TopFarmer")
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# keypress repeating
pygame.key.set_repeat(400, 50)


user_input = ""
cursor_x = 0  # Cursor column position
cursor_y = 0  # Cursor row position
text_lines = [""]  # List to handle multi-line text


def draw_grid(surface, width, height, cell_size):
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
            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(
                    x * SCALE_FACTOR + SIDE_WIDTH,
                    y * SCALE_FACTOR,
                    SCALE_FACTOR,
                    SCALE_FACTOR,
                ),
            )

            # draw sprites on top of square
            if color == POTATO:
                # scale image
                potato2 = pygame.transform.scale(potato1, (SCALE_FACTOR, SCALE_FACTOR))
                # then draw sprite
                surface.blit(
                    potato2,
                    (
                        x * SCALE_FACTOR + SIDE_WIDTH,
                        y * SCALE_FACTOR,
                        SCALE_FACTOR,
                        SCALE_FACTOR,
                    ),
                )


def render_text_input():
    pygame.draw.rect(surface, BLACK, pygame.Rect(0, 0, SIDE_WIDTH, SCREEN_HEIGHT))
    y_offset = SCALE_FACTOR
    for i, line in enumerate(text_lines):
        text_image = pygame.font.SysFont(None, 24).render(line, True, GREEN)
        pygame.draw.rect(
            surface, BLACK, pygame.Rect(0, y_offset + (i * 24), SIDE_WIDTH, 24)
        )
        surface.blit(text_image, (0, y_offset + (i * 24)))
        if i == cursor_y:
            # Draw cursor
            cursor_pos = pygame.font.SysFont(None, 24).render(
                line[:cursor_x], True, GREEN
            )
            cursor_x_pos = cursor_pos.get_width()
            pygame.draw.line(
                surface,
                GREEN,
                (cursor_x_pos, y_offset + (i * 24)),
                (cursor_x_pos, y_offset + (i * 24) + 24),
                2,
            )


def render_button(txt, clr, bg, x, y, w, h):
    text_image = pygame.font.SysFont(None, int(SCALE_FACTOR / 2)).render(txt, True, clr)
    pygame.draw.rect(
        surface,
        bg,
        pygame.Rect(
            SCALE_FACTOR * x, SCALE_FACTOR * y, w * SCALE_FACTOR, h * SCALE_FACTOR
        ),
    )
    surface.blit(
        text_image, ((x + 1.12) * SCALE_FACTOR - len(txt) * 7, y * SCALE_FACTOR + 16)
    )


def render_inventory():
    text_image = pygame.font.SysFont(None, int(SCALE_FACTOR / 2)).render(
        str(farm.farmer.get_inventory()), True, BLACK
    )
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, SIDE_WIDTH, BUTTON_HEIGHT))
    surface.blit(text_image, (30, 15))


def execute_python_code(code):
    try:
        exec(code, {"farm": farm, "print": print}, globals())
    except Exception as e:
        print(f"Error: {e}")


def handle_button_run():
    global user_input
    user_input = "\n".join(text_lines)
    user_input = user_input.strip()
    if user_input:
        # split by lines '\n', so that every line is show as it is executed
        user_input_list = user_input.split("\n")
        final_user_input = ""
        for line in user_input_list:
            final_user_input += line + "\n"
            if line[-1] != ":":
                if line[:4] == "    ":
                    final_user_input += "    "
                final_user_input += "render_all()\n"
                if line[:4] == "    ":
                    final_user_input += "    "
                final_user_input += "time.sleep(1)\n"
        print(final_user_input)
        execute_python_code(final_user_input)
        # render_all()
        # print(farm)
        # time.sleep(1)
    # render_all()
    # print(farm)
    # time.sleep(1)


def handle_button_clear():
    global text_lines, cursor_x, cursor_y
    text_lines = [""]
    cursor_x = 0
    cursor_y = 0


def handle_button_reset():
    global farm, text_lines, cursor_x, cursor_y
    farm = FarmGrid(FARM_WIDTH, FARM_HEIGHT)
    farm.add_farmer()
    text_lines = [""]
    cursor_x = 0
    cursor_y = 0


def handle_button_help():
    message = 'Move the farmer: farm.farmer.move("direction")\n'
    message += "direction can be left, right, up, down\n\n"
    message += 'Plant a crop: farm.farmer.plant("crop", "direction")\n'
    message += "crop can be potato, carrot, pumpkin\n\n"
    message += 'Harvest a crop: farm.farmer.harvest("direction")\n\n'
    root = tkinter.Tk()
    root.geometry("400x200")
    w = tkinter.Label(root, text="How to play", font="50")
    w.pack()
    msg = tkinter.Message(root, text=message, width=600)
    msg.pack()
    root.mainloop()


def render_all():
    render_farm()
    draw_grid(surface, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR)
    render_text_input()
    render_button("RUN", WHITE, GREEN, 0, 9, 2, 1)
    render_button("CLEAR", WHITE, BLUE, 2, 9, 2, 1)
    render_button("RESTART", WHITE, RED, 4, 9, 2, 1)
    render_button("HELP", BLACK, YELLOW, 6, 9, 2, 1)
    render_inventory()
    pygame.display.flip()


def handle_key_press(event):
    global cursor_x, cursor_y, text_lines

    if event.key == pygame.K_BACKSPACE:
        line = text_lines[cursor_y]
        if cursor_x > 0:
            text_lines[cursor_y] = line[: cursor_x - 1] + line[cursor_x:]
            cursor_x -= 1
        elif cursor_y > 0:
            cursor_x = len(text_lines[cursor_y - 1])
            text_lines[cursor_y - 1] += line
            text_lines.pop(cursor_y)
            cursor_y -= 1

    elif event.key == pygame.K_RETURN:
        if cursor_y + 1 >= len(text_lines):
            text_lines.append("")
        line = text_lines[cursor_y]
        text_lines[cursor_y] = line[:cursor_x]
        text_lines.insert(cursor_y + 1, line[cursor_x:])
        cursor_y += 1
        cursor_x = 0

    elif event.key == pygame.K_TAB:
        line = text_lines[cursor_y]
        text_lines[cursor_y] = line[:cursor_x] + " " * 4 + line[cursor_x:]
        cursor_x += 4

    elif event.key == pygame.K_LEFT:
        if cursor_x > 0:
            cursor_x -= 1
        elif cursor_y > 0:
            cursor_y -= 1
            cursor_x = len(text_lines[cursor_y])

    elif event.key == pygame.K_RIGHT:
        if cursor_x < len(text_lines[cursor_y]):
            cursor_x += 1
        elif cursor_y + 1 < len(text_lines):
            cursor_y += 1
            cursor_x = min(cursor_x, len(text_lines[cursor_y]))

    elif event.key == pygame.K_UP:
        if cursor_y > 0:
            cursor_y -= 1
            cursor_x = min(cursor_x, len(text_lines[cursor_y]))

    elif event.key == pygame.K_DOWN:
        if cursor_y + 1 < len(text_lines):
            cursor_y += 1
            cursor_x = min(cursor_x, len(text_lines[cursor_y]))

    else:
        if event.unicode:  # Only add if the unicode character is valid
            line = text_lines[cursor_y]
            text_lines[cursor_y] = line[:cursor_x] + event.unicode + line[cursor_x:]
            cursor_x += 1


def play_music(type):
    if type == "theme":
        # pygame.mixer.music.load("./FarmGameTextBased_ExecFunc/resources/Capstone-CodeGame.mp3")
        pygame.mixer.music.load(
            "./FarmGameTextBased_ExecFunc/resources/CodeGameTest.mp3"
        )
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(0, 0, 5000)
        pygame.mixer.music.fadeout(5)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(
            "./FarmGameTextBased_ExecFunc/resources/Capstone-CodeGame.mp3"
        )
        pygame.mixer.music.play(0, 0, 5000)


# Main loop
running = True
play_music("theme")
while running:
    for event in pygame.event.get():
        if not pygame.mixer.music.get_busy():
            play_music("theme")

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            handle_key_press(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if (
                0 <= mouse[0] <= SCALE_FACTOR * 2
                and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT
            ):
                handle_button_run()
            if (
                SCALE_FACTOR * 2 <= mouse[0] <= SCALE_FACTOR * 4
                and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT
            ):
                handle_button_clear()
            if (
                SCALE_FACTOR * 4 <= mouse[0] <= SCALE_FACTOR * 6
                and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT
            ):
                handle_button_reset()
            if (
                SCALE_FACTOR * 6 <= mouse[0] <= SCALE_FACTOR * 8
                and SCREEN_HEIGHT - SCALE_FACTOR <= mouse[1] <= SCREEN_HEIGHT
            ):
                handle_button_help()

        render_all()
pygame.quit()
sys.exit()
