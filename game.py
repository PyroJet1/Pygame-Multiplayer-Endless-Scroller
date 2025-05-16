import pygame, time
from background import Background
from player import Player
from world import World
from network import Network

class Game:
    def __init__(self, num_players = 1, is_multiplayer = False):
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
       self.world = World(screen)
       self.score = 0.0
       self.font = pygame.font.SysFont("Arial", 36)
       self.start_time = pygame.time.get_ticks()
       self.num_players = num_players
       self.players = []

       self.is_multiplayer = is_multiplayer

       if hasattr(self, 'network') and self.network is not None:
           self.network.close()
       if self.is_multiplayer:
           self.network = Network(self)
       else:
           self.network = None



       for i in range(4):
           player = Player(self.screen, i+1, self)
           player.active = (i < num_players)
           self.players.append(player)

    def run_game(self):
        self.background.paused = False
        self.clock = pygame.time.Clock()

        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.background.create_parallax(dt)
            ground_tiles = self.world.ground_sprites

            # Check game over for active players
            if any(p.check_game_over() for p in self.players if p.active):
                if self.handle_game_over():
                    return "quit"
                break

            # Event handling for active players
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return "quit"

                # Player 1 controls (WASD) - Always active if num_players >= 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.players[0].LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.players[0].RIGHT_KEY = True
                    if event.key == pygame.K_w:
                        self.players[0].jump()


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.players[0].LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.players[0].RIGHT_KEY = False





            # Update all players (active and inactive)
            for player in self.players:
                if player.active:
                    player.update(dt, ground_tiles, self.players)
                else:
                    # Keep inactive players in place for collision testing
                    player.player.y = self.screen.get_height() - 105  # Ground level

            self.world.world_run()
            self.draw_score()

            # Draw all players
            for player in self.players:
                if player.active or (self.is_multiplayer and not player.active):
                    player.draw()
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), player.player)

            pygame.display.update()
        return None

    def handle_game_over(self):
        self.background.paused = True
        final_time = (pygame.time.get_ticks() - self.start_time) // 1000
        while True:
            action = self.show_game_over_screen(self.score, final_time)
            if action == "restart":
                self.__init__()  # Reset game state
                self.run_game()
                break
            elif action == "menu":
                self.run = False
                break
            elif action == "quit":
                pygame.quit()
                return True
            return False

    def show_game_over_screen(self, score, time_survived):
        font_large = pygame.font.SysFont("Arial", 72)
        font_medium = pygame.font.SysFont("Arial", 48)

        buttons = [
            {"label": "Play Again", "action": "restart"},
            {"label": "Main Menu", "action": "menu"}
        ]

        # Create button surfaces and rects
        button_rects = []
        for i, btn in enumerate(buttons):
            text = font_medium.render(btn["label"], True, (255, 255, 255))
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, 500 + i * 100))
            btn["rect"] = rect
            btn["surface"] = text

        while True:
            # Darken game background
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            # Display stats
            score_text = font_large.render(f"Final Score: {int(score)}", True, (255, 255, 255))
            time_text = font_medium.render(f"Time Survived: {time_survived}s", True, (255, 255, 255))

            self.screen.blit(score_text, score_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300)))
            self.screen.blit(time_text, time_text.get_rect(center=(self.SCREEN_WIDTH // 2, 380)))

            # Draw buttons
            for btn in buttons:
                bg_rect = btn["rect"].inflate(30, 20)
                pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
                self.screen.blit(btn["surface"], btn["rect"])

            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn["rect"].collidepoint(event.pos):
                            return btn["action"]

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
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            selected_value = button["value"]
                            if selected_value == "back":
                                return None  # Return to main menu
                            elif selected_value in [2, 3, 4]:
                                return selected_value

            pygame.display.update()
        return None

    def update_online_player(self, player_num, x, y):
        index = player_num - 1
        if 0 <= index < len(self.players) and not self.players[index].active:
            self.players[index].player.x = x
            self.players[index].player.y = y

    def show_loading_screen(self):
        font = pygame.font.SysFont("Arial", 48)
        loading_text = font.render("Searching for players...", True, (255, 255, 255))
        text_rect = loading_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
        start_time = time.time()

        while self.run:
            self.background.create_parallax(0.0001)
            self.screen.blit(loading_text, text_rect)
            pygame.display.update()

            if time.time() - start_time > 15:
                print("[NETWORK] Discovery Timeout")

            # Check if peers are found or timeout
            if len(self.network.game_players) > 0:
                print(f"[NETWORK] Found players: {self.network.game_players}")
                return True  # Start game

            # Event handling to prevent freeze
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
            pygame.time.wait(100)
        return None








