from dataclasses import dataclass
import collections
import os
import random

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
        """

        :param name: String of outcome name
        :param odds: Odds for outcome (Form of outcome is always odds:1)
        """
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
    """
    Contains a collection of outcomes for a single roulette wheel output

    outcomes: set of outcomes for the bin. Outcomes can be added with addOutcome method.

    """
    outcomes: set

    def __init__(self, outcomes = {}):
        """

        :param outcomes:set of outcomes that will become a frozenset to make up the initial bin
        """
        self.outcomes = frozenset(outcomes)

    def addOutcome(self, outcome):
        """

        :param outcome: Outcome() to be added to the bin
        :return: Updates the outcomes in the bin
        """
        self.outcomes |=  {outcome}


class Wheel():

    bins: collections.abc.Sequence
    rng: int

    def __init__(self):
        """

        """
        self.bins = tuple(Bin() for i in range(38))
        self.rng = random.Random()

    def addOutcome(self, number: int, outcome: Outcome) -> None:
        self.bins[number].addOutcome(outcome)

    def choose(self) -> Bin:
        return self.rng.choice(self.bins)

    def get(self,bin: int) -> Bin:
        return self.bins[bin]




