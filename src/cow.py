from src.clickable import Clickable
from src._consts import SCREEN_WIDTH, SCREEN_HEIGHT
import src._helpers as hp
import numpy as np
import random
import pygame

COW_SPEED_VARIANCE = 0.20
COW_SPEED_VARIANCE_STEP = 0.01

# Load an image of a cow and get its rect
cow_image = pygame.image.load("img/cow.png")
cow_rect = cow_image.get_rect()

# Create a sprite group to hold all the cows        
cows = pygame.sprite.Group()

# Define a class for the cow sprite
class Cow(Clickable):
    # Constructor method
    def __init__(self):
        # Call the parent class constructor
        super().__init__()

        # Set the image and rect attributes
        self.image = cow_image
        self.rect = cow_rect.copy()

        self.name = "Cow"
        self.agility = random.choice(np.arange(0.25, 1.75, 0.25).tolist())

        # Create CowInfo for this cow
        self.info_panel = CowInfo(self)

        # Set a random position and speed for the cow
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.choice([-self.agility, self.agility])
        self.speed_y = random.choice([-self.agility, self.agility])
        self.speed_x_variance = random.choice(np.arange(-COW_SPEED_VARIANCE, COW_SPEED_VARIANCE, COW_SPEED_VARIANCE_STEP).tolist())
        self.speed_y_variance = random.choice(np.arange(-COW_SPEED_VARIANCE, COW_SPEED_VARIANCE, COW_SPEED_VARIANCE_STEP).tolist())

        # Add a clicked attribute to store whether the cow is clicked or not
        self.clicked = False

    # Update method to move the cow around randomly
    def update(self):
        print('agility: ', self.agility, "speed_x:", self.speed_x)
        self.update_movement()

    def get_clamped_speed(self, speed):
        # Generate a random number between -0.1 and 0.1
        delta = random.uniform(-COW_SPEED_VARIANCE_STEP, COW_SPEED_VARIANCE_STEP)

        # Add or subtract the delta from the speed value
        speed += delta

        # Clamp the speed value between a minimum and maximum value
        speed = max(min(speed, self.agility + COW_SPEED_VARIANCE), self.agility - COW_SPEED_VARIANCE)

        # Return the modified speed value
        return speed

    def update_movement(self):
        # Get the modified speed_x value from the function
        self.speed_x = self.get_clamped_speed(self.speed_x)

        # Get the modified speed_y value from the function    
        self.speed_y = self.get_clamped_speed(self.speed_y)

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

    def left_click(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.info_panel.image.set_alpha(255)

# Define a new class for the cow info window
class CowInfo(Clickable):
    def __init__(self, cow: Cow):
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
