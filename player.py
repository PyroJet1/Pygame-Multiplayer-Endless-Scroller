import pygame
from spritesheet import Spritesheet

class Player:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = pygame.Rect(0, self.screen.get_height() - 105, 63, 105)

        # Load and process sprite sheet
        self.sprite_sheet = pygame.image.load(f'sprites/character_animations_sprite_p{player}.png')
        self.sheet = Spritesheet(self.sprite_sheet)
        self.animation_steps = [8,1,2,1]
        self.animation_list = []
        self.last_updated = pygame.time.get_ticks()
        self.animation_cooldown = 100 #milliseconds
        self.frame = 0
        self.step_counter = 0
        self.action = 0
        self.animation_cooldown = 100
        self.last_updated = pygame.time.get_ticks()

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sheet.get_image(self.step_counter, 21, 35, 3))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)

        # Movement and physics
        self.speed = 5
        self.gravity, self.friction = 2000, -15
        self.jump_strength = -1000
        self.velocity_y = 0
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.is_jumping, self.on_ground = False, False
        self.position, self.velocity = pygame.math.Vector2(self.player.topleft), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.ground_y = self.screen.get_height() - self.player.height

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.check_collisionsx(tiles)
        self.vertical_movement(dt)
        self.check_collisionsy(tiles)

    def draw(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated > self.animation_cooldown:
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            self.last_updated = current_time

        # Draw the animated sprite at the player's current position
        image = self.animation_list[self.action][self.frame]
        self.screen.blit(image, self.player.topleft)
        pygame.draw.rect(self.screen, (255, 255, 255), self.player, 2)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 3000
        elif self.RIGHT_KEY:
            self.acceleration.x += 3000
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(600)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.player.x = int(self.position.x)

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.1: self.velocity.x = 0

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)


        self.player.bottom = self.position.y

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y = self.jump_strength
            self.on_ground = False


    # def movement(self, ground_segments):
        # keys = pygame.key.get_pressed()
        #
        # # Horizontal movement
        # if keys[pygame.K_a]:
        #     self.player
        # elif keys[pygame.K_d]:
        #     self.player.x += self.speed
        #
        # # Jump if on the ground
        # if keys[pygame.K_SPACE] and not self.is_jumping:
        #     self.velocity_y = self.jump_strength
        #     self.is_jumping = True
        #
        # # Apply gravity
        # self.velocity_y += self.gravity
        # self.player.y += self.velocity_y
        #
        # # Check for collision with ground segments
        # on_ground = False
        # for segment in ground_segments:
        #     if self.player.colliderect(segment) and self.velocity_y >= 0:
        #         self.player.bottom = segment.top
        #         self.velocity_y = 0
        #         self.is_jumping = False
        #         on_ground = True
        #         break
        #
        # # if not on_ground:
        #     self.is_jumping = True

        # Update animation frame


    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.player.colliderect(tile):
                hits.append(tile)
        return hits

    def check_collisionsx(self, tile):
        collisions = self.get_hits(tile)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.player.w
                self.player.x = int(self.position.x)
            elif self.velocity.x < 0:
                self.position.x = tile.right
                self.player.x = int(self.position.x)


    def check_collisionsy(self, tile):
        self.on_ground = False
        self.player.bottom += 1
        collision = self.get_hits(tile)
        for tile in collision:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.top
                self.player.bottom = int(self.position.y)
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.bottom + self.player.h
                self.player.bottom = int(self.position.y)