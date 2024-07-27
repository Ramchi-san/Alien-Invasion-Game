import pygame
from pygame.sprite import Sprite
from PIL import Image

class Alien_Ship(Sprite):
    """A class to represent a single alien ship in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #This capability to manipulate the size of the image gives much more flexibility to the capability of the program
        self._alien_ship_resizer('version-1/images/alien_ship-fin.png', 50, 50)
    
        #Load the alien ship image and set its rect attribute
        self.image = pygame.image.load('version-1/images/resized_alien_ship.png')
        self.rect = self.image.get_rect()

        #Start each new alien ship near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's ship's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien ship is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien ship to right and left"""
        self.x += (self.settings.alien_ship_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def _alien_ship_resizer(self, img_file, width, height):
        with Image.open(img_file) as img:
            # Resize the image
            resized_img = img.resize((width, height))
            # Save the resized image
            resized_img.save('version-1/images/resized_alien_ship.png')



