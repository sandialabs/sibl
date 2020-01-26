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
        cls._out = 'temp'  # put test files into sibl/xyfigure/test/temp/

    @classmethod
    def tearDownClass(cls):
        print(cls._path_str + ' completed.')

    @classmethod
    def compare_test_to_reference(cls, jfile):
        print(f'Reference json file is {jfile}')

        jfile_test = os.path.join(cls._out, jfile.split('.')[0] + '_test.json')
        print(f'Test json file is {jfile_test}')

        with open(jfile, 'r') as fin:
            dict_test = json.load(fin)  # make a copy of reference json
            # print(dict_test)  # for debug

            file_a = dict_test['figure']['file']
            print(f'Reference png file is {file_a}')

            file_b = os.path.join(cls._out, file_a.split('.')[0] + '_test.png')
            print(f'Test png file is {file_b}')

            dict_test['figure']['file'] = file_b  # replace png file name
            # print(dict_test)  # for debug

            with open(jfile_test, 'w') as outfile:
                json.dump(dict_test, outfile)

            xyfigure_client.main([jfile_test])
        
            return (file_a, file_b)

    def test_same(self):
        # self.assertTrue(same(self._orig, self._same, verbose=True))
        self.assertTrue(same(self._orig, self._same))

    def test_different(self):
        self.assertFalse(same(self._orig, self._diff))
        self.assertFalse(same(self._same, self._diff))

    def test_cosines_prefilter(self):
        jfile = 't_v_cosines_prefilter.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_cosines_postfilter(self):
        jfile = 't_v_cosines_postfilter.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sine(self):
        jfile = 't_v_sines.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sine_time_derivative(self):
        jfile = 't_v_sines_ddt1.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sines_prefilter(self):
        jfile = 't_v_sines_prefilter.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_sines_postfilter(self):
        jfile = 't_v_sines_postfilter.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_quadratic(self):
        jfile = 't_v_half_u_squared_test.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_quadratic_ddt1(self):
        jfile = 't_v_half_u_squared_test_ddt1.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_quadratic_ddt2(self):
        jfile = 't_v_half_u_squared_test_ddt2.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))

    def test_quadratic_ddt3(self):
        jfile = 't_v_half_u_squared_test_ddt3.json'
        fa, fb = self.compare_test_to_reference(jfile)
        self.assertTrue(same(fa, fb))


if __name__ == '__main__':
    unittest.main()
