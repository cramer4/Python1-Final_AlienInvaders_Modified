import pygame
from settings import Settings

class Title_screen:

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = Settings()
        # Load the ship image and get its rect.
        self.image = pygame.image.load("images/title.jpg")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.center = self.screen_rect.center

    def show_title_screen(self):
        self.screen.blit(self.image, self.rect)
