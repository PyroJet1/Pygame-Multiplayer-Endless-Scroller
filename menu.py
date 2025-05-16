import pygame
from game import Game

def run_menu():
    game = Game()

    while True:
        game = Game()
        selection = game.run_game_menu()

        if selection == "solo":
            result = game.run_game()
            if result == "quit":
                return False

        elif selection == "multiplayer":
            num_players = game.run_multiplayer_menu()  # Handle menu in multiplayer context
            if num_players in [2, 3, 4]:
                game.__init__(num_players=num_players, is_multiplayer=True)
                game.network.broadcast(timeout=10)
                if game.show_loading_screen():
                    game.run_game()

        elif selection == "quit" or selection is None:
            return False  # Tell main not to start game

        # If no quit, the loop continues and shows menu again