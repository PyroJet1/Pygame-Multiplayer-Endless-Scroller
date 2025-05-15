import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, world):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 0.0
        self.world = world

    def update(self, *args):
        self.rect.x -= self.world.GROUND_SPEED
        self.speed = self.world.GROUND_SPEED
        if self.rect.right < 0:
            self.kill()






    
