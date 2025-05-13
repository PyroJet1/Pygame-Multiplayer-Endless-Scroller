import pygame
from spritesheet import Spritesheet

class Player:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = pygame.Rect(0, self.screen.get_height() - 105, 63, 105)

        # Load and process sprite sheet
        self.sprite_sheet = pygame.image.load(f'sprites/charachter_animations_sprite_p{player}.png') #21x33
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
        self.gravity = 1.0
        self.jump_strength = -20
        self.velocity_y = 0
        self.is_jumping = False
        self.ground_y = self.screen.get_height() - self.player.height

    def movement(self, ground_segments):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_a]:
            self.player.x -= self.speed
        elif keys[pygame.K_d]:
            self.player.x += self.speed

        # Jump if on the ground
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_strength
            self.is_jumping = True

        # Apply gravity
        self.velocity_y += self.gravity
        self.player.y += self.velocity_y

        # Check for collision with ground segments
        on_ground = False
        for segment in ground_segments:
            if self.player.colliderect(segment) and self.velocity_y >= 0:
                self.player.bottom = segment.top
                self.velocity_y = 0
                self.is_jumping = False
                on_ground = True
                break

        if not on_ground:
            self.is_jumping = True

        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated > self.animation_cooldown:
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            self.last_updated = current_time

        # Draw the animated sprite at the player's current position
        image = self.animation_list[self.action][self.frame]
        self.screen.blit(image, self.player.topleft)