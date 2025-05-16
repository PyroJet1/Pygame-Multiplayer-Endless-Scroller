import pygame
from game import Game

def run_menu():
    game = Game()

    while True:
        selection = game.run_game_menu()

        if selection == "solo":
            result = game.run_game()
            if result == "quit":
                return False

        elif selection == "multiplayer":
            num_players = game.run_multiplayer_menu()
            if num_players == "quit":
                return False

            elif num_players in [2, 3, 4]:
                print(f"Multiplayer selected with {num_players} players")
                # Multiplayer logic here

        elif selection == "quit" or selection is None:
            return False  # Tell main not to start game