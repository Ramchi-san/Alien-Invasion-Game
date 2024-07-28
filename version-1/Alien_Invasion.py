import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien_ship import Alien_Ship
from time import sleep 
from game_stats import Game_Stats
from button import Button
from scoreboard import Scoreboard

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
        self.button = Button(self, "Play")
        self.game_stats = Game_Stats(self)
        self.score_board =  Scoreboard(self)

        self._create_fleet()
    
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien_ships()
            self._update_screen()
    
   
    def _check_events(self):
        """Responds to mouse presses and key clicks"""
         #Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos_inst = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos = mouse_pos_inst)
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
        elif event.key == pygame.K_p:
            self._check_play_button(play_key=True)
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
        #if len(self.bullets) < self.settings.bullets_allowed:
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
        self._detecting_collision()
        
    
    def _detecting_collision(self):
        #Check for any bullets that have hit aliens.
        #If so, rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.alien_ships,
                                                True, True)
        if collisions:
            for alien_ships in collisions.values():
                self.game_stats.game_score += self.settings.alien_ship_points * len(alien_ships)
            self.score_board.prep_score()
            self.score_board.check_high_score() 

        if not self.alien_ships:
            #Destoy the remaining bullets once all the alien ships are destroyed, then create a new fleet.
            self.bullets.empty()
            self.settings.increase_speed()

            #Increase level
            self.game_stats.level += 1
            self.score_board.prep_level()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of alien ships"""
        #Create an alien ship and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width.
        alien_ship = Alien_Ship(self)
        alien_ship_width, alien_ship_height = alien_ship.rect.size
        alien_ship_width = alien_ship.rect.width
        available_space_x = self.settings.screen_width - (2*alien_ship_width)
        number_alien_ships_x = available_space_x // (2 * alien_ship_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_ship_height)
                             - ship_height)
        number_rows = available_space_y // (2 * alien_ship_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            for alien_ship_number in range(number_alien_ships_x):
                self._create_alien_ship(alien_ship_number, row_number)

    def _create_alien_ship(self, alien_ship_number, row_number):
        #Create an alien ship and place it in the row.
        alien_ship = Alien_Ship(self)
        alien_ship_width, alien_ship_height = alien_ship.rect.size
        alien_ship.x = alien_ship_width + 2 * alien_ship_width * alien_ship_number
        alien_ship.rect.x = alien_ship.x
        alien_ship.rect.y = alien_ship.rect.height + 2 * alien_ship.rect.height * row_number
        self.alien_ships.add(alien_ship)
        
    def _update_alien_ships(self):
        """Check if any alien ship is touching the edge then
            Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.alien_ships.update()

        #Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.alien_ships):
            self._ship_hit()
        
        self._check_alien_ship_bottom()
            
    
    def _check_fleet_edges(self):
        """Respond appropriately if any alien ship has reached the edge"""
        for alien_ship in self.alien_ships.sprites():
            if alien_ship.check_edges():
                self._check_change_fleet_direction()
                break
    
    def _check_change_fleet_direction(self):
        """Drop the entire fleet and change the movement direction"""
        for alien_ship in self.alien_ships.sprites():
            alien_ship.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responses to the ship being hit"""
        
        #Decrementing the number of ships available
        if self.game_stats.ships_left > 0:
            #Decrement ships left and update the scoreaboard.
            self.game_stats.ships_left -= 1
            self.score_board.prep_ships()
            #Get rid of any remaining aliens and bullets
            self.alien_ships.empty()
            self.bullets.empty()
 
            #Create a new ship and fleet
            self._create_fleet() 
            self.ship.center_ship()

            #Pause
            sleep(0.5)

        else:
            self.game_stats.game_active = False
            pygame.mouse.set_visible(True)
            """
            self.display_popup()
            sleep(2)
            sys.exit()
            """
    
    def _check_alien_ship_bottom(self):
        """Responds to alien ship reaching the bottom of the screen"""
        screen_rect = self.screen.get_rect()

        for alien_ship in self.alien_ships.sprites():
            if alien_ship.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos = None, play_key = False):
        """Start a new game when play button is clicked"""
        button_collide = None
        if mouse_pos: 
            button_collide = self.button.rect.collidepoint(mouse_pos)

        if (button_collide or play_key) and not self.game_stats.game_active:
            self.game_stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.game_stats.game_active = True
            self.score_board.prep_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()

            #Clear all aliens and bullets
            self.alien_ships.empty()
            self.bullets.empty()

            #Hides the mouse curson
            pygame.mouse.set_visible(False)

                
    def _update_screen (self):
        """Update new images on the screen, and flip the new screen"""
        #Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.alien_ships.draw(self.screen)

        #Draw the button after all the other element when the game isn't active
        if not self.game_stats.game_active:
            self.button.draw_button()
        
        self.score_board.show_score()

        #Make the most recently drawn screen visible
        pygame.display.flip()
    
   



    #Additional functions
    def display_popup(self, message = "Game Over Ship Hit!!!"):
        font = pygame.font.Font(None, 36)
        popup_width, popup_height = 300, 150
        popup_x = (self.settings.screen_width - popup_width) // 2
        popup_y = (self.settings.screen_height - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        
        # Draw pop-up background
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), popup_rect, 2)
        
        # Render the message text
        text_surface = font.render(message, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()


if __name__ == "__main__":
    #Make a game instance, and run the game
    alien_invasion = Alien_Invasion()
    alien_invasion.run_game()
