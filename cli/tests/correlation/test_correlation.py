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

    def test_006_squares(self):
        verbosity = True

        ref_t = [1.0, 2.0, 3.0]
        ref_y = [2.0, 2.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [4.0, 5.0, 6.0, 7.0]
        sub_y = [3.0, 3.0, 3.0, 3.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        known_y = [0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.4948716593053935

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_007_squares_extended(self):
        verbosity = True

        ref_t = [0.0, 1.0, 2.0, 3.0, 4.0]
        ref_y = [0.0, 2.0, 2.0, 2.0, 0.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
        sub_y = [0.0, 3.0, 3.0, 3.0, 3.0, 0.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
        known_y = [0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 0.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.38490017945975047

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_008_squares_reflected(self):
        verbosity = True

        ref_t = [-3.0, -2.0, -1.0]
        ref_y = [2.0, 2.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [-7.0, -6.0, -5.0, -4.0]
        sub_y = [3.0, 3.0, 3.0, 3.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0]
        known_y = [3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.4948716593053935

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_009_squares_extended_reflected(self):
        verbosity = True

        ref_t = [-4.0, -3.0, -2.0, -1.0, 0.0]
        ref_y = [0.0, 2.0, 2.0, 2.0, 0.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [-8.0, -7.0, -6.0, -5.0, -4.0, -3.0]
        sub_y = [0.0, 3.0, 3.0, 3.0, 3.0, 0.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        known_y = [0.0, 3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.38490017945975047

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_010_squares_subject_negative(self):
        verbosity = True

        ref_t = [1.0, 2.0, 3.0]
        ref_y = [2.0, 2.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [-7.0, -6.0, -5.0, -4.0]
        sub_y = [3.0, 3.0, 3.0, 3.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        known_y = [3.0, 3.0, 3.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.31491832864888675

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_011_reference_negative(self):
        verbosity = True

        ref_t = [-3.0, -2.0, -1.0]
        ref_y = [2.0, 2.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [4.0, 5.0, 6.0, 7.0]
        sub_y = [3.0, 3.0, 3.0, 3.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-11.0, -10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0]
        known_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0]
        known_cc_rel_error = 0.5
        known_L2_error = 0.31491832864888675

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_020_ramp(self):
        verbosity = True

        ref_t = [0.0, 1.0, 2.0]
        ref_y = [0.0, 1.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [1.0, 2.0, 3.0]
        sub_y = [0.0, 1.0, 2.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [-1.0, 0.0, 1.0, 2.0]
        known_y = [0.0, 0.0, 1.0, 2.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_021_ramp_shift_right(self):
        verbosity = True

        ref_t = [1.0, 2.0, 3.0]
        ref_y = [0.0, 1.0, 2.0]
        reference = np.transpose([ref_t, ref_y])

        sub_t = [2.0, 3.0, 4.0]
        sub_y = [0.0, 1.0, 2.0]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = [0.0, 1.0, 2.0, 3.0]
        known_y = [0.0, 0.0, 1.0, 2.0]

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(cc_rel_error, self.TOL)
        self.assertLess(L2_error, self.TOL)

    def test_100_correlation_recipe(self):
        jfile = os.path.join(self.path, "correlation_recipe.json")
        result = client.main([jfile])
        self.assertIsNone(result)

    def test_101_anomaly_recipe(self):
        jfile = os.path.join(self.path, "anomaly_recipe.json")
        result = client.main([jfile])
        self.assertIsNone(result)

    def test_102_anomaly_xcorr(self):
        verbosity = True

        afile = os.path.join(self.path, "signal_a.csv")
        bfile = os.path.join(self.path, "signal_b.csv")

        reference = np.genfromtxt(
            afile,
            dtype="float",
            delimiter=",",
            skip_header=1,
            skip_footer=0,
            usecols=(0, 1),
        )

        subject = np.genfromtxt(
            bfile,
            dtype="float",
            delimiter=",",
            skip_header=1,
            skip_footer=0,
            usecols=(0, 1),
        )

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = np.linspace(1, 21, 21)
        known_y = [0, 1, 2, 3, 3, 0, 1, 2, 3, 4, 0, 1, 1, 4, 4, 0, 1, 2, 3, 4, 0]
        known_cc_rel_error = 0.025
        known_L2_error = 0.08247860988423225

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)

    def test_103_L2_with_constant_signals(self):
        verbosity = True

        ref_t = [10, 11, 12, 13]
        ref_y = [20, 20, 20, 20]
        reference = np.transpose([ref_t, ref_y])

        sub_t = ref_t
        sub_y = [18, 18, 18, 18]
        subject = np.transpose([sub_t, sub_y])

        calculated_t, calculated_y, cc_rel_error, L2_error = xycc(
            reference, subject, verbosity
        )

        known_t = sub_t
        known_y = sub_y
        known_cc_rel_error = 0.1
        known_L2_error = 1.0

        self.assertTrue(self.same(known_t, calculated_t, verbosity))
        self.assertTrue(self.same(known_y, calculated_y, verbosity))
        self.assertLess(abs(known_cc_rel_error - cc_rel_error), self.TOL)
        self.assertLess(abs(known_L2_error - L2_error), self.TOL)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()


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
