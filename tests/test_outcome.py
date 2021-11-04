from roulette import *
from unittest import TestCase

class TestOutcome(TestCase):
    def test_outcome():
        o1 = Outcome("Red", 1)
        o2 = Outcome("Red", 1)
        o3 = Outcome("Black", 2)
        assert str(o1) == "Red (1:1)"
        assert repr(o2) == "Outcome(name='Red', odds=1)"
        assert o1 == o2
        assert o1.odds == 1
        assert o1.name == "Red"
        assert o3.name == "Black"
        assert o3.odds == 2
        assert o3.odds > o1.odds
        assert o1.odds == o2.odds
        assert o1 != o3
        assert o2 != o3
        assert o1.winAmount(5) == 5
        assert o3.winAmount(5) == 10


