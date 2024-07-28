import json
import pygame.font
import os
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """A class to report all the scoring mechanics of the game"""
    def __init__(self, ai_game):
        """Initializes scoring attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.game_stats = ai_game.game_stats

        #Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    
    def prep_score(self):
        """"Turn the score into a rendered image"""
        rounded_score = round(self.game_stats.game_score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                    self.settings.bg_color)
        
        #Display the score at the top-right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 
    
    def show_score(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.game_stats.high_score, -1)    
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                        self.text_color, self.settings.bg_color)

        #Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top            
    
    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.game_stats.game_score > self.game_stats.high_score:
            self.game_stats.high_score = self.game_stats.game_score
            self.prep_high_score()
    
    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.game_stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                    self.settings.bg_color)
        
        #Position the level below below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.game_stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

        

    # Function to save user information to a JSON file
    def save_to_json(self, high_score, filename='version-1/high_score_data.json'):
        with open(filename, 'w') as json_file:
            json.dump(high_score, json_file, indent=4)
    
    # Function to check if a file is empty
    def is_file_empty(self, filename='version-1/high_score_data.json'):
        return os.path.exists(filename) and os.path.getsize(filename) == 0
        
    def read_json(self, filename='version-1/high_score_data.json'):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data