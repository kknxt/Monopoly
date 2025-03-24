from monopoly.player import Player, NotEnoughMoneyException
from monopoly.plane import Card, CHANCES
from monopoly.game import Dice
import pytest


def test_player_constructor():
    jurek = Player("Jurek")
    assert jurek._name == "Jurek"
    assert jurek._cash == 15000000
    assert jurek._cards == []
    assert jurek._position == 1


def test_test_changing_bank_balance():
    jurek = Player("Jurek")
    assert jurek.name() == "Jurek"
    jurek.change_balance(10000000)
    assert jurek.cash() == 5000000
    jurek.earn(1)
    assert jurek.cash() == 5000001


def test_buy_card():
    jurek = Player("Jurek")
    card = Card("Lublin", "grey", 750000, 75000)
    jurek.buy_card(card)
    assert len(jurek._cards) == 1
    assert jurek.cash() == 15000000 - 750000


def test_movement(monkeypatch):
    def move_5():
        return 5
    dice = Dice()
    monkeypatch.setattr(dice, "make_throw", move_5)
    jurek = Player("Jurek")
    jurek.make_move(dice)
    assert jurek.position() == 6
    jurek.make_move(dice)
    assert jurek.position() == 11


def test_position_reset_and_cash_bonus_after_lap(monkeypatch):
    def move_45():
        return 45
    dice = Dice()
    monkeypatch.setattr(dice, "make_throw", move_45)
    jurek = Player("Jurek")
    assert jurek.position() == 1
    assert jurek.cash() == 15000000
    jurek.make_move(dice)
    assert jurek.position() == 6
    assert jurek.cash() == 17000000


def test_is_in_game():
    jurek = Player("Jurek")
    jurek._cash = -1
    assert jurek.is_in_game() is False


def test_exception():
    jurek = Player("Jurek")
    with pytest.raises(NotEnoughMoneyException):
        jurek.change_balance(15000001)


def test_change_balance_chance_card():
    jurek = Player("Jurek")
    jurek.change_balance(CHANCES[5])
    assert jurek.cash() == 15500000


def test_can_build_houses_yes():
    card = Card("Istanbul", "brown", 350000, 35000)
    card2 = Card("Ankara", "brown", 350000, 35000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    jurek.buy_card(card2)
    assert jurek.can_build_houses(card) is True
    assert jurek.can_build_houses(card2) is True


def test_can_build_houses_not_owner():
    card = Card("Istanbul", "brown", 350000, 35000)
    card2 = Card("Ankara", "brown", 350000, 35000)
    jurek = Player("Jurek")
    assert jurek.can_build_houses(card) is False
    assert jurek.can_build_houses(card2) is False


def test_can_build_houses_not_a_property():
    start = Card("Start", card_type="START")
    chance = Card("Chance", card_type="CHANCE")
    tax = Card("Income tax", None, None, 1000000, "TAX")
    transport = Card("Bus Station", "transport", 1000000, 500000)
    jurek = Player("Jurek")
    assert jurek.can_build_houses(start) is False
    assert jurek.can_build_houses(chance) is False
    assert jurek.can_build_houses(tax) is False
    assert jurek.can_build_houses(transport) is False


def test_can_build_houses_hotel_and_4_houses():
    card = Card("Istanbul", "brown", 350000, 35000)
    card2 = Card("Ankara", "brown", 350000, 35000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    jurek.buy_card(card2)
    jurek.build_houses(card, 4)
    jurek.build_hotel(card2)
    assert jurek.can_build_houses(card) is False
    assert jurek.can_build_houses(card2) is False
    assert card2.houses() is None


def test_can_build_hotel_yes():
    card = Card("Gdansk", "grey", 750000, 75000)
    card2 = Card("Lublin", "grey", 750000, 75000)
    card3 = Card("Warsaw", "grey", 1000000, 100000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    jurek.buy_card(card2)
    jurek.buy_card(card3)
    jurek.build_houses(card, 4)
    jurek.build_houses(card2, 4)
    jurek.build_houses(card3, 4)
    assert jurek.can_build_hotel(card) is True
    assert jurek.can_build_hotel(card2) is True
    assert jurek.can_build_hotel(card3) is True


def test_can_build_hotel_not_enough_houses():
    card = Card("Gdansk", "grey", 750000, 75000)
    card2 = Card("Lublin", "grey", 750000, 75000)
    card3 = Card("Warsaw", "grey", 1000000, 100000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    jurek.buy_card(card2)
    jurek.buy_card(card3)
    jurek.build_houses(card, 0)
    jurek.build_houses(card2, 2)
    jurek.build_houses(card3, 3)
    assert jurek.can_build_hotel(card) is False
    assert jurek.can_build_hotel(card2) is False
    assert jurek.can_build_hotel(card3) is False


def test_can_build_hotel_already_hotel():
    card = Card("Gdansk", "grey", 750000, 75000)
    card2 = Card("Lublin", "grey", 750000, 75000)
    card3 = Card("Warsaw", "grey", 1000000, 100000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    jurek.buy_card(card2)
    jurek.buy_card(card3)
    jurek.build_hotel(card)
    jurek.build_hotel(card2)
    jurek.build_hotel(card3)
    assert jurek.can_build_hotel(card) is False
    assert jurek.can_build_hotel(card2) is False
    assert jurek.can_build_hotel(card3) is False


def test_build_houses_and_hotel():
    card = Card("Warsaw", "grey", 1000000, 100000)
    jurek = Player("Jurek")
    jurek.buy_card(card)
    assert card.houses() == 0
    jurek.build_houses(card, 2)
    balance = 15000000 - 2 * card.house_price() - card.price()
    assert jurek.cash() == balance
    assert card.houses() == 2
    jurek.build_houses(card, 1)
    assert card.houses() == 3
    jurek.build_hotel(card)
    assert card.houses() is None
    assert card.hotel() == 1


def test_pay_another_player():
    jurek = Player("Jurek")
    zenek = Player("Zenek")
    jurek.pay_another_player(zenek, 5000000)
    assert jurek.cash() == 10000000
    assert zenek.cash() == 20000000
