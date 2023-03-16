import pygame

# List of all things that are clickables
clickables = []

class Clickable(pygame.sprite.Sprite):
    def __init__(self) -> None:
        # Call the parent class constructor
        super().__init__()
        self.rect: pygame.Rect = None
        clickables.append(self)

    def left_click(self):
        pass

def handle_click_events(event_list):
    for event in event_list:
        if event.type != pygame.MOUSEBUTTONDOWN:
            continue
        # Check if the mouse position collides with the cow's rect
        mouse_pos = pygame.mouse.get_pos()
        can_be_clicked: Clickable
        for can_be_clicked in clickables:
            if can_be_clicked.rect.collidepoint(mouse_pos):
                if event.button == 1:
                    can_be_clicked.left_click()
