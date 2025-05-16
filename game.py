import pygame
import sys
from background import Background
from player import Player
from world import World

class Game:
    def __init__(self, num_players = 1):
       self.player = None
       self.SCREEN_WIDTH = 1920
       self.SCREEN_HEIGHT = 1080
       self.clock = 0
       self.FPS = 60
       self.run = True
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

       for i in range(num_players):  # Only create `num_players` instances
           player = Player(self.screen, i + 1)
           self.players.append(player)

    def run_game(self):
        self.background.paused = False
        self.clock = pygame.time.Clock()

        while self.run:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.background.create_parallax(dt)
            self.calculate_score(dt)
            ground_tiles = self.world.ground_sprites

            # Check game over for active players
            if all(player.check_game_over() for player in self.players):
                if self.handle_game_over():
                    return "quit"

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
                    if event.key == pygame.K_RIGHT:
                        self.players[1].RIGHT_KEY = True
                    elif event.key == pygame.K_LEFT:
                        self.players[1].LEFT_KEY = True
                    if event.key == pygame.K_UP:
                        self.players[1].jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.players[0].LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.players[0].RIGHT_KEY = False
                    if event.key == pygame.K_RIGHT:
                        self.players[1].RIGHT_KEY = False
                    elif event.key == pygame.K_LEFT:
                        self.players[1].LEFT_KEY = False

                # Player 2 controls arrow keys

            # Update existing players only, draw the existing ones only as well
            for player in self.players:
                player.update(dt, ground_tiles, self.players)
                player.draw()

            self.world.world_run()
            self.draw_score()

            pygame.display.update()
        return None

    def handle_game_over(self):
        self.background.paused = True
        stored_players = self.num_players # stores player count
        while True:
            action = self.show_game_over_screen()
            if action == "restart":
                self.__init__(num_players=stored_players)  # Reset game state
                self.run_game()
                break
            elif action == "menu":
                self.run = False
                break
            elif action == "quit":
                return True
            return False

    def show_game_over_screen(self):
        # Initialize fonts
        font_large = pygame.font.SysFont("Arial", 72)
        font_medium = pygame.font.SysFont("Arial", 48)

        # Calculate winner
        winner = max(self.players, key=lambda player: player.score)

        buttons = [
            {"label": "Play Again", "action": "restart"},
            {"label": "Main Menu", "action": "menu"}
        ]

        # Create button surfaces
        for i, btn in enumerate(buttons):
            text = font_medium.render(btn["label"], True, (255, 255, 255))
            rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, 800 + i * 100))
            btn["surface"] = text
            btn["rect"] = rect

        while True:
            # Dark overlay
            overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            # Winner text
            winner_text = font_large.render(f"PLAYER {self.players.index(winner) + 1} WINS!", True, winner.color)
            self.screen.blit(winner_text, winner_text.get_rect(center=(self.SCREEN_WIDTH // 2, 300)))

            # Player scores
            y_pos = 400
            for i, player in enumerate(self.players):
                score_text = font_medium.render(
                    f"Player {i + 1}: {int(player.score)}",
                    True,
                    player.color if player.check_game_over() else (150, 150, 150)  # Gray out dead players
                )
                self.screen.blit(score_text, score_text.get_rect(center=(self.SCREEN_WIDTH // 2, y_pos)))
                y_pos += 100

            # Draw buttons
            for btn in buttons:
                bg_rect = btn["rect"].inflate(30, 20)
                pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
                self.screen.blit(btn["surface"], btn["rect"])

            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn["rect"].collidepoint(event.pos):
                            return btn["action"]

    def calculate_score(self, dt):
        for player in self.players:
            if not player.check_game_over():
                time_points = 100 * dt

                player_x = player.player.x
                screen_width = self.screen.get_width()

                clamped_x = max(0, min(player_x, screen_width))
                position_ratio = clamped_x / screen_width
                position_points = 100 * position_ratio * dt

                # Update total score
                player.score += time_points + position_points

    def draw_score(self):
        y_offset = 20  # Start position from top
        for i, player in enumerate(self.players):
            # Create text with white color
            score_text = self.font.render(f"P{i + 1}: {int(player.score)}", True, (255, 255, 255))
            text_rect = score_text.get_rect(topright=(self.SCREEN_WIDTH - 20, y_offset))
            bg_rect = text_rect.inflate(20, 10)  # Add padding around text

            # Draw background with player's specific color (from your array) with 150 alpha
            box_color = (*player.colors[i], 150)  # RGBA format
            pygame.draw.rect(self.screen, box_color, bg_rect)

            # Draw white text on top
            self.screen.blit(score_text, text_rect)

            y_offset += 60  # Space between score boxes

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
            pygame.event.pump()
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
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check buttons immediately on click
                    pos = pygame.mouse.get_pos()
                    for button in buttons:
                        if button["rect"].collidepoint(pos):
                            return button["action"]
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return "quit"

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
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            selected_value = button["value"]
                            if selected_value == "back":
                                return None  # Return to main menu
                            elif selected_value in [2, 3, 4]:
                                # Start game with selected player count
                                multiplayer_game = Game(num_players=selected_value)
                                result = multiplayer_game.run_game()
                                # If game returns "quit", propagate it
                                if result == "quit":
                                    return "quit"
                                # Otherwise show multiplayer menu again
                                break  # Breaks out of button loop, stays in menu loop

            pygame.display.update()
        return None