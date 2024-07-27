class Settings:
    """A class to store all the settings for Alien Invasion"""

    def __init__ (self):
        """Initialize the game's settings"""

        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)

        #ship's settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #alien ship's settings
        self.alien_ship_speed = 1.0
        self.fleet_drop_speed = 10
        #fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1 

        #Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

