import pygame

class Player:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.Rect((300, 250, 50, 50))

    def movement(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.player)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move_ip(-20, 0)
        elif keys[pygame.K_d]:
            self.player.move_ip(20, 0)
        elif keys[pygame.K_w]:
            self.player.move_ip(0, -20)
        elif keys[pygame.K_s]:
            self.player.move_ip(0, 20)
