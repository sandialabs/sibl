"""
This module tests the XYFactory class.
To run

$ conda activate siblenv
(siblenv) $ cd ~/sibl
(siblenv) [~/sibl]$ pytest cli/tests/model/test_factory.py -v
"""

import os
from unittest import TestCase, main

# import xyfigure.client as client
# import xyfigure.code.client as client
# import xyfigure.code.client as client
import xyfigure.client as client


class MyTestCase(TestCase):
    """This is the unit test for the XYFactory class."""

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("cli", "tests", "model")
        return super().setUpClass()

    def test_unknown_factory_item_request(self):
        jfile = os.path.join(self.path, "u-squared-ddt1-model-type-defect.json")
        result = client.main([jfile])
        self.assertIsNone(result)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
