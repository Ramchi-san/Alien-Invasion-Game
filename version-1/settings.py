class Settings:
    """A class to store all the settings for Alien Invasion"""

    def __init__ (self):
        """Initialize the game's settings"""

        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        #ship's settings
        self.ship_limit = 3

        #Bullet settings
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        #Speed-up scale
        self.speed_up_scale = 1.1

        #Scoring
        self.alien_ship_points = 10
        self.increasing_score_scale = 1.5      

          

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.alien_ship_speed = 1.0
        self.bullet_speed = 3
        #alien ship's settings
        self.fleet_drop_speed = 5

        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increases speed mechanics and scoring scale"""
        self.ship_speed *= 1.2
        self.alien_ship_speed *= 1.5
        self.bullet_speed *= 1.2
        self.alien_ship_points = int(self.alien_ship_points * self.increasing_score_scale)
    
    
        

