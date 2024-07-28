import json

class Game_Stats:
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings

        #start alien invasion in an active state
        self.game_active = False
        
        #High score should never be reset
        self.high_score = 0
        self.level = 1

        self.reset_stats()

        
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.game_score = 0
    
    
        

