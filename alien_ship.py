import pygame
from pygame.sprite import Sprite
from PIL import Image

class Alien_Ship(Sprite):
    """A class to represent a single alien ship in the fleet"""

    def __init__(self, ai_game):
        """Initialize the alien ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self._alien_ship_resizer('images/alien_ship-fin.png', 100, 100)
    
        #Load the alien ship image and set its rect attribute
        self.image = pygame.image.load('images/resized_alien_ship.png')
        self.rect = self.image.get_rect()

        #Start each new alien ship near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's ship's exact horizontal position.
        self.x = float(self.rect.x)

    def _alien_ship_resizer(self, img_file, width, height):
        with Image.open(img_file) as img:
            # Resize the image
            resized_img = img.resize((width, height))
            # Save the resized image
            resized_img.save('images/resized_alien_ship.png')



