import random

from monopoly.display import GameStats, FieldInfo
from monopoly.input import Input
from monopoly.plane import Plane, CHANCES
from monopoly.player import Player

"""
The actions that the player can choose from during his turn'
"""
MENU_DESCRIPTION = "ACTIONS: 0 - roll dice and move,"
MENU_DESCRIPTION += " 1 - print field layout, 2 - quit game"
MENU_END = 2


class Dice:
    """
    Class for simulating throwing of dice.
    """
    def make_throw(self):
        """
        Return a random number between 2 and 12 simulating the throw of dice
        :return: int
        """
        return random.randint(2, 12)


class Game:
    """
    The Game class.

    Class responsible for managing the game process.
    """
    def __init__(self, display):
        """
        Initializes the game.
        :param display: instance of Display class that handles output.
        Attributes:
            input: instance of Input class that handles input.
            players_count: number of players playing.
            plane: instance of Plane class, that represents the board.
            players: list of Player objects playing.
            losers: list that's displayed at the end,
            that contains the players who lost.
            dice: dice that determines the position displacement each throw.
            current_round: number of the current round.
            end_requested: the condition that changes
            when player requests to end the game.
        """
        self._display = display
        self._input = Input()
        self._players_count = 0
        self._plane = Plane()
        self._players = []
        self._losers = []
        self._dice = Dice()
        self._current_round = 0
        self._end_requested = False

    def init_game(self):
        """
        Initializes the game with number of players given by the user.
        Uses input to initialize the number of players.
        """
        self._players_count = int(self._input.ask_for_number_of_players())
        self.init_players()

    def init_players(self):
        """
        Initialize the players and add them to the players list.
        """
        for idx in range(self._players_count):
            self._players.append(Player(f"Player {idx + 1}"))

    def play_game(self):
        """
        Game loop.
        Plays the game until is_game_over returns True.
        When it does, prints the game statistics.
        """
        while not self.is_game_over():
            self.play_a_round()
        self._display.print_end_stats(self._losers, self.find_winners())

    def play_a_round(self):
        """
        Operates playing a round of the game.
        Splits the round into turns for each players.
        Moves the player.
        Checks if the player hasn't lost.
        Updates the game stats and displays them.
        """
        self.increase_round_number()
        for player in self._players:
            self._display.show_message(f"\n It's {player.name()}'s turn")
            if self.show_options() == MENU_END:
                self._display.show_message("End of game")
                break
            else:
                self.move_player(player)

        round_stats = self.calculate_round_stats()
        self._display.refresh_game_round_stats(round_stats)

    def move_player(self, player):
        """
        Moves a player on the game board by the dice number.
        Calls a function that Processes the game state
        after the player landed on a field.
        :param player: Player that's moving.
        """
        if player.is_in_game():
            position = player.make_move(self._dice)
            self.process_after_move(position, player)

    def process_after_move(self, position, player):
        """
        Process what happens after a player lands on a field.
        Calls the check card method to determine what type of card it is.
        Depending on the card, an action connected to the card will be called.
        Checks if the player lost due to the action that happened.
        :param position: Field that the player landed on.
        :param player: The player that jusr moved.
        """
        card = self._plane.get_field_from_position(position)
        self.check_card(card, player)
        self.check_if_player_lose_in_this_round(player)

    def increase_round_number(self):
        """
        Increases the current round number by 1.
        """
        self._current_round += 1

    def is_game_over(self):
        """
        Checks if the game is over,
        by checking if there are less than 2 active players
        or if the end of the game has been requested.
        :return: True if the game ended, else False.
        """
        activePlayers = 0
        for idx in range(self._players_count):
            if self._players[idx].is_in_game():
                activePlayers += 1
        return activePlayers < 2 or self._end_requested

    def calculate_round_stats(self):
        """
        Creates a GameStats object
        and updates it with the current round statistics.
        :return: Current state of the game stats.
        """
        round_stats = GameStats()
        for player in self._players:
            round_stats.set_player_stats(player)
        round_stats.set_round(self._current_round)
        return round_stats

    def find_winners(self):
        """
        Finds the players who are still in the game,
        when the game ends.
        :return: List of players that won.
        """
        winners = []
        for player in self._players:
            if player.is_in_game():
                winners.append(player)
        return winners

    def check_if_player_lose_in_this_round(self, player):
        """
        Checks if the player has lost in this round.
        Adds them to the losers list if they haven't been added yet.
        If the index of the player is not found, it means
        that he hasn't been added yet, so we add him to the list.
        :param player: Player.
        """
        if not player.is_in_game():
            try:
                self._losers.index(player)
            except ValueError:
                self._losers.append(player)

    def landed_someones_card(self, card, player):
        """
        Processes the situation where the player
        landed on a card owned by another player.

        Makes a transaction of the fee from player to player.
        Prints a message informing the players what happened.

        :param card: The card on which the player landed.
        :param player: The player that landed on the card.
        """
        player.pay_another_player(card.owner(), card.fee())
        self._display.show_message(
            f"POSITION: {player.position()} - YOU LANDED ON {card.name()} WHICH IS ALREADY OWNED BY {card.owner().name()}. YOU PAID THE PLAYER A FEE OF {card.fee()}."  # noqa
        )

    def landed_own_card(self, card, player):
        """
        Processes the situation where the player
        landed on his own card.

        Displays the message about landing on his own card.
        Checks if player can build hotels or houses.
        If he can, asks the player if they want to do it.
        If they do, it builds the hotel or the amount of
        houses given by player's input.
        It charges the player's account the price of houses and builds them.

        If he can't build yet, it informs him about it.

        :param card: The card on which the player landed.
        :param player: The player that landed on the card.
        """
        self._display.show_card_info_own(card)
        if player.can_build_hotel(card) is True:
            if self._input.ask_player_to_buy_hotel(card, player) in ["y", "Y"]:
                player.build_hotel(card)
        if player.can_build_houses(card) is True:
            if self._input.ask_player_to_buy_houses(card, player) in ["y", "Y"]:  # noqa
                player.build_houses(card, self._input.ask_number_houses(card))
        else:
            self._display.show_message(
                "You need to have a monopoly to build houses on this field."
                )

    def landed_buyable_field(self, card, player):
        """
        Processes the situation where the player
        landed on a card that's buyable.

        Asks the player if he wants to buy that card.
        If he does, it charges his account and makes him the owner.

        :param card: The card on which the player landed.
        :param player: The player that landed on the card.
        """
        self._display.show_card_info(card)
        if self._input.ask_player_to_buy_card(player) in ["y", "Y"]:
            player.buy_card(card)

    def landed_tax(self, card, player):
        """
        Processes the situation where the player
        landed on a tax field.

        Informs him about it and the amount of the fee.
        Processes the payment to the bank.

        :param card: The card on which the player landed.
        :param player: The player that landed on the card.
        """
        player.change_balance(card.fee())
        self._display.show_message(
            f"POSITION: {player.position()} - YOU LANDED ON A TAX FIELD. YOU PAID THE BANK {card.fee()}."  # noqa
        )

    def landed_chance(self, player):
        """
        Processes the situation where the player
        landed on a chance field.

        Chooses a random chance amount from the list of possible chances.
        Changes player's bank balance,
        gives the information about the amount of the chance.

        :param player: The player that landed on the card.
        """
        chance = random.choice(CHANCES)
        player.change_balance(chance)
        if chance > 0:
            self._display.show_message(
                f"POSITION: {player.position()} - OH NO! YOU LANDED ON A CHANCE FIELD. YOU LOSE {chance}."  # noqa
            )
        if chance < 0:
            chance = abs(chance)
            self._display.show_message(
                f"POSITION: {player.position()} - LUCKY! YOU LANDED ON A CHANCE FIELD. YOU EARN {chance}."  # noqa
            )

    def check_card(self, card, player):
        """
        Checks the type of card.
        Reacts accordingly to the type of card,
        using the methods specified for each type of field.

        Also Processes types not mentioned above,
        "PARKING" and "START.

        :param card: The card on which the player landed.
        :param player: The player that landed on the card.
        """
        if card.owner() and card.owner() != player:
            self.landed_someones_card(card, player)
        elif card.owner() == player:
            self.landed_own_card(card, player)
        else:
            if card.type() == "FIELD":
                self.landed_buyable_field(card, player)
            if card.type() == "TAX":
                self.landed_tax(card, player)
            if card.type() == "PARKING":
                self._display.show_message(
                    f"POSITION: {player.position()} - YOU LANDED ON A PARKING FIELD. NOTHING HAPPENS"  # noqa
                )
            if card.type() == "CHANCE":
                self.landed_chance(player)
            if card.type() == "START":
                player.earn(2000000)
                self._display.show_message(
                    f"POSITION: {player.position()} - YOU LANDED ON A START FIELD. YOU GET 1000000"  # noqa
                )

    def show_options(self):
        """
        Throughout the whole game, displays player's options.
        Collects the input choice option of a player.
        When player chooses 0, it returns 0 (rolls dice and moves him).
        When 1, shows the plane and the cards from the board.
        When 2, ends the game.
        """
        while True:
            self._display.show_message(MENU_DESCRIPTION)
            option = self._input.choose_menu_option(
                "Choose your action: ", [0, 1, 2, MENU_END]
                )
            if option == 0:
                return 0
            elif option == 1:
                self._display.show_fields(self.field_list())
            elif option == MENU_END:
                self._end_requested = True
                return MENU_END

    def field_list(self):
        """
        Creates a list of fields in order to print them.
        Formats them using a FieldInfo object.
        Is used to print out in show_options() method.
        Returns the list of fields.
        """
        fields = []
        for field in self._plane.fields():
            fields.append(FieldInfo(field.name(), field.price(), field.color(), field.get_state()))  # noqa
        return fields
