import pygame
from spritesheet import Spritesheet

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.Rect((300, 250, 50, 50))
        self.sprite_sheet = pygame.image.load('sprites/charachter_animations_sprite.png') #21x33
        self.sheet = Spritesheet(self.sprite_sheet)

        #animation list
        self.animation_steps = [8,1,2,1]
        self.animation_list = []
        self.last_updated = pygame.time.get_ticks()
        self.animation_cooldown = 100 #milliseconds
        self.frame = 0
        self.step_counter = 0
        self.action = 0

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.sheet.get_image(self.step_counter, 21, 35, 3))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)


    def movement(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.player)

        #update animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_updated > self.animation_cooldown:
            self.frame += 1
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

            self.last_updated = current_time


        self.screen.blit(self.animation_list[self.action][self.frame], (0,0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move_ip(-20, 0)
        elif keys[pygame.K_d]:
            self.player.move_ip(20, 0)
        elif keys[pygame.K_w]:
            self.player.move_ip(0, -20)
        elif keys[pygame.K_s]:
            self.player.move_ip(0, 20)


