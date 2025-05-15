import pygame
from spritesheet import Spritesheet

class Player:
    def __init__(self, screen, player_num):
        self.screen = screen
        self.active = False
        x_position = 200 + (player_num * 150)  # Space players horizontally
        self.player = pygame.Rect(x_position, screen.get_height() - 105, 63, 105)
        self.player = pygame.Rect(200 - (20 * player_num), self.screen.get_height() - 105, 63, 105)

        # Load and process sprite sheet
        self.sprite_sheet = pygame.image.load(f'sprites/character_animations_sprite_p{player_num}.png')
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
        self.game_over = False
        self.on_player = False
        self.boost_multiplier = 1.5

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sheet.get_image(self.step_counter, 21, 35, 3))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)

        # Movement and physics
        self.speed = 5
        self.gravity, self.friction = 2400, -15
        self.jump_strength = -1100
        self.velocity_y = 0
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.is_jumping, self.on_ground = False, False
        self.position, self.velocity = pygame.math.Vector2(self.player.topleft), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)
        self.ground_y = self.screen.get_height() - self.player.height

    def update(self, dt, tiles, players=None):
        self.horizontal_movement(dt)
        self.check_collisionsx(tiles, players)
        self.vertical_movement(dt)
        self.check_collisionsy(tiles, players)
        self.check_game_over()

        # Collision with other players (active and inactive)
        if players:
            for other in players:
                if other is not self and self.player.colliderect(other.player):
                    self.handle_player_collision(other)

    def handle_player_collision(self, other):
        # Simple collision resolution
        if self.velocity.x > other.velocity.x:
            self.position.x -= 5
            other.position.x += 5
        else:
            self.position.x += 5
            other.position.x -= 5

        # Update rect positions
        self.player.x = int(self.position.x)
        other.player.x = int(other.position.x)

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

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 7500
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
            self.on_player = False

    def get_hits(self, tiles):
        return [tile for tile in tiles if self.player.colliderect(tile.rect)]


    def check_collisionsx(self, tiles, players=None):
        collisions = self.get_hits(tiles)
        for tile in collisions:

            # Calculate overlap direction
            overlap_left = self.player.right - tile.rect.left
            overlap_right = tile.rect.right - self.player.left

            # Push player in the direction of smallest overlap
            if abs(overlap_left) < abs(overlap_right):
                self.position.x = tile.rect.left - self.player.width
            else:
                self.position.x = tile.rect.right

            # Update position and halt horizontal velocity
            self.player.x = int(self.position.x)
            self.velocity.x = 0

    def check_collisionsy(self, tiles, players=None):
        self.on_ground = False
        self.on_player = False
        self.player.bottom += 1  # Small overlap to detect ground
        collisions = self.get_hits(tiles)
        for tile in collisions:
            # Resolve vertical collision regardless of tile speed
            if self.velocity.y > 0:  # Falling down
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top  # Use tile.rect
                self.player.bottom = int(self.position.y)
            elif self.velocity.y < 0:  # Jumping up
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.player.height
                self.player.bottom = int(self.position.y)
        self.player.bottom -= 1  # Reset overlap check

    def check_game_over(self):
        if self.player.top > self.screen.get_height() or self.player.right < 0:
            self.game_over = True
        return self.game_over