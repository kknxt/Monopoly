from monopoly.game import Game
from monopoly.display import Display
from monopoly.input import Input


def test_constructor():
    display = Display()
    game = Game(display)
    assert game._display == display
    assert game._players_count == 0
    assert game._players == []
    assert game._losers == []
    assert game._current_round == 0
    assert game._end_requested is False


def test_init_game_and_players(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    assert game._players_count == 4
    assert len(game._players) == 4


def test_init_players(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    assert game._players[0].name() == "Player 1"
    assert game._players[1].name() == "Player 2"
    assert game._players[2].name() == "Player 3"
    assert game._players[3].name() == "Player 4"


def test_is_game_over(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    game._players[0].earn(-200000000)
    game._players[1].earn(-200000000)
    game._players[2].earn(-200000000)
    assert game.is_game_over() is True


def test_is_game_over_not(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    assert game.is_game_over() is False


def test_find_winners(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    game._players[0].earn(-200000000)
    game._players[1].earn(-200000000)
    game._players[2].earn(-200000000)
    assert len(game.find_winners()) == 1
    assert game.find_winners()[0] == game._players[3]


def test_find_winners_4(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    assert len(game.find_winners()) == 4


def test_find_winners_0(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    game._players[0].earn(-200000000)
    game._players[1].earn(-200000000)
    game._players[2].earn(-200000000)
    game._players[3].earn(-200000000)
    assert len(game.find_winners()) == 0


def test_field_list(monkeypatch):
    def players_4():
        return 4
    disp = Display()
    input = Input()
    game = Game(disp)
    game._input = input
    monkeypatch.setattr(input, "ask_for_number_of_players", players_4)
    game.init_game()
    assert len(game.field_list()) == 40