"""
This module is a unit test of the image_diff.py script.
To run

$ python -m unittest image_diff_test.py

"""
import unittest
import image_diff as idff

class TestImageDiff(unittest.TestCase):

    # def __init__(self):
    #     # super().__init__()

    # self._original = 'image_diff_test_original.png'
    # self._clone = 'image_diff_test_clone.png'
    # self._different = 'image_diff_test_different.png'

    def test_same(self):
        # self.assertTrue(idff.same(self._original, self._clone), verbose=True))
        # idff.same(self._original, self._clone, verbose=True)
        self.assertTrue(idff.same('image_diff_test_original.png', 'image_diff_test_clone.png'))

    def test_different(self):
        # self.assertTrue(idff.same(self._original, self._clone), verbose=True))
        # idff.same(self._original, self._clone, verbose=True)
        self.assertFalse(idff.same('image_diff_test_original.png', 'image_diff_test_different.png'))
        self.assertFalse(idff.same('image_diff_test_clone.png', 'image_diff_test_different.png'))

if __name__ == '__main__':
    unittest.main()
