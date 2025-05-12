import pygame
from background import Background
from player import Player

class Game:
    def __init__(self):
       self.SCREEN_WIDTH = 1920
       self.SCREEN_HEIGHT = 1080
       self.clock = pygame.time.Clock()
       self.FPS = 60
       self.run = True
       pygame.init()
       screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
       self.screen = screen
       pygame.display.set_caption("LAST STAND")
       self.background = Background(screen)
       self.player = Player(screen)

    def run_game(self):

        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.background.create_parallax(dt)
            self.player.movement()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            pygame.display.update()

    def run_game_menu(self):
        font = pygame.font.SysFont("Arial", 72)
        button_text = font.render("START GAME", True, (255, 255, 255))
        button_rect = button_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))

        while self.run:
            dt = 0.0001
            self.background.create_parallax(dt)

            delta_time = 0.001
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 128 = 35% opacity

            self.screen.blit(overlay, (0, 0))

            # Draw button background and text
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect.inflate(40, 20))  # button background
            self.screen.blit(button_text, button_rect)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Will later quit program
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True  # Signal to start game

            pygame.display.update()

        return None












