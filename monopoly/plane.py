class Card:
    """
    The Card class.

    Used to represent a property card from the Monopoly game.
    It has all the attributes a real card from the game would have.
    Objects of this class are crucial to the gameplay.
    """
    def __init__(self, name, color=None, price=None, fee=0, card_type="FIELD"):
        """
        Initializes a card object.
        :param name: The name of the card, the only required argument.
        :param color: The color of the card - separates different monopolies.
        :param price: The price of the card, None by deafult.
        :param fee: The fee for landing on the card, 0 by default.
        :param card_type: The type of card - used do determine property cards,
        from utility card that have different importance to the game.

        Attributes:
            houses: Number of houses on a property card.
        set to 0 when a card objet is initialized.
            owner: The owner of a card. If not none,
    (bought card), it is an instance of the player class.
            house_price: Price to buy a house (or hotel) on a property.
            hotel: The presence of a hotel on a property.
        """
        self._name = name
        self._type = card_type
        self._price = price
        self._color = color
        self._fee = fee
        self._houses = 0
        self._owner = None
        if price:
            self._house_price = price / 2
        else:
            self._house_price = None
        self._hotel = None

    def owner(self):
        """
        Get the owner of the card.
        :return: The owner of the card.
        """
        return self._owner

    def price(self):
        """
        Get the price of the card.
        :return: The price of the card.
        """
        return self._price

    def houses(self):
        """
        Get the current number of houses on the card.
        :return: The number of houses on the card.
        """
        return self._houses

    def hotel(self):
        """
        Checks if there is a hotel on the card.
        :return: The hotel on the card.
        """
        return self._hotel

    def house_price(self):
        """
        Get the price of a house on the card.
        Since the house price is the price divided by 2,
        the function could often return a float.
        Thus, it returns it as an int.
        :return: The price of a house on the card.
        """
        if self._house_price:
            return int(self._house_price)
        return self._house_price

    def add_houses(self, amount):
        """
        Add the number of houses on the card.
        :param amount: The number of houses to add to the card.
        """
        self._houses += amount

    def set_houses(self, amount):
        """
        Change the number of houses on the card.
        :param amount: The number of houses to set on the card.
        """
        self._houses = amount

    def set_hotel(self):
        """
        Build a hotel on a card.
        Sets the hotel attribute from None to 1.
        """
        self._hotel = 1

    def possible_num_houses(self):
        """
        Get the maximum number of houses that can be built on the card.
        Since a card can have a maximum of 4 houses,
        it returns the difference of 4 and current number of houses.
        :return: The maximum number of houses that can be built on the card.
        """
        return 4 - self._houses

    def set_owner(self, player):
        """
        Set the owner of the card.
        :param player: The buyer of the card.
        """
        self._owner = player

    def fee(self):
        """
        Get the fee for landing on the card.
        The fee varies by the number of houses,
        or the presence of a hotel on a card.
        :return: The fee paid for landing on the card.
        """
        if self._houses == 0:
            return self._fee
        if self._houses == 1:
            return self._fee * 5
        if self._houses == 2:
            return self._fee * 15
        if self._houses == 3:
            return self._fee * 30
        if self._houses == 4:
            return self._fee * 40
        if self._hotel:
            return self._fee * 50

    def color(self):
        """
        Get the color of the card.
        :return: The color of the card.
        """
        return self._color

    def type(self):
        """
        Get the type of the card.
        :return: The type of the card.
        """
        return self._type

    def name(self):
        """
        Get the name of the card.
        :return: The name of the card.
        """
        return self._name

    def is_property(self):
        """
        Check if the card is a property.
        :return: True if the card is a property, else False.
        """
        return self._type == 'FIELD'

    def get_state(self):
        """
        Get the state of the card.
        Used throughout the game to inform the player,
        what is the state of the card he landed on.
        :return: The state of the card as a string.
        """
        if self.is_property():
            if self._owner:
                return f"bought by {self._owner.name()}"
            else:
                return "available to buy"
        else:
            return "not buyable"


"""
The possible chance values for when player lands on a chance field.
There are both positive and negative values, as player can either
lose or earn money from a chance field.
"""
CHANCES = [
    500000,
    750000,
    200000,
    350000,
    1000000,
    -500000,
    -750000,
    -200000,
    -350000,
    -1000000
]

"""
All the cards used in the game.
Their order is important, as its set for the whole game.

The order they are in is the same as in the Monopoly World game.
"""
CARDS = [
    Card("Start", card_type="START"),
    Card("Istanbul", "brown", 350000, 35000),
    Card("Chance", card_type="CHANCE"),
    Card("Ankara", "brown", 350000, 35000),
    Card("Income tax", None, None, 1000000, "TAX"),
    Card("Bus Station", "transport", 1000000, 500000),
    Card("Gdansk", "grey", 750000, 75000),
    Card("Chance", card_type="CHANCE"),
    Card("Lublin", "grey", 750000, 75000),
    Card("Warsaw", "grey", 1000000, 100000),
    Card("Parking", card_type="PARKING"),
    Card("Valencia", "pink", 1000000, 100000),
    Card("Solar Power Plant", "power", 750000, 350000),
    Card("Barcelona", "pink", 1000000, 100000),
    Card("Madrid", "pink", 1200000, 120000),
    Card("Train Station", "transport", 1000000, 500000),
    Card("Naples", "orange", 1400000, 140000),
    Card("Chance", card_type="CHANCE"),
    Card("Rome", "orange", 1400000, 140000),
    Card("Milan", "orange", 1600000, 160000),
    Card("Parking", card_type="PARKING"),
    Card("Phoenix", "red", 1750000, 175000),
    Card("Chance", card_type="CHANCE"),
    Card("Chicago", "red", 1750000, 175000),
    Card("Los Angeles", "red", 2000000, 200000),
    Card("Airport", "transport", 1000000, 500000),
    Card("Lyon", "yellow", 2200000, 220000),
    Card("Marseille", "yellow", 2200000, 220000),
    Card("Wind Power Plant", "power", 750000, 350000),
    Card("Paris", "yellow", 2400000, 240000),
    Card("Parking", card_type="PARKING"),
    Card("Helsinki", "green", 2500000, 250000),
    Card("Oslo", "green", 2500000, 250000),
    Card("Chance", card_type="CHANCE"),
    Card("Stockholm", "green", 2700000, 270000),
    Card("Rocket Launch Station", "transport", 1000000, 500000),
    Card("Chance", card_type="CHANCE"),
    Card("Abu Dhabi", "blue", 3000000, 300000),
    Card("Revenue tax", None, None, 1500000, "TAX"),
    Card("Dubai", "blue", 3250000, 325000)
]

"""
The variable that stores the length of the game plane.
"""
PLANE_LENGTH = len(CARDS)


class Plane:
    """
    The Plane class.

    Used to represent the Monopoly board.
    """
    def __init__(self):
        """
        Initializes a Plane object.
        Attributes:
            field_count: Number of fields on the plane
            fields: Objects of the Card class, representing board fields.
        """
        self._field_count = PLANE_LENGTH
        self._fields = CARDS

    def get_field_from_position(self, position):
        """
        Get the field at a specific position on the plane.
        :param position: The position of the field on the plane.
        :return: The field at the specified position.
        """
        return self._fields[position - 1]

    def fields(self):
        """
        Get all the fields on the plane.
        :return: A list of fields on the plane.
        """
        return self._fields
