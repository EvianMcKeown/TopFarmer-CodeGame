# tilegraphics.py

import pygame


class TileGraphics:
    def __init__(self, scale_factor, farmer_scale=(64, 64)):  # Farmer scale
        self.scale_factor = scale_factor
        self.farmer_scale = farmer_scale  # scale size for the farmer sprite
        self.load_graphics()
        self.farmer_frame_index = 0
        self.last_update_time = pygame.time.get_ticks()  # For frame timing
        self.frame_delay = 200  # Time between frames in milliseconds

    def load_graphics(self):
        """loads images from assets folder for crop images and farmer spritesheet for animation"""

        self.tree_img = pygame.image.load("assets/tree.png").convert_alpha()
        self.tree_img = pygame.transform.scale(
            self.tree_img, (self.scale_factor, self.scale_factor)
        )
        # Load the farmer sprite sheet (ensure it's 48x48 per frame)
        self.farmer_sprite_sheet = pygame.image.load(
            "assets/farmer_idle.png"
        ).convert_alpha()
        self.farmer_sprites = []

        # Assuming there are 2 frames in a row and the sprites are 48x48
        for i in range(2):  # 2 frames in the sheet
            frame = self.farmer_sprite_sheet.subsurface(
                (i * 48, 0, 48, 48)
            )  # Cut images from sheet
            scaled_frame = pygame.transform.scale(
                frame, self.farmer_scale
            )  # Scale farmer frames
            self.farmer_sprites.append(scaled_frame)
        # Load crop images (32x32)
        self.crop_images = {
            0: pygame.image.load("assets/potato.png").convert_alpha(),
            1: pygame.image.load("assets/carrot.png").convert_alpha(),
            2: pygame.image.load("assets/pumpkin.png").convert_alpha(),
        }

        # scale crop images to match the grid tile size
        for key in self.crop_images:
            self.crop_images[key] = pygame.transform.scale(
                self.crop_images[key], (self.scale_factor, self.scale_factor)
            )

    def get_farmer_frame(self):
        # Update farmerframe based on time
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.farmer_frame_index = (self.farmer_frame_index + 1) % len(
                self.farmer_sprites
            )
            self.last_update_time = current_time

        return self.farmer_sprites[self.farmer_frame_index]

    def render_farmer(self, surface, x, y):
        """draws farmer sprite animation at specified position"""
        farmer_frame = self.get_farmer_frame()

        # Adjust the farmer  position to center the sprite on a tile
        offset_x = (self.scale_factor - self.farmer_scale[0]) // 2
        offset_y = (self.scale_factor - self.farmer_scale[1]) // 2

        surface.blit(
            farmer_frame,
            (x * self.scale_factor + offset_x, y * self.scale_factor + offset_y),
        )

    def render_crop(self, surface, crop_type, x, y):
        """draws crop image on specified tile"""
        # Get the crop image based on crop type and render (blit) it
        if crop_type in self.crop_images:
            crop_image = self.crop_images[crop_type]
            surface.blit(crop_image, (x * self.scale_factor, y * self.scale_factor))

    def render_tree(self, surface, x, y):
        """draws tree image on specified tile"""
        tree_image = self.tree_img
        surface.blit(tree_image, (x * self.scale_factor, y * self.scale_factor))
