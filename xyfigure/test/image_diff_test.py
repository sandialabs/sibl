"""
This module is a unit test of the image_diff.py script.
To run

# python image_diff_test.py                 # or
$ python -m unittest image_diff_test.py     # for default interaction, and
$ python -m unittest -v image_diff_test.py  # for higher verbosity

"""
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
from unittest import TestCase, main

# related third-party imports

# local application/library specific imports
from xyfigure.test.image_diff import same

class TestImageDiff(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._path_str = 'sibl/xyfigure/test/image_diff_test.py'
        print(cls._path_str + ' initialized.')

        cls._orig = 'image_diff_test.png'
        cls._same = 'image_diff_test_clone.png'
        cls._diff = 'image_diff_test_diff.png'
        cls._verbose = True  # verbose

    @classmethod
    def tearDownClass(cls):
        print(cls._path_str + ' completed.')

    def test_same(self):
        # self.assertTrue(same(self._orig, self._same, verbose=True))
        self.assertTrue(same(self._orig, self._same, self._verbose))

    def test_different(self):
        self.assertFalse(same(self._orig, self._diff, self._verbose))
        self.assertFalse(same(self._same, self._diff, self._verbose))


if __name__ == '__main__':
    main()  # calls unittest.main()
