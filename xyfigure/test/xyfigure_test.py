"""
This module is a unit test of the xyfigure service.
To run

$ python -m unittest xyfigure_test.py     # for default interaction, and 
$ python -m unittest -v xyfigure_test.py  # for higher verbosity

"""
# standard library imports
import json
import os
import sys
import unittest

# third-party imports

# local imports
# from test.image_diff import same
# import test.image_diff as idff
# import image_diff as idff
# import client as xyfigure_client
from image_diff import same
# from ..client import main
#from .. client import main
sys.path.insert(0, '../')
import client as xyfigure_client  # from parent directory


class TestImageDiff(unittest.TestCase):

    # https://stackoverflow.com/questions/23667610/what-is-the-difference-between-setup-and-setupclass-in-python-unittest/23670844
    # The difference manifests itself when you have more than one test method 
    # in your class. setUpClass and tearDownClass are run once for the whole class; 
    # setUp and tearDown are run before and after each test method.

    @classmethod
    def setUpClass(cls):
        cls._path_str = 'sibl/xyfigure/test/xyfigure_test.py'
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



if __name__ == '__main__':
    unittest.main()
