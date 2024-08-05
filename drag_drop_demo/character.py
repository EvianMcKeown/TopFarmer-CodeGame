import pygame
from settings import BLUE

class Character:
    def __init__(self):
        self.rect = pygame.Rect(200, 200, 50, 50)
        self.color = BLUE
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.moving = False
        self.direction = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def set_target(self, direction):
        self.direction = direction
        self.moving = True
        if direction == "UP":
            self.target_y = self.rect.y - 50
        elif direction == "DOWN":
            self.target_y = self.rect.y + 50
        elif direction == "LEFT":
            self.target_x = self.rect.x - 50
        elif direction == "RIGHT":
            self.target_x = self.rect.x + 50

    def update(self):
        if self.moving:
            if self.direction == "UP":
                self.rect.y -= 7
            elif self.direction == "DOWN":
                self.rect.y += 7
            elif self.direction == "LEFT":
                self.rect.x -= 7
            elif self.direction == "RIGHT":
                self.rect.x += 7

            if abs(self.rect.x - self.target_x) < 2 and abs(self.rect.y - self.target_y) < 2:
                self.rect.x = self.target_x
                self.rect.y = self.target_y
                self.moving = False
