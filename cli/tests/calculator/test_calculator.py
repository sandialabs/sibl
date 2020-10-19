import unittest

# from xyfigure.tests.calculator import calculator
# import calculator as calc
# from xyfigure.calculator import calculator
import xyfigure.calculator as calc


class MyTestCase(unittest.TestCase):
    """
    To test on command line:
    (siblenv) $ cd ~/sibl
    (siblenv) $ pytest cli/tests/calculator/test_calculator.py -v
    """

    def test_add(self):
        # total = calculator.add(4, 5)
        total = calc.example_add(4, 5)
        assert total == 9

    def test_subtract(self):
        # total = calculator.subtract(9, 5)
        total = calc.example_subtract(9, 5)
        assert total == 4

    def test_multiply(self):
        # total = calculator.multiply(10, 3)
        total = calc.example_multiply(10, 3)
        assert total == 30

    def test_divide(self):
        # total = calculator.divide(9, 3)
        total = calc.example_divide(9, 3)
        assert total == 3
