"""
This module is a unit test of the image_diff.py script.
To run

# python test_image_diff.py                 # or
$ python -m unittest test_image_diff.py     # for default interaction, and
$ python -m unittest -v test_image_diff.py  # for higher verbosity

"""
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
from unittest import TestCase, main

# related third-party imports

# local application/library specific imports
# from xyfigure.test.image_diff import same
# from xyfigure.code.test.image_diff import same
# from image_diff import same
# from xyfigure.tests.img_same_diff.image_diff import same
from .image_diff import same


class TestImageDiff(TestCase):
    @classmethod
    def setUpClass(cls):

        # cls._path_str = "xyfigure/code/test/img_same_diff/"
        # cls._path_str = "xyfigure/tests/img_same_diff/"
        cls._path_str = "cli/tests/img_same_diff/"
        # cls._orig = cls._path_str + 'image_diff_test.png'
        # cls._same = cls._path_str + 'image_diff_test_clone.png'
        # cls._diff = cls._path_str + 'image_diff_test_diff.png'
        cls._orig = cls._path_str + "H_460_460_px_RGBA_846400.png"
        cls._same = cls._path_str + "H_460_460_px_RGBA_846400_clone.png"
        cls._diff = cls._path_str + "H_460_460_px_RGBA_846400_diff.png"
        # cls._no_such_file = cls._path_str + 'no_such_file.png'
        cls._verbose = False  # verbose

    # @classmethod
    # def tearDownClass(cls):
    #     print(cls._path_str + ' completed.')

    def test_same(self):
        self.assertTrue(same(self._orig, self._same, self._verbose))

    def test_different(self):
        self.assertFalse(same(self._orig, self._diff, self._verbose))
        self.assertFalse(same(self._same, self._diff, self._verbose))

    # def test_no_such_file(self):
    #     with self.assertRaises(IOError) as context:
    #         same(self._orig, self._no_such_file, self._verbose)
    #     # self.assertEqual(IOError, the_exception)
    #     self.assertTrue('cannot open a file' in str(context.exception))


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
