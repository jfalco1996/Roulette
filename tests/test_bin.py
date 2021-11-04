from roulette import *
from unittest import TestCase

class TestBin(TestCase):
    def test_bin(self):
        o1 = Outcome("Red", 1)
        o2 = Outcome("Black", 2)
        o3 = Outcome("Red", 4)
        o4 = Outcome("High", 1)
        o5 = Outcome("low", 12)
        b1 = Bin({o1,o2,o3})
        b2 = Bin({o4,o5,o3})
        b3 = Bin({o1,o2,o3,o4,o5})
        b4 = Bin({o3})
        b5 = Bin({o4})
        self.assertSetEqual(b1.intersection(b2), b4)
        self.assertSetEqual(b1.union(b2),b3)
        self.assertTrue(b1.isdisjoint(b5))
        self.assertTrue(b1.issubset(b3) and b2.issubset(b3) and b4.issubset(b3) and b5.issubset(b3))
