class Display:
    """
    The Display class.

    Responsible for printing game data and managing the interface.
    """
    def refresh_game_round_stats(self, game_state):
        """
        Prints the current round number and statistics for all players.
        It is called at the end of every round's last turn.

        It gives the players information about their position on the plane
        and their bank balance.

        It also prints a dotted line at the end,
        to visually separate rounds in the terminal.

        :param game_state: An instance of GameStats class,
        containing the current game statistics.
        """
        print(f"Round #: {(game_state.round())}")
        print("Player stats:")
        for player_stat in game_state.player_stats():
            print(f"{player_stat.name()}: position: {player_stat.position()}, {player_stat.cash()}")  # noqa
        print("-----------------------------------------------------------------------------------")  # noqa

    def print_end_stats(self, losers, winners):
        """
        Prints the game statistics at the end of the game.
        Shows the winner and losers alongside their stats.
        Prints out a thank you message as it is called when game is over.
        :param losers: A list of players that lost.
        :param winners: A list of players that won.
        """
        print("Losers:")
        for player in losers:
            print(f"{player.name()}, balance: {player.cash()}")
        print("Winners:")
        for player in winners:
            print(f"{player.name()}, balance: {player.cash()}")
        print("Thank you for playing! :)")

    def show_card_info(self, card):
        """
        Informs the player that they landed on a card that can be purchased.
        :param card: An card object.
        """
        print("YOU LANDED ON A FIELD WITH A CARD YOU CAN BUY:")
        print(f"{card.name()}, price: {card.price()}")

    def show_card_info_own(self, card):
        """
        Informs the player that they landed on their card.
        Prints the fee and color of the card.
        :param card: An object representing the card.
        """
        print(f"YOU LANDED ON A FIELD YOU OWN: ({card.name()}).")
        print(f"Fee: {card.fee()}, Color: {card.color()}")

    def show_fields(self, field_infos):
        """
        Upon player's request, prints out a whole list of cards on the plane.

        The cards are numerated by their plane positions.

        Helps player visualize the board and shows information about each card,
        such as price, color and owner.

        Ends by printing a line at the bottom,
        to visually separate the interface.

        :param field_infos: A list of FieldInfo instances.
        """
        num = 0
        for field_info in field_infos:
            num += 1
            print(f"{num}. {field_info.info()}")
        print("-----------------------------------------------------------------------------------")  # noqa

    def show_message(self, msg):
        """
        Prints a message to the user.
        :param msg: The message to be printed.
        """
        print(msg)


class PlayerStat:
    """
    The PlayerStat class.

    Responsible for keeping player statistics,
    that are important during the game.

    It the attributes in one place and makes it easier
    to call them at the same time.
    """
    def __init__(self, name, position, cash):
        """
        Initializes a PlayerStat object.
        :param name: Player's name.
        :param position: Player's current position.
        :param cash: Player's current bank balance.
        """
        self._cash = cash
        self._position = position
        self._name = name

    def cash(self):
        """
        Get the current bank balance of the player.
        :return: Player's cash.
        """
        return self._cash

    def position(self):
        """
        Get the current position of the player.
        :return: Player's position.
        """
        return self._position

    def name(self):
        """
        Get the name of the player.
        :return: Player's name.
        """
        return self._name


class GameStats:
    """
    The GameStats class.

    Class responsible for storing and managing game statistics.
    Gets the stats for display through data-transfer-object
    from the Game object in the game.
    """
    def __init__(self):
        """
        Initialize empty list for storing player statistics and round number.
        Attributes:
            player_stats: the list which stores the statistics.
            round: the number of the current round.
        """
        self._player_stats = []
        self._round = 0

    def set_player_stats(self, player):
        """
        Add a new player statistic to the list.
        :param player: Player object to get statistics from.
        """
        self._player_stats.append(
            PlayerStat(player.name(), player.position(), player.cash())
            )

    def set_round(self, round_number):
        """
        Set the current round number.
        :param round_number: Current round number.
        """
        self._round = round_number

    def player_stats(self):
        """
        Return a list of player statistics.
        :return: List of PlayerStat objects.
        """
        return self._player_stats

    def round(self):
        """
        Return the current round number.
        :return: Integer representing the round number.
        """
        return self._round


class FieldInfo:
    """
    The FieldInfo class.

    Responsible for storing and returning formatted info about a field.
    Instances used when printing a list of all fields on the plane.
    """
    def __init__(self, name, price, color, state):
        """
        Initialize field information with name, price, color, and state.
        :param name: The name of the field.
        :param price: The price of the field.
        :param color: The color of the field.
        :param state: The state of the field.
        """
        self._state = state
        self._color = color
        self._price = price
        self._name = name

    def info(self):
        """
        Return a string with formatted information about the field.
        :return: The field information.
        """
        if self._color:
            return f"{self._name}: price: {self._price}, color: {self._color}, {self._state}"  # noqa
        else:
            return f"{self._name}: price: {self._price}, {self._state}"
