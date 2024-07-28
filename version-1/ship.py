import pygame
from PIL import Image
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        
        #Load the ship image and get its rect.
        new_img_file = 'version-1/images/resized_ship.png'
        self._ship_resizer('version-1/images/ship.png', 100, 100, new_img_file)
        self.image = pygame.image.load(new_img_file)
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        #Movement flag
        self.moving_right = False
        self.moving_left = False
    
    def _ship_resizer(self, img_file, width, height, new_img_file):
        with Image.open(img_file) as img:
            
            # Resize the image
            resized_img = img.resize((width, height))
            resized_img.save(new_img_file)

    def center_ship(self):
        #Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Update the ship's position based on the movement flag"""
        #Update the ship's x-value instead of rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        #Update the rect value from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
