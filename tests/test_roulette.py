from roulette import *
from unittest import TestCase

class TestWheel(TestCase):
    def test_wheel(self):
        w = Wheel()
        o1 = Outcome("Red", 1)
        o2 = Outcome("Black", 2)
        o3 = Outcome("Red", 4)
        o4 = Outcome("High", 1)
        o5 = Outcome("low", 12)
        b1 = Bin({o1,o2,o3})
        b2 = Bin({o4,o5,o3})

        for o in b1:
            w.addOutcome(1,o)
        for o in b2:
            w.addOutcome(2,o)
        self.assertEqual(print(w.get(1)),print(b1))
        self.assertEqual(print(w.get(2)),print(b2))

    def test_wheel_sequence(self):
        wheel = Wheel()
        wheel.addOutcome(8, Outcome("test", 1))
        wheel.addOutcome(36, Outcome("test", 2))
        wheel.rng.seed(1)
        self.assertIn(Outcome("test", 1),wheel.choose().outcomes)
        self.assertIn(Outcome("test", 2), wheel.choose().outcomes)