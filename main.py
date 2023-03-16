# Import pygame and other modules
import pygame
import random

# Initialize pygame
pygame.init()

# Define some colors and constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 32

# Calculate the number of tiles needed to cover the screen horizontally and vertically
tiles_x = SCREEN_WIDTH // TILE_SIZE + 1
tiles_y = SCREEN_HEIGHT // TILE_SIZE + 1

# Create a screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load an image of a cow and get its rect
cow_image = pygame.image.load("cow.png")
cow_rect = cow_image.get_rect()

# Load four images of grass tiles and store them in a list
grass_images = [pygame.image.load("grass1.png"), pygame.image.load("grass2.png"), pygame.image.load("grass3.png"), pygame.image.load("grass4.png")]

# Create a nested list to store the random indices for each tile
tile_indices = []

# Create a surface to hold all the tiles
tile_surface = pygame.Surface((tiles_x * TILE_SIZE, tiles_y * TILE_SIZE))

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
        tile_surface.blit(grass_images[index], (x * TILE_SIZE, y * TILE_SIZE))
    # Append the row list to the tile indices list
    tile_indices.append(row)

# Define a class for the cow sprite
class Cow(pygame.sprite.Sprite):
    # Constructor method
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Set the image and rect attributes
        self.image = cow_image
        self.rect = cow_rect.copy()

        # Set a random position and speed for the cow
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-1, 1])
        self.speed_y = random.choice([-1, 1])

        # Add a clicked attribute to store whether the cow is clicked or not
        self.clicked = False

    # Update method to move the cow around randomly
    def update(self):
        # Move the cow horizontally by its speed_x value
        self.rect.x += self.speed_x

        # Check if the cow has hit the left or right edge of the screen and reverse its direction if so
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1

        # Move the cow vertically by its speed_y value    
        self.rect.y += self.speed_y

        # Check if the cow has hit the top or bottom edge of the screen and reverse its direction if so    
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

    def show_info(self):
        # Check if there is a mouse button down event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the left mouse button is pressed
                if event.button == 1:
                    # Check if the mouse position collides with the cow's rect
                    mouse_pos = pygame.mouse.get_pos()
                    if self.rect.collidepoint(mouse_pos):
                        # If yes, toggle the clicked attribute
                        self.clicked = not self.clicked
                    else:
                        # If no, set the clicked attribute to False
                        self.clicked = False


# Define a new class for the cow info window
class CowInfo(pygame.sprite.Sprite):
    def __init__(self, cow):
        # Call the parent class constructor
        pygame.sprite.Sprite.__init__(self)
        # Set the image and rect attributes
        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        # Draw a black border around the window
        pygame.draw.rect(self.image, (0, 0, 0), self.rect, 2)
        # Create a font object
        self.font = pygame.font.SysFont("Arial", 20)
        # Render the cow's name and agility stat on the window
        self.name_text = self.font.render(cow.name, True, (0, 0, 0))
        self.agility_text = self.font.render(f"Agility: {cow.agility}", True, (0, 0, 0))
        # Blit the texts on the window
        self.image.blit(self.name_text, (10, 10))
        self.image.blit(self.agility_text, (10, 50))
        # Set the position of the window to be centered on the cow
        self.rect.center = cow.rect.center

    def update(self):
        # Check if the mouse is over the window
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            # If yes, make the window slightly transparent
            self.image.set_alpha(200)
        else:
            # If no, make the window fully opaque
            self.image.set_alpha(255)

# Create a sprite group to hold all the cows        
cows = pygame.sprite.Group()
# Create a sprite group for the cow info windows
info_group = pygame.sprite.Group()

# Create some cows and add them to the group        
for i in range(10):
    cow = Cow()
    cows.add(cow)

# Main game loop    
running = True    
while running:
    # Handle events    
    for event in pygame.event.get():
        # Quit if the user closes the window or presses ESC        
        if event.type == pygame.QUIT:
            running = False            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Update sprites    
    cows.update()
    info_group.update()

    # Call the show_info method for each cow in the cows group
    for cow in cows:
        cow.show_info()
        # Check if the cow is clicked
        if cow.clicked:
            # If yes, create a new CowInfo object and add it to the info group
            info = CowInfo(cow)
            info_group.add(info)
        else:
            # If no, remove any existing CowInfo object from the info group that matches this cow's name
            for sprite in info_group:
                if sprite.name_text == cow.name_text:
                    info_group.remove(sprite)

    # Blit the tile surface on the screen at (0, 0)
    screen.blit(tile_surface, (0, 0))

    # Draw all the cows on the screen
    cows.draw(screen)

    # Draw all the cow info windows on the screen
    info_group.draw(screen)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to FPS
    clock.tick(FPS)

# Quit pygame and exit the program
pygame.quit()
