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

        elif selection == "quit" or selection is None:
            return False  # Tell main not to start game