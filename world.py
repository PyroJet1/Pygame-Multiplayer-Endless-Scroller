import pygame
from tile import Tile

class World:
    def __init__(self, screen):
        self.screen = screen
        grass = pygame.image.load("jungle-tileset/Grass1.png").convert_alpha()
        self.Grass = pygame.transform.scale(grass, (64,64))
        mud = pygame.image.load("jungle-tileset/mud.png").convert_alpha()
        self.Mud = pygame.transform.scale(mud,(64,64))
        deep= pygame.image.load("jungle-tileset/deepmud.png").convert_alpha()
        self.Deep = pygame.transform.scale(deep,(64,64))
        self.TILE_W, self.TILE_H = self.Grass.get_size()
        self.ground_sprites = pygame.sprite.Group()
        self.spawn_x = 0
        self.GROUND_SPEED = 5



    def spawn_ground(self, column_group, spawn_x, speed, screen_height):
        # vertical positions: top of grass layer
        deep_y = screen_height - self.TILE_H
        mud_y = deep_y - self.TILE_H
        grass_y = mud_y - self.TILE_H

        # create one tile of each type at (spawn_x, y)
        column_group.add(Tile(self.Grass, spawn_x, grass_y, speed))
        column_group.add(Tile(self.Mud, spawn_x, mud_y, speed))
        column_group.add(Tile(self.Deep, spawn_x, deep_y, speed))

        # advance spawn_x
        return spawn_x + self.TILE_W

    def world_run(self):
        self.ground_sprites.update()

        rightmost_x = 0
        for tile in self.ground_sprites:
            if tile.rect.right > rightmost_x:
                rightmost_x = tile.rect.right


        while self.spawn_x < self.screen.get_width() + self.TILE_W:
            self.spawn_x = self.spawn_ground(self.ground_sprites, self.spawn_x, self.GROUND_SPEED, self.screen.get_height())

        self.ground_sprites.draw(self.screen)



