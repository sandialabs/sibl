"""
This module is a unit test of the image_diff.py script.
To run

$ python -m unittest image_diff_test.py     # for default interaction, and
$ python -m unittest -v image_diff_test.py  # for higher verbosity

"""
import unittest
from image_diff import same

class TestImageDiff(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._path_str = 'sibl/xyfigure/test/image_diff_test.py'
        print(cls._path_str + ' initialized.')

        cls._orig = 'image_diff_test_original.png'
        cls._same = 'image_diff_test_clone.png'
        cls._diff = 'image_diff_test_different.png'

    @classmethod
    def tearDownClass(cls):
        print(cls._path_str + ' completed.')

    def test_same(self):
        # self.assertTrue(same(self._orig, self._same, verbose=True))
        self.assertTrue(same(self._orig, self._same))

    def test_different(self):
        self.assertFalse(same(self._orig, self._diff))
        self.assertFalse(same(self._same, self._diff))


if __name__ == '__main__':
    unittest.main()