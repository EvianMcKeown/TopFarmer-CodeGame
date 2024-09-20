# tilegraphics.py

import pygame


class TileGraphics:
    """
    Handles the graphical representation of tiles, including crops, trees, and the farmer sprite.
    This class manages the loading of images, scaling of graphics, and rendering of animated sprites on the game surface, providing visual elements for the farm environment.
    """

    def __init__(self, scale_factor, farmer_scale=(64, 64)):
        """
        Initializes the TileGraphics object, setting the scale factors for tile and farmer graphics.
        This constructor prepares the necessary attributes for rendering graphics, including loading the graphics and initializing frame timing for animations.

        Args:
            scale_factor: A float representing the scaling factor for tile graphics.
            farmer_scale: A tuple representing the size of the farmer sprite (default is (64, 64)).
        """
        self.scale_factor = scale_factor
        self.farmer_scale = farmer_scale  # scale size for the farmer sprite
        self.load_graphics()
        self.farmer_frame_index = 0
        self.last_update_time = pygame.time.get_ticks()  # For frame timing
        self.frame_delay = 200  # Time between frames in milliseconds

    def load_graphics(self):
        """
        Loads graphical assets for crops and the farmer sprite sheet from the specified assets folder.
        This function initializes the images for trees, crops, and the farmer's animations, scaling them appropriately for use in the game.
        """
        # load tree img
        self.tree_img = pygame.image.load("assets/tree1.png").convert_alpha()
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
            0: pygame.image.load("assets/potato1.png").convert_alpha(),
            1: pygame.image.load("assets/carrot1.png").convert_alpha(),
            2: pygame.image.load("assets/pumpkin1.png").convert_alpha(),
        }

        # scale crop images to match the grid tile size
        for key in self.crop_images:
            self.crop_images[key] = pygame.transform.scale(
                self.crop_images[key], (self.scale_factor, self.scale_factor)
            )

    def get_farmer_frame(self):
        """
        Retrieves the current frame of the farmer sprite for animation.
        This function updates the farmer's frame index based on the elapsed time, ensuring smooth animation by cycling through the available frames, and returns the current frame to be rendered.

        Returns:
            Surface: The current farmer sprite frame to be displayed.
        """

        # Update farmerframe based on time
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.farmer_frame_index = (self.farmer_frame_index + 1) % len(
                self.farmer_sprites
            )
            self.last_update_time = current_time

        return self.farmer_sprites[self.farmer_frame_index]

    def render_farmer(self, surface, x, y):
        """
        Renders the farmer sprite animation at a specified position on the given surface.
        This function retrieves the current frame of the farmer sprite, calculates the appropriate position to center the sprite on a tile, and draws it on the specified surface.

        Args:
            surface: The Pygame surface on which to draw the farmer sprite.
            x: The x-coordinate of the tile where the farmer sprite should be rendered.
            y: The y-coordinate of the tile where the farmer sprite should be rendered.
        """
        farmer_frame = self.get_farmer_frame()

        # Adjust the farmer  position to center the sprite on a tile
        offset_x = (self.scale_factor - self.farmer_scale[0]) // 2
        offset_y = (self.scale_factor - self.farmer_scale[1]) // 2

        surface.blit(
            farmer_frame,
            (
                x * self.scale_factor + offset_x,
                y * self.scale_factor + offset_y,
            ),
        )

    def render_crop(self, surface, crop_type, x, y):
        """Draws crop image on specified tile of the given surface.

        Args:
            surface: The Pygame surface on which to draw the crop image.
            crop_type: An integer representing the type of crop to render.
            x: The x-coordinate of the tile where the crop image should be rendered.
            y: The y-coordinate of the tile where the crop image should be rendered.
        """
        # Get the crop image based on crop type and render (blit) it
        if crop_type in self.crop_images:
            crop_image = self.crop_images[crop_type]
            surface.blit(
                crop_image, (x * self.scale_factor, y * self.scale_factor)
            )

    def render_tree(self, surface, x, y):
        """
        Renders the tree image on a specified tile of the given surface.
        This function draws the tree image at the calculated position based on the provided coordinates, allowing for visual representation of trees in the game.

        Args:
            surface: The Pygame surface on which to draw the tree image.
            x: The x-coordinate of the tile where the tree image should be rendered.
            y: The y-coordinate of the tile where the tree image should be rendered.
        """
        tree_image = self.tree_img
        surface.blit(tree_image, (x * self.scale_factor, y * self.scale_factor))
