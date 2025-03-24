from monopoly.plane import Card, Plane, CARDS


def test_card_constructor():
    lublin = Card("Lublin", "grey", 750000, 75000)
    assert lublin._name == "Lublin"
    assert lublin._type == "FIELD"
    assert lublin._price == 750000
    assert lublin._color == "grey"
    assert lublin._fee == 75000
    assert lublin._houses == 0
    assert lublin._owner is None
    assert lublin._house_price == 375000
    assert lublin._hotel is None


def test_card_constructor_chance_with_getters():
    chance = Card("Chance", card_type="CHANCE")
    assert chance.name() == "Chance"
    assert chance.type() == "CHANCE"
    assert chance.price() is None
    assert chance.color() is None
    assert chance.fee() == 0
    assert chance.houses() == 0
    assert chance.owner() is None
    assert chance.house_price() is None
    assert chance.hotel() is None


def test_card_constructor_tax():
    tax = Card("Revenue tax", None, None, 1500000, "TAX")
    assert tax.name() == "Revenue tax"
    assert tax.type() == "TAX"
    assert tax.price() is None
    assert tax.color() is None
    assert tax.fee() == 1500000
    assert tax.houses() == 0
    assert tax.owner() is None
    assert tax.house_price() is None
    assert tax.hotel() is None


def test_possible_num_houses():
    warsaw = Card("Warsaw", "grey", 1000000, 100000)
    assert warsaw.possible_num_houses() == 4
    warsaw.set_houses(1)
    assert warsaw.houses() == 1
    assert warsaw.possible_num_houses() == 3
    warsaw.set_houses(4)
    assert warsaw.houses() == 4
    assert warsaw.possible_num_houses() == 0


def test_fee_houses_and_hotels():
    card = Card("Phoenix", "red", 1750000, 175000)
    assert card.fee() == 175000
    card.add_houses(1)
    assert card.fee() == 875000
    card.add_houses(1)
    assert card.fee() == 2625000
    card.add_houses(1)
    assert card.fee() == 5250000
    card.add_houses(1)
    assert card.fee() == 7000000
    card.set_houses(None)
    card.set_hotel()
    assert card.hotel() == 1
    assert card.fee() == 8750000


def test_ownership():
    jurek = "Jurek Ogorek"
    card = Card("Phoenix", "red", 1750000, 175000)
    assert card.owner() is None
    card.set_owner(jurek)
    assert card.owner() == jurek


def test_if_plane_length_40():
    assert len(CARDS) == 40


def test_plane_field_count():
    board = Plane()
    assert board._field_count == 40
    assert board._fields == CARDS


def test_position():
    board = Plane()
    card = board.get_field_from_position(6)
    card2 = board.get_field_from_position(40)
    assert card.name() == "Bus Station"
    assert card2.name() == "Dubai"


def test_is_property():
    card = Card("Phoenix", "red", 1750000, 175000)
    assert card.is_property() is True


def test_is_property_not():
    card = Card("Revenue tax", None, None, 1500000, "TAX")
    assert card.is_property() is False


def test_get_state_available_to_buy():
    card = Card("Phoenix", "red", 1750000, 175000)
    assert card.get_state() == "available to buy"
