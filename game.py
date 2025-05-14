import pygame
from background import Background
from player import Player
from world import World

class Game:
    def __init__(self):
       self.SCREEN_WIDTH = 1920
       self.SCREEN_HEIGHT = 1080
       self.clock = 0
       self.FPS = 60
       self.run = True
       pygame.init()
       screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
       self.screen = screen
       pygame.display.set_caption("GAME NAME GOES HERE")
       self.background = Background(screen)
       self.player = Player(screen, 1)
       self.world = World(screen)
       self.score = 0.0
       self.font = pygame.font.SysFont("Arial", 36)
       self.start_time = pygame.time.get_ticks()

    def run_game(self):
        self.clock = pygame.time.Clock()
        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.background.create_parallax(dt)
            self.calculate_score(dt)



            ground_rects = [tile.rect for tile in self.world.ground_sprites]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.player.RIGHT_KEY = True
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.player.RIGHT_KEY = False
                    elif event.key == pygame.K_SPACE:
                        if self.player.is_jumping:
                            self.player.velocity.y *= 0.25
                            self.player.is_jumping = False

            self.player.update(dt, ground_rects)
            self.world.world_run()
            self.player.draw()
            self.draw_score()
            pygame.display.update()
        return None

    def calculate_score(self, dt):
        # Time survived component (10 points/sec)
        time_points = 100 * dt

        # Position component (0-50 points/sec based on right position)
        player_x = self.player.player.x
        screen_width = self.screen.get_width()

        # Ensure player X position stays within screen bounds (0 to screen_width)
        # so we can fairly calculate how far to the right they've progressed
        clamped_x = max(0, min(player_x, screen_width))
        position_ratio = clamped_x / screen_width
        position_points = 100 * position_ratio * dt

        # Update total score
        self.score += time_points + position_points

    def draw_score(self):
        # Create text surface
        score_text = self.font.render(f"SCORE: {int(self.score)}", True, (255, 255, 255))
        text_rect = score_text.get_rect(topright=(self.SCREEN_WIDTH - 20, 20))

        # Create background rectangle
        bg_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)

        # Draw elements
        self.screen.blit(score_text, text_rect)

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
        return None

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
        return None