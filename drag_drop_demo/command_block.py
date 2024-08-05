import pygame
from settings import GRAY, BLACK, font

class CommandBlock:
    def __init__(self, x, y, text):
        self.rect =pygame.Rect(x, y, 100, 50)
        self.color =GRAY
        self.text =text
        self.dragging =False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf =font.render(self.text, True, BLACK)
        screen.blit(text_surf, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging =True
                mouse_x, mouse_y =event.pos
                self.offset_x =self.rect.x - mouse_x
                self.offset_y =self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging =False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y
