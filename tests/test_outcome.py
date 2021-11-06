from roulette import *
from unittest import TestCase

class TestOutcome(TestCase):
    def test_outcome(self):
        o1 = Outcome("Red", 1)
        o2 = Outcome("Red", 1)
        o3 = Outcome("Black", 2)
        self.assertEqual(str(o1),"Red (1:1)")
        self.assertEqual(repr(o2), "Outcome(name='Red', odds=1)")
        self.assertEqual(o1,o2)
        self.assertEqual(o1.odds, 1)
        self.assertEqual(o1.name, "Red")
        self.assertEqual(o3.name, "Black")
        self.assertEqual(o3.odds, 2)
        self.assertTrue(o3.odds > o1.odds)
        self.assertEqual(o1.odds, o2.odds)
        self.assertNotEqual(o1, o3)
        self.assertNotEqual(o2,o3)
        self.assertEqual(o1.winAmount(5), 5)
        self.assertEqual(o3.winAmount(5), 10)


