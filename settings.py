#! python3
# settings.py: To store settings of Alien invasion


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship setting
        # self.ship_speed = 1.5: Will change with level
        self.ship_limit = 3

        # Bullet settings
        # self.bullet_speed = 1.0: will change with level
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        # self.alien_speed = 1.0: will change with level
        self.fleet_drop_speed = 10
        # self.fleet_direction = 1

        # How quickly the game speeds
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that can change throughuot the game"""
        self.ship_speed = 1.5

        self.bullet_speed = 3.0

        self.alien_speed = 1.0
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
