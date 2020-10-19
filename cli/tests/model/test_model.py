"""
This module tests the XYModel class.
To run

$ conda activate siblenv
(siblenv) $ cd ~/sibl
(siblenv) [~/sibl]$ pytest cli/tests/model/test_model.py -v
"""

import os
import unittest

# import xyfigure.client as client
# import xyfigure.code.client as client
# import xyfigure.code.client as client
import xyfigure.client as client


class MyTestCase(unittest.TestCase):
    """This is the unit test for the XYModel class."""

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("cli", "tests", "model")
        return super().setUpClass()

    @unittest.expectedFailure
    def test_defective_json_keyword_order(self):
        jfile = os.path.join(self.path, "u-squared-ddt1-order-defect.json")
        client.main([jfile])

    def test_verbose_model(self):
        jfile = os.path.join(self.path, "u-squared-ddt1-verbose.json")
        client.main([jfile])

    def test_defective_signal_process(self):
        jfile = os.path.join(self.path, "u-squared-ddt1-signal-process-defect.json")
        client.main([jfile])

    @unittest.expectedFailure
    def test_defective_json_keyword_file(self):
        jfile = os.path.join(self.path, "u-squared-ddt1-file-defect.json")
        client.main([jfile])
