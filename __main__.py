import pygame
from menu import run_menu
from game import Game

def main() -> None:
    pygame.init()
    should_continue = run_menu()

    if should_continue:
        game = Game()
        result = game.run_game()

        if result == "quit":
            pygame.quit()
            return

    pygame.quit()

if __name__ == "__main__":
    main()