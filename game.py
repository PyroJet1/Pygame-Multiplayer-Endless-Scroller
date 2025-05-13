import pygame
from background import Background
from player import Player
from world import World

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
       pygame.display.set_caption("GAME NAME GOES HERE")
       self.background = Background(screen)
       self.player = Player(screen, 1)
       self.world = World(screen)

    def run_game(self):
        self.run = True
        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.background.create_parallax(dt)

            # Define ground with gaps
            # ground_segments = [
            #     pygame.Rect(0, self.SCREEN_HEIGHT - 40, 400, 40),
            #     pygame.Rect(500, self.SCREEN_HEIGHT - 40, 300, 40),
            #     pygame.Rect(900, self.SCREEN_HEIGHT - 40, 400, 40),
            # ]
            #
            #
            # # Draw ground segments
            # for segment in ground_segments:
            #     pygame.draw.rect(self.screen, (100, 70, 30), segment)
            # self.player.movement(ground_segments)

            ground_rects = [tile.rect for tile in self.world.ground_sprites]
            self.player.movement(ground_rects)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return "quit"

            self.world.world_run()

            pygame.display.update()

    def run_game_menu(self):
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 48)

        buttons = [
            {"label": "START GAME", "action": "solo"},
            {"label": "MULTIPLAYER", "action": "multiplayer"},
            {"label": "QUIT", "action": "quit"}
        ]

        button_rects = []
        for i, button in enumerate(buttons):
            text_surf = font.render(button["label"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.SCREEN_WIDTH // 2, 400 + i * 100))
            button["surface"] = text_surf
            button["rect"] = text_rect
            button_rects.append(button)

        while self.run:
            self.background.create_parallax(0.0001)

            # Slight dark overlay
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))  # Very light darkness
            self.screen.blit(overlay, (0, 0))

            # Draw translucent buttons with text
            for button in buttons:
                rect = button["rect"]
                bg = pygame.Surface(rect.inflate(30, 20).size, pygame.SRCALPHA)
                bg.fill((0, 0, 0, 150))  # Translucent black
                self.screen.blit(bg, rect.inflate(30, 20).topleft)
                self.screen.blit(button["surface"], rect)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            return button["action"]

            pygame.display.update()

    def run_multiplayer_menu(self):
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 48)

        buttons = [
            {"label": "2 PLAYERS", "value": 2},
            {"label": "3 PLAYERS", "value": 3},
            {"label": "4 PLAYERS", "value": 4},
            {"label": "BACK TO MAIN MENU", "value": "back"},
        ]

        for i, button in enumerate(buttons):
            text_surf = font.render(button["label"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.SCREEN_WIDTH // 2, 400 + i * 100))
            button["surface"] = text_surf
            button["rect"] = text_rect

        while self.run:
            self.background.create_parallax(0.0001)

            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))
            self.screen.blit(overlay, (0, 0))

            for button in buttons:
                rect = button["rect"]
                bg = pygame.Surface(rect.inflate(30, 20).size, pygame.SRCALPHA)
                bg.fill((0, 0, 0, 150))
                self.screen.blit(bg, rect.inflate(30, 20).topleft)
                self.screen.blit(button["surface"], rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            if button["value"] == "back":
                                return None  # go back to main menu
                            return button["value"]

            pygame.display.update()