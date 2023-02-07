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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
