import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Building the model for an alien"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.level = self.settings.level

        self.x = float(self.rect.x)

    def check_edges(self):
        """check if alien is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """updates the screen for the alien"""
        if self.level < 5:

            self.x += (self.settings.alien_speed * self.settings.fleet_direction)
            self.rect.x = self.x

        elif self.level >= 5:
            if self.settings.fleet_direction == 1:
                self.settings.fleet_drop_speed = self.settings.initial_drop_speed
                self.x += (self.settings.alien_speed * self.settings.fleet_direction)
                self.rect.x = self.x

            elif self.settings.fleet_direction == -1:
                self.settings.fleet_drop_speed = -10
                self.x += (self.settings.alien_speed * self.settings.fleet_direction)
                self.rect.x = self.x
