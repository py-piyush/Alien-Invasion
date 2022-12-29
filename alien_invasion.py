import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


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

        # Full screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)

    def run_game(self) -> None:
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Responds to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Store high score if game is complete
                if not self.stats.game_active:
                    high_score = self.stats.high_score
                    self.sb.store_high_score(high_score)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to right
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            # Store high score if game is complete
            if not self.stats.game_active:
                high_score = self.stats.high_score
                self.sb.store_high_score(high_score)
            sys.exit()

    def _check_keyup(self, event):
        """Respond to keyreleases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks Play"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Reset the game statistics and settings
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.settings.initialize_dynamic_settings()

            # Get rid of any remaining aliens and bulets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

    def __ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old ones"""
        self.bullets.update()
        # Get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_colisions()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Create an alien and find the number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width, alien.rect.height
        available_space_x = self.settings.screen_width - (
            self.settings.screen_width // 3
        )
        number_aliens_x = available_space_x // int(1.5 * alien_width)

        # Determine number of rows that fit on screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height // 2
        number_rows = available_space_y // int(1.5 * alien_height)

        # Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(row_number, alien_number)

    def _create_alien(self, row_number, alien_number):
        """Create and alien and place it in row"""
        alien = Alien(self)
        margin_left = (self.settings.screen_width // 3) // 2
        alien_width, alien_height = alien.rect.size
        alien.x = margin_left + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 1.5 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached and edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.__ship_hit()

        # Look for aliens hitting the bottom
        self._check_aliens_bottom()

    def _check_bullet_alien_colisions(self):
        """Respond to bullet alien collision"""
        # Check for collisions
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # Update score
            for aliens in collisions.values():
                self.stats.score += self.settings.points
                self.sb.prep_score()
                self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.__ship_hit()
                break

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # Draw the play button if game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()
        # display.flip() will update the contents of the entire display
        # display.update() allows to update a portion of the screen, instead of the entire area of the screen. Passing no arguments, updates the entire display


if __name__ == "__main__":
    # Make a game instance, and run the game
    game = AlienInvasion()
    game.run_game()
