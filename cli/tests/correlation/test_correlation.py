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


class XYModelCrossCorrelation(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("cli", "tests", "correlation")
        cls.TOL = 1e-6  # tolerance
        return super().setUpClass()

    @classmethod
    def same(cls, a, b, verbosity=False):

        _same = False
        l2norm_diff = np.linalg.norm(a - b)

        if verbosity:
            print(f"array a = {a}")
            print(f"array b = {b}")
            print(f"l2norm_diff = {l2norm_diff}")

        if np.abs(l2norm_diff) < cls.TOL:
            _same = True

        return _same

    def test_000_hat_1_hat_2(self):
        verbosity = True

        ref_t = [0.0, 1.0, 2.0]
        ref_y = [0.0, 1.0, 0.0]  # hat at 1
        reference = np.transpose([ref_t, ref_y])

        sub_t = [1.0, 2.0, 3.0]
        sub_y = [0.0, 1.0, 0.0]  # hat at 2
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-1.0, 0.0, 1.0, 2.0]
        known_y = [0.0, 0.0, 1.0, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_001_hat_1_double_freq_hat_2(self):
        verbosity = True

        ref_t = [0.0, 0.5, 1.0, 1.5, 2.0]
        ref_y = [0.0, 0.5, 1.0, 0.5, 0.0]  # hat at 1
        reference = np.transpose([ref_t, ref_y])

        sub_t = [1.0, 2.0, 3.0]
        sub_y = [0.0, 1.0, 0.0]  # hat at 2
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
        known_y = [0.0, 0.0, 0.0, 0.5, 1.0, 0.5, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))

    def test_002_hat_1_hat_2_double_freq(self):
        verbosity = True

        ref_t = [0.0, 1.0, 2.0]
        ref_y = [0.0, 1.0, 0.0]  # hat at 1
        reference = np.transpose([ref_t, ref_y])

        sub_t = [1.0, 1.5, 2.0, 2.5, 3.0]
        sub_y = [0.0, 0.5, 1.0, 0.5, 0.0]  # hat at 2
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
        known_y = [0.0, 0.0, 0.0, 0.5, 1.0, 0.5, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_003_hat_2_hat_1(self):
        verbosity = True

        ref_t = [1.0, 2.0, 3.0]
        ref_y = [0.0, 1.0, 0.0]  # hat at 2
        reference = np.transpose([ref_t, ref_y])

        sub_t = [0.0, 1.0, 2.0]
        sub_y = [0.0, 1.0, 0.0]  # hat at 1
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [1.0, 2.0, 3.0, 4.0]
        known_y = [0.0, 1.0, 0.0, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_004_hat_2_double_freq_hat_1(self):
        verbosity = True

        ref_t = [1.0, 1.5, 2.0, 2.5, 3.0]
        ref_y = [0.0, 0.5, 1.0, 0.5, 0.0]  # hat at 2
        reference = np.transpose([ref_t, ref_y])

        sub_t = [0.0, 1.0, 2.0]
        sub_y = [0.0, 1.0, 0.0]  # hat at 1
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        known_y = [0.0, 0.5, 1.0, 0.5, 0.0, 0.0, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_005_hat_2_hat_1_double_freq(self):
        verbosity = True

        ref_t = [1.0, 2.0, 3.0]
        ref_y = [0.0, 1.0, 0.0]  # hat at 2
        reference = np.transpose([ref_t, ref_y])

        sub_t = [0.0, 0.5, 1.0, 1.5, 2.0]
        sub_y = [0.0, 0.5, 1.0, 0.5, 0.0]  # hat at 1
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        known_y = [0.0, 0.5, 1.0, 0.5, 0.0, 0.0, 0.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    # def test_001_hats_recipe(self):
    #     jfile = os.path.join(self.path, "hats_recipe.json")
    #     result = client.main([jfile])
    #     self.assertIsNone(result)

    def test_100_correlation_recipe(self):
        jfile = os.path.join(self.path, "correlation_recipe.json")
        result = client.main([jfile])
        self.assertIsNone(result)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
