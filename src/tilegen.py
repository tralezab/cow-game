import pygame
import random
from src._consts import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class TileGen():
    def __init__(self) -> None:

        # Calculate the number of tiles needed to cover the screen horizontally and vertically
        tiles_x = SCREEN_WIDTH // TILE_SIZE + 1
        tiles_y = SCREEN_HEIGHT // TILE_SIZE + 1

        # Load four images of grass tiles and store them in a list
        grass_images = [pygame.image.load("img/grass1.png"), pygame.image.load("img/grass2.png"), pygame.image.load("img/grass3.png"), pygame.image.load("img/grass4.png")]

        # Create a nested list to store the random indices for each tile
        tile_indices = []

        # Create a surface to hold all the tiles
        self.tile_surface = pygame.Surface((tiles_x * TILE_SIZE, tiles_y * TILE_SIZE))


        # Loop through each row of tiles
        for y in range(tiles_y):
            # Create an empty list for this row
            row = []
            # Loop through each column of tiles
            for x in range(tiles_x):
                # Choose a random index between 0 and 3 (inclusive)
                index = random.randint(0, 3)
                # Append the index to the row list
                row.append(index)
                # Blit the corresponding grass image on the tile surface at this position
                self.tile_surface.blit(grass_images[index], (x * TILE_SIZE, y * TILE_SIZE))
            # Append the row list to the tile indices list
            tile_indices.append(row)
