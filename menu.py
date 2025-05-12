import pygame
from game import Game

def run_menu():
    game = Game()
    selection = game.run_game_menu()

    if selection == "solo":
        game.run_game()
    elif selection == "multiplayer":
        # Yet to build
        print("Multiplayer menu not implemented yet")
    elif selection == "quit":
        pygame.quit()
        return

# For testing the menu directly
if __name__ == "__main__":
    start_game = run_menu()
    print("Start Game:", start_game)