import sys
from time import sleep

import pygame

from pygame import mixer
mixer.init()
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from super_bullet import Super_bullet
from title_screen import Title_screen
import sfx

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((1920, 1080))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)

        self.title = Title_screen(self)

        # Draw scoreboard information
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.ship2 = Ship(self)
        self.ship2.rect.x = (self.ship.x + 75)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Make the Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""

        if not self.stats.game_active:
            mixer.init()
            mixer.music.load("sounds/game_music.mp3")
            if not self.settings.mute:
                mixer.music.play(-1)

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                if self.stats.level >= 2:
                    self.ship2.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT and self.ship2.x < self.screen_rect.right:
            self.ship.moving_right = True
            self.ship2.moving_right = True

        elif event.key == pygame.K_LEFT and self.ship.x > 0:
            self.ship.moving_left = True
            self.ship2.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.ship2.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.ship2.moving_left = False

    def reset_charge(self):
        self.stats.super_bullet_charge = 0

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:

            if self.stats.level >= 2:
                if self.stats.super_bullet_charge >= 50:
                    if not self.settings.mute:
                        sfx.sound_effect(sfx.fire)
                    self.super_bullet = True
                    self.reset_charge()
                    for x in range(0, 10):
                        super_bullet = Super_bullet(self)
                        self.bullets.add(super_bullet)
                        super_bullet2 = Super_bullet(self)
                        super_bullet2.rect.midtop = self.ship2.rect.midtop
                        self.bullets.add(super_bullet2)

                else:
                    if not self.settings.mute:
                        sfx.sound_effect(sfx.fire)
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)
                    new_bullet2 = Bullet(self)
                    new_bullet2.rect.midtop = self.ship2.rect.midtop
                    self.bullets.add(new_bullet2)

            else:
                if self.stats.super_bullet_charge >= 50:
                    if not self.settings.mute:
                        sfx.sound_effect(sfx.fire)
                    self.super_bullet = True
                    self.reset_charge()
                    for x in range(0, 20):
                        super_bullet = Super_bullet(self)
                        self.bullets.add(super_bullet)
                else:

                    if not self.settings.mute:
                        sfx.sound_effect(sfx.fire)
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
         # Remove any bullets and aliens that have collided.

        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                if not self.settings.mute:
                    sfx.sound_effect(sfx.alien_hit)
                self.stats.score += self.settings.alien_points * len(alien)
                self.stats.super_bullet_charge += 1
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:

            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.aliens.empty()
            if not self.settings.mute:
                sfx.sound_effect(sfx.level_up)

            self.stats.raise_level()
            self.settings.raise_level()
            self._create_fleet()

            self.settings.increase_speed()
            self.sb.prep_level()

            sleep(2.3)

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._hit_ship()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._hit_ship()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        self.levelup_aliens()

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        if self.stats.level >= 2:
            self.ship2.x = (self.ship.x + 75)
            self.ship2.blitme()

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw scoreboard infomation

        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.title.show_title_screen()
            self.play_button.draw_button()
        pygame.display.flip()

    def _hit_ship(self):
        self.stats.super_bullet_charge = 0
        if self.stats.ships_left > 0:

            if not self.settings.mute:
                sfx.sound_effect(sfx.ship_hit)
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            self.ship2.rect.x = self.x = float(self.ship2.rect.x)
            self.sb.prep_ships()

            sleep(1)
        else:
            if not self.settings.mute:
                sfx.sound_effect(sfx.game_over)
            sleep(3.3)
            self.stats.game_active = False
            self.settings.fleet_drop_speed = 10

    def check_play_button(self, mouse_pos):
        """Start a new game when the Player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings

            self.settings.initialize_dynamic_settings()
            pygame.mixer.music.pause()

            if not self.settings.mute:
                sfx.sound_effect(sfx.load_up)
            sleep(1.5)
            # Reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.reset_score()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

    def levelup_aliens(self):
        if self.stats.level == 1:
            pass
        if self.stats.level == 2:
            for alien in self.aliens:
                alien.image = pygame.image.load("images/lvl2_alien.jpg")
        if self.stats.level == 3:
            for alien in self.aliens:
                alien.image = pygame.image.load("images/lvl3_alien.jpg")
        if self.stats.level >= 4:
            for alien in self.aliens:
                alien.image = pygame.image.load("images/lvl4_alien.jpg")


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
