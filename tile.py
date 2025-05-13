import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    
