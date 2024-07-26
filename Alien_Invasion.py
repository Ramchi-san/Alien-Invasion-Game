import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_ship import Alien_Ship

class Alien_Invasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initializes the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_ships = pygame.sprite.Group()

        self._create_fleet()
    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
    
   
    def _check_events(self):
        """Responds to mouse presses and key clicks"""
         #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.KEYDOWN_event_check(event)
            elif event.type == pygame.KEYUP:
                self.KEYUP_event_check(event)    
    
    def KEYDOWN_event_check(self, event):
        """Responds to key presses"""
        if event.key == pygame.K_RIGHT:
            #Move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            #Move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def KEYUP_event_check(self, event):
        """"Responds to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        #Update bullet position
        self.bullets.update()
        
        #Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create the fleet of alien ships"""
        #Create an alien ship and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien_ship = Alien_Ship(self)
        alien_ship_width = alien_ship.rect.width
        available_space_x = self.settings.screen_width - (2*alien_ship_width)
        number_alien_ships_x = available_space_x // (2 * alien_ship_width)

        #Create the first row of aliens
        for alien_ship_number in range(number_alien_ships_x):
            #Create an alien ship and place it in the row.
            alien_ship = Alien_Ship(self)
            alien_ship.x = alien_ship_width + 2 * alien_ship_width * alien_ship_number
            alien_ship.rect.x = alien_ship.x
            self.alien_ships.add(alien_ship)

    def _update_screen (self):
        """Update new images on the screen, and flip the new screen"""
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.alien_ships.draw(self.screen)

        #Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    #Make a game instance, and run the game
    alien_invasion = Alien_Invasion()
    alien_invasion.run_game()
