from monopoly.plane import PLANE_LENGTH


class NotEnoughMoneyException(Exception):
    """
    The NotEnoughMoneyException

    Used when player is trying to make a payment,
    of an amount he doesn't have.

    :param amount: The amount he has to pay.
    """
    def __init__(self, amount):
        super().__init__(
            f"You don't have enough money to make payment of amount: {amount}."
            )


class Player:
    """
    The Player class.

    Used to represent a player (user).
    """
    def __init__(self, name):
        """
        Initializes a Player object.
        :param name: The name of the player.
        Attributes:
            cash: the bank balance of each player.
        Every player is created with the starting balance of 15000000.
            cards: list of players owned cards.
            position: player's position on the game plane.
        """
        self._cash = 15000000
        self._name = name
        self._cards = []
        self._position = 1

    def name(self):
        """
        Get the name of the player.
        :return: The name of the player.
        """
        return self._name

    def cash(self):
        """
        Get the bank balance of the player.
        :return: The cash of the player.
        """
        return self._cash

    def position(self):
        """
        Get the current position of the player on the plane.
        :return: The current position of the player on the plane.
        """
        return self._position

    def is_in_game(self):
        """
        Check if the player is still in the game.
        :return: True if the player has cash greater than 0, else False.
        """
        return self._cash > 0

    def change_balance(self, amount):
        """
        Change the balance of the player by a specific amount.
        It is used to buy properties, or add chance values to players account.
        That's why chances have both positive and negative values.
        If a negative chance value is drawn, the player would earn that amount.
        :param amount: The amount to be subtracted from the player's cash.
        :raise: NotEnoughMoneyException if the player doesn't have
        enough money to make the payment.
        """
        if not self.has_enough_money_to_pay(amount):
            raise NotEnoughMoneyException(amount)
        self._cash -= amount

    def earn(self, amount):
        """
        Add a specific amount to the player's cash.
        :param amount: The amount to be added to the player's cash.
        """
        self._cash += amount

    def can_build_houses(self, card):
        """
        Check if the player can build houses on a specific card.
        Since some monopolies have 2 cards and some have 3,
        it has different conditions for them.
        Also, it checks if there is a hotel on the card,
        since you can't have houses and a hotel.
        :param card: The card to be checked.
        :return: True if the player can build houses on the card, else False.
        """
        color = card.color()
        monopoly = []
        if card.houses() is not None:
            if card.houses() < 4:
                for cards in self._cards:
                    if cards.color() == color:
                        monopoly.append(cards)
                if (color == "brown" or color == "blue") and len(monopoly) == 2:  # noqa
                    monopoly = []
                    return True
                elif (color == "brown" or color == "blue") and len(monopoly) < 2:  # noqa
                    monopoly = []
                    return False
                if color != "power" and color != "transport" and len(monopoly) == 3:  # noqa
                    monopoly = []
                    return True
                else:
                    monopoly = []
                    return False
            else:
                return False
        else:
            return False

    def build_houses(self, card, amount):
        """
        Build houses on a specific card.
        Charges the player's account the price of the built houses.
        :param card: The card on which the houses are to be built.
        :param amount: The number of houses to be built.
        """
        card.add_houses(amount)
        self.change_balance(amount * card.house_price())

    def can_build_hotel(self, card):
        """
        Check if the player can build a hotel on a specific card.
        It can only happen when there are 4 houses on the card.
        :param card: The card to be checked.
        :return: True if the player can build a hotel on the card, else False.
        """
        if card.houses() == 4 and card.owner() == self:
            return True
        else:
            return False

    def build_hotel(self, card):
        """
        Builds a hotel on a specific card.
        Also, it sets the number of houses to None,
        so the fee getter from the plane class can go to the last if statement.
        Charges player's account the price of a hotel (the same as house's).
        :param card: The card on which the hotel is to be built.
        """
        card.set_houses(None)
        card.set_hotel()
        self.change_balance(card.house_price())

    def pay_another_player(self, player, amount):
        """
        Make a payment to another player.
        Called when player pays a fee to another player.
        :param player: The player to whom the payment is to be made.
        :param amount: The amount to be paid.
        """
        self._cash -= amount
        player.earn(amount)

    def buy_card(self, card):
        """
        Buys a card from the plane.
        Charges the player the price of the property.
        Adds the card to player's cards.
        :param card: The card to be bought.
        """
        self.change_balance(card._price)
        self._cards.append(card)
        card.set_owner(self)

    def make_move(self, dice):
        """
        Moves the player forward on the plane.
        Uses the dice to determine the displacement.

        When position is bigger than the number of fields
        (player completed a lap around the board),
        subtracts the number of fields so the position
        still matches the positions of cards.

        IMPORTANT: this function also gives the player
        the bonus for completing a lap and crossing the start field.

        :param dice: The dice to be thrown.
        :return: The new position of the player on the plane.
        """
        move = dice.make_throw()
        self._position += move
        if self._position >= PLANE_LENGTH:
            self.earn(2000000)
            self._position -= PLANE_LENGTH
        return self._position

    def has_enough_money_to_pay(self, amount):
        """
        Check if the player has enough money to make a payment.
        :param amount: The amount of the payment.
        :return: True if the player has enough money, else False.
        """
        return self._cash >= amount
