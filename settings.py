# This class contains the settings for the Alien Invasion Game

class Settings:
    def __init__(self):
        """Initialize static settings."""
        # Screen Settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (230, 230, 230)

        # Ship Settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        self.super_bullet_width = 8
        self.super_bullet_height = 30
        self.super_bullet_color = (200, 60, 60)
        self.bullets_allowed = 3
        self.lvl_2_bullets_allowed = 6

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        self.level = 1

        self.mute = False

    def raise_level(self):
        self.level += 1

    def initialize_dynamic_settings(self):
        """Initialize settings that change durring the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.4
        self.fleet_direction = 1 # 1 = moves to the right, -1 = moves to the left
        self.initial_drop_speed = 25
        self.fleet_drop_speed = 10
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.initial_drop_speed += 0.5

        self.alien_points = int(self.alien_points * self.score_scale)
