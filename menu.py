
from game import Game

def run_menu():
    game = Game()
    return game.run_game_menu()

# For testing the menu directly
if __name__ == "__main__":
    start_game = run_menu()
    print("Start Game:", start_game)