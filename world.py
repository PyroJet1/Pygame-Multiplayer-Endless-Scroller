import pygame, csv, os, random
from tile import Tile

class World:
    def __init__(self, screen):
        self.screen = screen

        self.Grass = pygame.image.load("jungle-tileset/Grass1.png").convert_alpha()
        self.Grass2 = pygame.image.load("jungle-tileset/grass2.png").convert_alpha()
        self.Grass3 = pygame.image.load("jungle-tileset/Grass3.png").convert_alpha()
        self.Mud = pygame.image.load("jungle-tileset/mud.png").convert_alpha()
        self.Right_mud = pygame.image.load("jungle-tileset/rightmud.png").convert_alpha()
        self.Left_mud = pygame.image.load("jungle-tileset/mudleft.png").convert_alpha()
        self.Plainmud = pygame.image.load("jungle-tileset/plainmud.png").convert_alpha()
        self.Deep = pygame.image.load("jungle-tileset/deepmud.png").convert_alpha()
        self.Left_corner = pygame.image.load("jungle-tileset/leftcorner.png").convert_alpha()
        self.Left_wall = pygame.image.load("jungle-tileset/leftwall.png").convert_alpha()
        self.Right_corner = pygame.image.load("jungle-tileset/rightcorner.png").convert_alpha()
        self.Right_wall = pygame.image.load("jungle-tileset/rightwall.png").convert_alpha()
        self.flipleft = pygame.image.load("jungle-tileset/90leftflip.png").convert_alpha()
        self.flipright = pygame.image.load("jungle-tileset/90rightflip.png").convert_alpha()
        self.left90 = pygame.image.load("jungle-tileset/90left.png").convert_alpha()
        self.right90 = pygame.image.load("jungle-tileset/90right.png").convert_alpha()
        self.grassblock = pygame.image.load("jungle-tileset/Grassblock.png").convert_alpha()


        self.screen_width = self.screen.get_width()

        self.tile_size = 64
        self.ground_sprites = pygame.sprite.Group()
        self.spawn_x = 0
        self.GROUND_SPEED = 5
        self.start = 0
        self.start_x = 0
        self.start_y = 0

        self.maps = []

        for path in os.listdir("maps"):
            self.maps.append(os.path.join("maps", path))

        print(len(self.maps))

        self.load_tiles("starting_map.csv", self.GROUND_SPEED, 0)
        self.load_tiles(self.maps[random.randint(0,(len(self.maps) - 1))], self.GROUND_SPEED, 1)


    def spawn_ground(self, column_group, spawn_x, speed, screen_height, filename):

        #vertical positions: top of grass layer
        deep_y = screen_height - self.tile_size
        mud_y = deep_y - self.tile_size
        grass_y = mud_y - self.tile_size

        # create one tile of each type at (spawn_x, y)
        column_group.add(Tile(self.Grass, spawn_x, grass_y, speed))
        column_group.add(Tile(self.Mud, spawn_x, mud_y, speed))
        column_group.add(Tile(self.Deep, spawn_x, deep_y, speed))

        # advance spawn_x
        return spawn_x + self.tile_size

    def load_tiles(self, filename, speed, spawn_after):
        map_data = self.read_csv(filename)
        if spawn_after:
            offset = self.screen_width - 8
        else:
            offset = 0
        x, y = 0, 0
        for row in map_data:
            x = 0
            for tile in row:
                if tile == '0':
                    self.ground_sprites.add(Tile(self.Plainmud, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '1':
                    self.ground_sprites.add(Tile(self.Grass2, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '2':
                    self.ground_sprites.add(Tile(self.Grass, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '3':
                    self.ground_sprites.add(Tile(self.Grass3, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '4':
                    self.ground_sprites.add(Tile(self.Left_corner, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '5':
                    self.ground_sprites.add(Tile(self.Left_wall,(x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '6':
                    self.ground_sprites.add(Tile(self.Deep, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '7':
                    self.ground_sprites.add(Tile(self.Mud, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '8':
                    self.ground_sprites.add(Tile(self.Left_mud, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '9':
                    self.ground_sprites.add(Tile(self.Right_wall, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '10':
                    self.ground_sprites.add(Tile(self.Right_mud, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '11':
                    self.ground_sprites.add(Tile(self.Right_corner, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '12':
                    self.ground_sprites.add(Tile(self.flipleft, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '13':
                    self.ground_sprites.add(Tile(self.flipright, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '14':
                    self.ground_sprites.add(Tile(self.left90, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '15':
                    self.ground_sprites.add(Tile(self.right90, (x * self.tile_size) + offset, y * self.tile_size, speed))
                elif tile == '16':
                    self.ground_sprites.add(Tile(self.grassblock, (x * self.tile_size) + offset, y * self.tile_size, speed))

                x += 1
            y += 1
        return map_data

    def world_run(self):

        self.start += self.GROUND_SPEED
        if self.start % self.screen_width == 0:
            self.load_tiles(self.maps[random.randint(0,(len(self.maps) - 1))], self.GROUND_SPEED, 1)


        self.ground_sprites.update()
        self.ground_sprites.draw(self.screen)


    def read_csv(self, filename):
        map=[]
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
            return map






