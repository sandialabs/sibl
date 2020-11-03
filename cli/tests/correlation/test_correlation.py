"""
This module tests signal cross-correlation.
To run

$ conda activate siblenv
(siblenv) $ cd ~/sibl
(siblenv) $ python cli/src/xyfigure/client.py cli/tests/correlation/correlation_recipe.json
(siblenv) [~/sibl]$ pytest cli/tests/correlation/test_correlation.py -v
"""

import os
import numpy as np
from unittest import TestCase, main

# import xyfigure.client as client
# import xyfigure.code.client as client
# import xyfigure.code.client as client
import xyfigure.client as client
from xyfigure.xymodel import cross_correlation as xycc


class MyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("cli", "tests", "correlation")
        return super().setUpClass()

    def test_000_xymodel_cross_correlation(self):
        verbosity = True
        signal_ref = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 0.0]])  # reference
        signal_sub = np.array([[1.0, 0.0], [2.0, 1.0], [3.0, 0.0]])  # subject
        xycc(signal_ref, signal_sub, verbosity)

    # def test_001_hats_recipe(self):
    #     jfile = os.path.join(self.path, "hats_recipe.json")
    #     result = client.main([jfile])
    #     self.assertIsNone(result)

    def test_002_correlation_recipe(self):
        jfile = os.path.join(self.path, "correlation_recipe.json")
        result = client.main([jfile])
        self.assertIsNone(result)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
