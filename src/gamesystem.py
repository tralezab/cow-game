import pygame
from src.clickable import handle_click_events
from src.cow import cows, Cow
from src.tilegen import TileGen
from src._consts import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, INITIAL_COW_AMOUNT

class CowGame():
    def __init__(self) -> None:
        pygame.init()
        self.game_setup()
        self.game_loop()
        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        should_continue = handle_system_events(events)
        if not should_continue:
            return False
        handle_click_events(events)
        return True

    def spawn_cows(self, amt):
        # Create some cows and add them to the group        
        for i in range(amt):
            cow = Cow()
            cows.add(cow)

    def game_setup(self):
        # Clock to limit framerate
        self.clock = pygame.time.Clock()
        # Create a screen object
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tile_gen = TileGen()
        self.spawn_cows(INITIAL_COW_AMOUNT)

    def game_loop(self):
        running = True
        while running:
            if not self.handle_events():
                break

            # Update sprites    
            cows.update()

            # Blit the tile surface on the screen at (0, 0)
            self.screen.blit(self.tile_gen.tile_surface, (0, 0))

            # Draw all the cows on the screen
            cows.draw(self.screen)

            # Update the display
            pygame.display.flip()

            self.clock.tick(FPS)

def handle_system_events(event_list):
    for event in event_list:
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
    return True
