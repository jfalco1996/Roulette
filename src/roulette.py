from dataclasses import dataclass


class Outcome:
    """
    Contains a single outcome on which a bet can be placed
    Ex:
    Red, 1:1
    1, 35:1
    """
    name: str
    odds: int

    def __init__(self, name: str, odds: int) -> None:
        self.name = name
        self.odds = odds

    def winAmount(self, amount:float) -> float:
        """
        :param self: Outcome object with a given name and odds
        :param amount: The amount that was bet on the outcome
        :return: amount bet on outcome multiplied by the odds on the bet
        """
        return amount * self.odds

    def __eq__(self, other) -> bool:
        """
        :param self: Outcome object
        :param other: Another outcome object to compare against
        :return: Returns true if outcome names are the same
        """

        return self.name == other.name

    def __ne__(self,other) -> bool:
        """

        :param self: Outcome object
        :param other: Another outcome object to compare against
        :return: Returns true if outcome names are not the same
        """

        return self.name != other.name

    def __hash__(self) -> int:
        """

        :param self: Outcome object
        :return: hash value of outcome object (integer)
        """
        return hash(self.name)

    def __str__(self) -> str:
        """

        :param self: Outcome object
        :return: name of outcome with odds
            Ex:
            "Red (1:1)"
        """
        return f"{self.name:s} ({self.odds:d}:1)"

    def __repr__(self) -> str:
        """

        :return: name of outcome constructor
            Ex:
             "Outcome(name='Red', odds=1)"
        """
        return f"{self.__class__.__name__:s}(name={self.name!r}, odds={self.odds!r})"

class Bin(frozenset):
    pass

