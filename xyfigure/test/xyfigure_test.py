"""
This module is a unit test of the xyfigure.py script.
To run

$ python -m unittest xyfigure_test.py

"""
import unittest
import json
# from test.image_diff import same
# import test.image_diff as idff
# import image_diff as idff
# import client as xyfigure_client
from image_diff import same
# from ..client import main
#from .. client import main
import os
import sys
sys.path.insert(0, '../')
import client as xyfigure_client  # from parent directory

class TestImageDiff(unittest.TestCase):

    # def __init__(self):
    #     # super().__init__()

    # self._original = 'image_diff_test_original.png'
    # self._clone = 'image_diff_test_clone.png'
    # self._different = 'image_diff_test_different.png'

    def test_sines(self):

        jfile = 't_v_sines.json'
        # print(f'Original json file is {jfile}')

        jfile_test = jfile.split('.')[0] + '_test.json'
        # print(f'Temporary json file is {jfile_test}')

        with open(jfile, 'r') as fin:
            dict_test = json.load(fin)
            # print(dict_test)

            file_a = dict_test['the-figure']['file']
            file_b = file_a.split('.')[0] + '_test.png'
            # print(file_a)
            # print(file_b)
            dict_test['the-figure']['file'] = file_b
            # print(dict_test)

            with open(jfile_test, 'w') as outfile:
                json.dump(dict_test, outfile)

            xyfigure_client.main([jfile_test])
        
            self.assertTrue(same(file_a, file_b))

            os.remove(jfile_test)
            os.remove(file_b)


    def test_same(self):
        # self.assertTrue(idff.same(self._original, self._clone), verbose=True))
        # idff.same(self._original, self._clone, verbose=True)
        self.assertTrue(same('image_diff_test_original.png', 'image_diff_test_clone.png'))

    def test_different(self):
        # self.assertTrue(idff.same(self._original, self._clone), verbose=True))
        # idff.same(self._original, self._clone, verbose=True)
        self.assertFalse(same('image_diff_test_original.png', 'image_diff_test_different.png'))
        self.assertFalse(same('image_diff_test_clone.png', 'image_diff_test_different.png'))

if __name__ == '__main__':
    unittest.main()
