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

        :param amount: The amount that was bet on the outcome
        :return: amount bet on outcome multiplied by the odds on the bet
        """
        return amount * self.odds

    def __eq__(self, other) -> bool:
        """

        :param other: Another outcome object to compare against
        :return: Returns true if outcome names are the same
        """

        return self.name == other.name and self.odds == other.odds

    def __ne__(self, other) -> bool:
        """

        :param other: Another outcome object to compare against
        :return: Returns true if outcome names are not the same
        """

        return self.name != other.name or self.odds != other.odds

    def __hash__(self) -> int:
        """

        :return: hash value of outcome object (integer)
        """
        return hash(self.name)

    def __str__(self) -> str:
        """

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

    def __init__(self, outcomes={}) -> None:
        """

        :param outcomes:set of outcomes that will become a frozenset to make up the initial bin
        """
        self.outcomes = frozenset(outcomes)

    def addOutcome(self, outcome: Outcome) -> None:
        """

        :param outcome: Outcome() to be added to the bin
        :return: Updates the outcomes in the bin
        """
        self.outcomes |= {outcome}


class Wheel:

    bins: collections.abc.Sequence
    all_outcomes: dict
    rng: int

    def __init__(self) -> None:
        """

        """
        self.bins = tuple(Bin() for i in range(38))
        self.all_outcomes = {}
        self.rng = random.Random()


    def addOutcome(self, number: int, outcome: Outcome) -> None:
        """

        :param number:
        :param outcome:
        :return:
        """
        self.all_outcomes[outcome.name] = outcome
        self.bins[number].addOutcome(outcome)

    def choose(self) -> Bin:
        """

        :return:
        """
        return self.rng.choice(self.bins)

    def get(self, loc: int) -> Bin:
        """

        :param loc:
        :return:
        """
        return self.bins[loc]

    def getOutcome(self, name) -> Outcome:
        """

        :param name:
        :return:
        """
        return self.all_outcomes[name]


