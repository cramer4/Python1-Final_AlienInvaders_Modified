
class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        # Start game in an inactive state.
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.super_bullet_charge = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.level = 1
        self.super_bullet_charge = 0

    def raise_level(self):
        self.level += 1
