from monopoly.display import Display
from monopoly.game import Game

if __name__ == '__main__':
    display = Display()
    game = Game(display)
    game.init_game()
    game.play_game()