class BinBuilder:

    wheel: Wheel

    def __init__(self, w: Wheel) -> None:
        """

        :param w:
        """
        self.wheel = w

    def straightbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        self.wheel.addOutcome(37, Outcome("00", odds))
        for i in range(0, 37):
            self.wheel.addOutcome(i, Outcome(str(i), odds))

    def leftrighthelper(self, pos: int, odds: int) -> None:
        """

        :param pos:
        :param odds:
        :return:
        """
        out = Outcome(str(pos) + '-' + str(pos + 1), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)

    def updownhelper(self, pos: int, odds: int) -> None:
        """

        :param pos:
        :param odds:
        :return:
        """
        out = Outcome(str(pos) + '-' + str(pos + 3), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 3, out)

    def splitbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
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

    def streetbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        for r in range(12):
            n = 3*r + 1
            out = Outcome(str(n) + '-' + str(n + 1) + '-' + str(n+2), odds)
            self.wheel.addOutcome(n, out)
            self.wheel.addOutcome(n+1, out)
            self.wheel.addOutcome(n+2, out)

    def cornerhelper(self, pos: int, odds: int) -> None:
        """

        :param pos:
        :param odds:
        :return:
        """
        out = Outcome(str(pos) + '-' + str(pos + 1) + '-' + str(pos+3) + '-' + str(pos+4), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)
        self.wheel.addOutcome(pos + 3, out)
        self.wheel.addOutcome(pos + 4, out)

    def cornerbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        for r in range(11):
            c1 = 3*r+1
            c2 = 3*r+2
            self.cornerhelper(c1, odds)
            self.cornerhelper(c2, odds)

    def linehelper(self, pos: int, odds: int) -> None:
        """

        :param pos:
        :param odds:
        :return:
        """
        out = Outcome(str(pos) + '-' + str(pos + 1) + '-' + str(pos + 2) + '-' + str(pos+3)
                      + '-' + str(pos+4) + '-' + str(pos + 5), odds)
        self.wheel.addOutcome(pos, out)
        self.wheel.addOutcome(pos + 1, out)
        self.wheel.addOutcome(pos + 2, out)
        self.wheel.addOutcome(pos + 3, out)
        self.wheel.addOutcome(pos + 4, out)
        self.wheel.addOutcome(pos + 5, out)

    def linebets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        for r in range(11):
            c1 = 3*r + 1
            self.linehelper(c1, odds)

    def dozenbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        for d in range(3):
            out = Outcome('Dozen ' + str(d+1), odds)
            for m in range(12):
                self.wheel.addOutcome(12*d+m+1, out)

    def columnbets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        for c in range(3):
            out = Outcome('Column ' + str(c+1), odds)
            for m in range(12):
                self.wheel.addOutcome(3*m+c+1, out)

    def evenmoneybets(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
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

    def fivebet(self, odds: int) -> None:
        """

        :param odds:
        :return:
        """
        five_outcome = Outcome("Five Bet", odds)
        for i in [0, 37, 1, 2, 3]:
            self.wheel.addOutcome(i, five_outcome)

    def buildbins(self) -> None:
        """

        :return:
        """
        self.straightbets(35)
        self.splitbets(17)
        self.streetbets(11)
        self.cornerbets(8)
        self.linebets(5)
        self.dozenbets(2)
        self.columnbets(2)
        self.evenmoneybets(1)
        self.fivebet(6)


class Bet:
    """

    """
    amountBet: int
    outcome: Outcome

    def __init__(self, amount: int, outcome: Outcome ) -> None:
        """

        :param amount:
        :param outcome:
        """
        self.amountBet = amount
        self.outcome = outcome

    def winAmount(self) -> int:
        """

        :return:
        """
        return (self.outcome.odds + 1) * self.amountBet

    def loseAmount(self) -> int:
        """

        :return:
        """
        return self.amountBet

    def __str__(self) -> str:
        """

        :return:
        """
        return f"${self.amountBet:d} on {self.outcome}"

    def __repr__(self) -> str:
        """

        :return:
        """
        return f"Bet(amount={self.amountBet:d}, outcome={self.outcome!r})"

class InvalidBet(Exception):
    def __init__(self):
        super().__init__()



class Table:
    """

    """
    limit: int
    minimum: int
    bets: list

    def __init__(self, *inputs) -> None:
        self.limit = 1
        self.minimum = 50
        if inputs is None:
            self.bets = []
        else:
            self.bets = []
            for i in inputs:
                self.bets.append(i)

    def placeBet(self, bet: Bet) -> None:
        self.bets.append(bet)

    def isValid(self) -> None:
        total = 0
        for i in self.bets:
            if i.amountBet < self.minimum:
                raise InvalidBet
            else:
                total += i.amountBet
        if total > self.limit:
            raise InvalidBet

    def __iter__(self):
        return iter(self.bets[:])

    def __str__(self) -> str:
        out_str = "("
        for i in iter(self):
            out_str += str(i)
            out_str += ", "
        out_str = out_str[:-2] + ")"
        return out_str

    def __repr__(self) -> str:
        out_str = "Table("
        for i in iter(self):
            out_str += repr(i)
            out_str += ", "
        out_str = out_str[:-2] + ")"
        return out_str

class Passenger57:
    """
    Player class who always bets on black
    """
    black: Bet
    table: Table

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.table = table
        self.wheel = wheel
        self.black = self.wheel.getOutcome("Black")

    def placeBets(self) -> None:
        """

        :return:
        """
        self.table.placeBet(Bet(5,self.black))

    def win(self, bet: Bet) -> None:
        """

        :param bet:
        :return:
        """
        print( str(bet) + " is a winner! You win $" + str(bet.winAmount()))

    def lose(self, bet: Bet) -> None:
        """

        :param bet:
        :return:
        """
        print( str(bet) + " is a loser. You lose $" + str(bet.loseAmount()))


class Game:
    """

    """
    wheel: Wheel
    table: Table
    player: Passenger57

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.wheel = wheel
        self.table = table

    def cycle(self, player: Passenger57):
        player.placeBets()
        wbin = self.wheel.choose()
        for bet in iter(player.table):
            if bet.outcome in wbin.outcomes:
                player.win(bet)
            else:
                player.lose(bet)




