import pygame

class Background:
    def __init__(self, screen):
        screen_size = pygame.display.get_window_size()
        self.SCREEN_WIDTH = screen_size[0]
        self.SCREEN_HEIGHT = screen_size[1]
        self.screen = screen
        bg1 = pygame.image.load("images/plx-1.png").convert_alpha()
        bg1 = pygame.transform.scale(bg1, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        bg2 = pygame.image.load("images/plx-2.png").convert_alpha()
        bg2 = pygame.transform.scale(bg2, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        bg3 = pygame.image.load("images/plx-3.png").convert_alpha()
        bg3 = pygame.transform.scale(bg3, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        bg4 = pygame.image.load("images/plx-4.png").convert_alpha()
        bg4 = pygame.transform.scale(bg4, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        bg5 = pygame.image.load("images/plx-5.png").convert_alpha()
        bg5 = pygame.transform.scale(bg5, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.scroll_speed = [0.0, 0.25, 0.5, 0.75, 1.0]
        self.scroll = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.accel = 0.025
        self.bg = [bg1, bg2, bg3, bg4, bg5]

    def create_parallax(self, dt):
        # speed-up each layer by accel% per second
        for i in (1, 2, 3, 4):
            if self.scroll_speed[4] >= 15:
                self.scroll_speed[4] = 15
            elif self.scroll_speed[3] >= 13:
                self.scroll_speed[3] = 13
            elif self.scroll_speed[2] >= 10:
                self.scroll_speed[2] = 10
            elif self.scroll_speed[1] >= 9:
                self.scroll_speed[1] = 9
            else:
                self.scroll_speed[i] *= (1 + self.accel * dt)



        # draw backmost layer
        self.screen.blit(self.bg[0], (0, 0))

        # draw each scrolling layer in turn
        for i in range(0, 2):
            self.screen.blit(self.bg[1], (i * self.SCREEN_WIDTH + self.scroll[1], 0))
        for i in range(0, 2):
            self.screen.blit(self.bg[2], (i * self.SCREEN_WIDTH + self.scroll[2], 0))
        for i in range(0, 2):
            self.screen.blit(self.bg[3], (i * self.SCREEN_WIDTH + self.scroll[3], 0))
        for i in range(0, 2):
            self.screen.blit(self.bg[4], (i * self.SCREEN_WIDTH + self.scroll[4], 0))

        # move each layer by its (now-increasing) speed
        self.scroll[1] -= self.scroll_speed[1]
        self.scroll[2] -= self.scroll_speed[2]
        self.scroll[3] -= self.scroll_speed[3]
        self.scroll[4] -= self.scroll_speed[4]

        # wrap offsets
        for i in (1, 2, 3, 4):
            if abs(self.scroll[i]) > self.SCREEN_WIDTH:
                self.scroll[i] = 0

