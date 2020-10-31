"""
This module tests signal cross-correlation.
To run

$ conda activate siblenv
(siblenv) $ cd ~/sibl
(siblenv) $ python cli/src/xyfigure/client.py cli/tests/correlation/correlation_recipe.json
(siblenv) [~/sibl]$ pytest cli/tests/correlation/test_correlation.py -v
"""

import os
from unittest import TestCase, main

# import xyfigure.client as client
# import xyfigure.code.client as client
# import xyfigure.code.client as client
import xyfigure.client as client


class MyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join("cli", "tests", "correlation")
        return super().setUpClass()

    def test_correlation_recipe(self):
        jfile = os.path.join(self.path, "correlation_recipe.json")
        result = client.main([jfile])
        self.assertIsNone(result)


# retain main for debugging this file in VS code
if __name__ == "__main__":
    main()  # calls unittest.main()
