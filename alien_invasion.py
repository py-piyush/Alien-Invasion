import sys
import pygame

from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behaviour"""

    def __init__(self) -> None:
        """Initialize the game, and create game resources"""

        # Creating pygame window
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

    def run_game(self) -> None:
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.settings.bg_color)

            # Make the most recently drawn screen visible
            pygame.display.flip()
            # display.flip() will update the contents of the entire display
            # display.update() allows to update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display


if __name__ == "__main__":
    # Make a game instance, and run the game
    game = AlienInvasion()
    game.run_game()
