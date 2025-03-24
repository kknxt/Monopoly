def get_yes_or_no(prompt):
    """
    This function asks the user for a yes or no response.
    It continues to prompt,
    until the user gives a valid response of "y", "Y", "n", or "N".
    :param prompt: The question to display to the user.
    :return: The user's response (y or n).
    """
    response = None
    while response not in ["y", "Y", "n", "N"]:
        response = input(prompt + "(y/n)")
    return response


def input_number(prompt, min=1, max=9):
    """
    This function asks the user for a number within a given range.
    It continues to ask until the user gives a valid response.
    If the user gives other responses than a single number,
    it's going to continue asking him.
    :param prompt: question/command to display to the user.
    :param min: The minimum acceptable value (inclusive), 1 by default.
    :param max: The maximum acceptable value (inclusive), 9 by default.
    :return: The user's response, as an int.
    """
    answer = ""
    while not answer.isnumeric() or int(answer) < min or int(answer) > max:
        answer = input(prompt + f"({min}-{max})")
    return int(answer)


class Input:
    """
    The Input class.

    This class is responsible for asking the player for input.
    The functions of this class displays commands and player options,
    and uses the functions mentioned earlier to collect the keyboard input.
    """
    def ask_player_to_buy_card(self, player):
        """
        This function asks if a player wants to buy a card.
        It uses the before mentioned function get_yes_or_no(prompt),
        to collect the player's answer.
        :param player: The player that is given the option to buy.
        :return: The player's response, y/Y or n/N.
        """
        return get_yes_or_no(f"{player.name()} - You can buy this card. Do you want to? ")  # noqa

    def ask_player_to_buy_houses(self, card, player):
        """
        This function asks a player to buy houses on a card.
        :param card: The card the houses are being purchased for.
        :param player: The card owner, player that's being asked.
        :return: The player's response, y/Y or n/N.
        """
        return get_yes_or_no(
            f"{player.name()} - You can buy houses on this card for {card.house_price()} each. Do you want to? "  # noqa
        )

    def ask_number_houses(self, card):
        """
        This function asks the user for the number of houses they want to buy.
        The prompt informs the user, how many houses they can buy.
        It shows the minimum and maximum value,
        that varies when the card already has houses.
        :param card: The card the houses are being purchased for.
        :return: The number of houses the user wants to buy, as an int.
        """
        return input_number(
            f"Enter the number of houses (maximum: {card.possible_num_houses()}): ", 1, card.possible_num_houses()  # noqa
        )

    def ask_player_to_buy_hotel(self, card, player):
        """
        This function asks a player to build a hotel on a card.
        It informs them about the availability of building it,
        and collects their response.
        :param card: The card the hotel is being purchased for.
        :param player: The card owner, player that's being asked.
        :return: The player's response, y/Y or n/N.
        """
        return get_yes_or_no(
            f"{player.name()} - You can buy a hotel on this card for {card.house_price()}. Do you want to? "  # noqa
        )

    def ask_for_number_of_players(self):
        """
        This function asks the user for the number of players in the game.
        It is called at the beginning of the game,
        its return value sets the number of players for the rest of the game.
        :return: The number of players, as an int.
        """
        return input_number(
            "Welcome to Monopoly! Enter the number of players: ", 2, 8
            )

    def choose_menu_option(self, menu_description, options):
        """
        This function asks the user to choose an option from a menu.
        It is used throughout the entire game duration,
        execute players' menu option choices.
        :param menu_description: A description of the menu options.
        :param options: A list of options.
        :return: The user's chosen option, in the form of assigned int.
        """
        answer = None
        while answer not in options:
            answer = input_number(menu_description, min(options), max(options))
        return answer
