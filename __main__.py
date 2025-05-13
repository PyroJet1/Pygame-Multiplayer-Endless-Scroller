import pygame
from menu import run_menu
from game import Game

def main() -> None:
    pygame.init()

    should_continue = run_menu()

    if should_continue:
        game = Game()
        game.run_game()

    pygame.quit()

if __name__ == "__main__":
    main()