import pygame
from menu import run_menu
from game import Game

def main() -> None:

    game = Game()
    game.run_game()

    pygame.quit()

if __name__ == "__main__":
    if run_menu():
        main()
