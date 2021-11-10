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

    def winAmount(self, amount: float) -> float:
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

        return self.name == other.name and self.odds == other.odds

    def __ne__(self, other) -> bool:
        """

        :param self: Outcome object
        :param other: Another outcome object to compare against
        :return: Returns true if outcome names are not the same
        """

        return self.name != other.name or self.odds != other.odds

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

    def __init__(self, outcomes={}):
        """

        :param outcomes:set of outcomes that will become a frozenset to make up the initial bin
        """
        self.outcomes = frozenset(outcomes)

    def addOutcome(self, outcome):
        """

        :param outcome: Outcome() to be added to the bin
        :return: Updates the outcomes in the bin
        """
        self.outcomes |= {outcome}


class Wheel:

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

    def get(self, loc: int) -> Bin:
        return self.bins[loc]


class BinBuilder:

    wheel: Wheel

    def __init__(self, w: Wheel) -> None:
        self.wheel = w

    def straightbets(self, odds):
        self.wheel.addOutcome(37, Outcome("00", odds))
        for i in range(0, 37):
            self.wheel.addOutcome(i, Outcome(str(i), odds))

    def leftrighthelper(self, pos, odds):
        out = Outcome(str(pos) + '-' + str(pos + 1), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)

    def updownhelper(self, pos, odds):
        out = Outcome(str(pos) + '-' + str(pos + 3), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 3, out)

    def splitbets(self, odds):
        r = 0
        while r < 12:
            c1 = 3*r+1
            c2 = 3*r+2

            self.leftrighthelper(c1, odds)
            self.leftrighthelper(c2, odds)

            if r < 11:
                c3 = c2+1
                self.updownhelper(c1, odds)
                self.updownhelper(c2, odds)
                self.updownhelper(c3, odds)
            r += 1

    def streetbets(self, odds):
        for r in range(12):
            n = 3*r + 1
            out = Outcome(str(n) + '-' + str(n + 1) + '-' + str(n+2), odds)
            self.wheel.addOutcome(n, out)
            self.wheel.addOutcome(n+1, out)
            self.wheel.addOutcome(n+2, out)

    def cornerhelper(self, pos, odds):
        out = Outcome(str(pos) + '-' + str(pos + 1) + '-' + str(pos+3) + '-' + str(pos+4), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)
        self.wheel.addOutcome(pos + 3, out)
        self.wheel.addOutcome(pos + 4, out)

    def cornerbets(self, odds):
        for r in range(11):
            c1 = 3*r+1
            c2 = 3*r+2
            self.cornerhelper(c1, odds)
            self.cornerhelper(c2, odds)

    def linehelper(self, pos, odds):
        out = Outcome(str(pos) + '-' + str(pos + 1) + '-' + str(pos + 2) + '-' + str(pos+3)
                      + '-' + str(pos+4) + '-' + str(pos + 5), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)
        self.wheel.addOutcome(pos + 2, out)
        self.wheel.addOutcome(pos + 3, out)
        self.wheel.addOutcome(pos + 4, out)
        self.wheel.addOutcome(pos + 5, out)

    def linebets(self, odds):
        for r in range(11):
            c1 = 3*r + 1
            self.linehelper(c1, odds)

    def dozenbets(self, odds):
        for d in range(3):
            out = Outcome('Dozen ' + str(d+1), odds)
            for m in range(12):
                self.wheel.addOutcome(12*d+m+1, out)

    def columnbets(self, odds):
        for c in range(3):
            out = Outcome('Column ' + str(c+1), odds)
            for m in range(12):
                self.wheel.addOutcome(3*m+c+1, out)

    def evenmoneybets(self, odds):
        red_bins = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        high_outcome = Outcome("High", odds)
        low_outcome = Outcome("Low", odds)
        even_outcome = Outcome("Even", odds)
        odd_outcome = Outcome("Odd", odds)
        red_outcome = Outcome("Red", odds)
        black_outcome = Outcome("Black", odds)
        for n in range(1, 37):
            if n < 19:
                self.wheel.addOutcome(n, low_outcome)
            else:
                self.wheel.addOutcome(n, high_outcome)

            if n % 2:
                self.wheel.addOutcome(n, odd_outcome)
            else:
                self.wheel.addOutcome(n, even_outcome)

            if n in red_bins:
                self.wheel.addOutcome(n, red_outcome)
            else:
                self.wheel.addOutcome(n, black_outcome)

    def fivebet(self, odds):
        five_outcome = Outcome("Five Bet", odds)
        for i in [0, 37, 1, 2, 3]:
            self.wheel.addOutcome(i, five_outcome)

    def buildbins(self) -> None:
        self.straightbets(35)
        self.splitbets(17)
        self.streetbets(11)
        self.cornerbets(8)
        self.linebets(5)
        self.dozenbets(2)
        self.columnbets(2)
        self.evenmoneybets(1)
        self.fivebet(6)
