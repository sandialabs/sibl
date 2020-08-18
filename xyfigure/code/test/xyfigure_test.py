"""
This module is a unit test of the xyfigure service.
It is run manually from the command line, but is not run as
part of the automated unit test on check in because its name
does not confirm to the test_xxx.py convention (e.g., leading "test_"
naming convention).

WARNING: Soon to be DEPRECATED, do NOT use.

To run

$ cd ~/sibl/xyfigure/code/test
$ python xyfigure_test.py                      # for terse interaction,
$ python -m unittest xyfigure_test             # for default interaction,
$ python -m unittest -v xyfigure_test          # for higher verbosity, and
to test just one of the test methods:

# e.g., to test the test_same() method
$ python -m unittest xyfigure_test.TestImageDiff.test_same
"""
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import os

# import sys
import json
from unittest import TestCase, main

# related third-party imports

# local application/library specific imports
# from xyfigure.test.image_diff import same
# from image_diff import same
from xyfigure.code.test.image_diff import same

# import xyfigure.client as xyfigure_client
# import xyfigure.code.client as xyfigure_client
import xyfigure.code.client as xyfigure_client


class TestImageDiff(TestCase):

    # https://stackoverflow.com/questions/23667610/what-is-the-difference-between-setup-and-setupclass-in-python-unittest/23670844
    # The difference manifests itself when you have more than one test method
    # in your class. setUpClass and tearDownClass are run once for the whole
    # class; setUp and tearDown are run before and after each test method.

    @classmethod
    def setUpClass(cls):
        cls._path = os.path.join("xyfigure", "code", "test")

        # cls._path_str = "sibl/xyfigure/code/test/xyfigure_test.py"
        cls._path_str = os.path.join(cls._path, "xyfigure_test.py")
        print(cls._path_str + " initialized.")

        # cls._img_same_diff = "img_same_diff"
        # cls._img_same_diff = os.path.join("xyfigure", "code", "test", "img_same_diff")
        cls._img_same_diff = os.path.join(cls._path, "img_same_diff")

        cls._orig = os.path.join(cls._img_same_diff, "image_diff_test.png")
        cls._clone = os.path.join(cls._img_same_diff, "image_diff_test_clone.png")
        cls._diff = os.path.join(cls._img_same_diff, "image_diff_test_diff.png")

        cls._rgb_orig = os.path.join(cls._img_same_diff, "H_460_460_px_RGB_634800.png")
        cls._rgb_clone = os.path.join(
            cls._img_same_diff, "H_460_460_px_RGB_634800_clone.png"
        )
        cls._rgba_orig = os.path.join(
            cls._img_same_diff, "H_460_460_px_RGBA_846400.png"
        )
        cls._rgba_clone = os.path.join(
            cls._img_same_diff, "H_460_460_px_RGBA_846400_clone.png"
        )
        cls._rgba_diff = os.path.join(
            cls._img_same_diff, "H_460_460_px_RGBA_846400_diff.png"
        )

        # cls._out = "temp"  # put test files into sibl/xyfigure/test/temp/

        # put test files into sibl/xyfigure/code/test/temp/
        cls._out = os.path.join(cls._path, "temp")

    @classmethod
    def tearDownClass(cls):
        print(cls._path_str + " completed.")

    @classmethod
    def compare_test_to_reference(cls, jfile):
        j_path_file = os.path.join(cls._path, jfile)
        print(f"Reference json file is {j_path_file}")

        jfile_test = os.path.join(cls._out, jfile.split(".")[0] + "_test.json")
        print(f"Test json file is {jfile_test}")

        # with open(jfile, "r") as fin:
        with open(j_path_file, "r") as fin:
            dict_test = json.load(fin)  # make a copy of reference json
            # print(dict_test)  # for debug

            file_a = dict_test["figure"]["file"]
            print(f"Reference png file is {file_a}")

            file_b = os.path.join(cls._out, file_a.split(".")[0] + "_test.png")
            print(f"Test png file is {file_b}")

            dict_test["figure"]["file"] = file_b  # replace png file name
            # print(dict_test)  # for debug

            with open(jfile_test, "w") as outfile:
                json.dump(dict_test, outfile)

            xyfigure_client.main([jfile_test])

            return (file_a, file_b)

    def test_same(self):
        # self.assertTrue(same(self._orig, self._same, verbose=True))
        self.assertTrue(same(self._orig, self._clone))
        self.assertTrue(same(self._rgb_orig, self._rgb_clone))
        self.assertTrue(same(self._rgba_orig, self._rgba_clone))

    def test_different(self):
        self.assertFalse(same(self._orig, self._diff))
        self.assertFalse(same(self._clone, self._diff))

        self.assertFalse(same(self._rgb_orig, self._rgba_orig))

        self.assertFalse(same(self._rgba_orig, self._rgba_diff))
        self.assertFalse(same(self._rgba_clone, self._rgba_diff))

    def test_cosines_prefilter(self):
        jfile = "cosines-prefilter.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_cosines_postfilter(self):
        jfile = "cosines-postfilter.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_integration(self):
        jfile = "zeros-int3.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_signal_process_serialize(self):
        jfile = "signal_process_serialize.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sine(self):
        jfile = "t_v_sines.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sine_time_derivative(self):
        jfile = "t_v_sines_ddt1.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sines_prefilter(self):
        jfile = "t_v_sines_prefilter.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sines_postfilter(self):
        jfile = "t_v_sines_postfilter.json"
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))


if __name__ == "__main__":
    main()  # calls unittest.main()
