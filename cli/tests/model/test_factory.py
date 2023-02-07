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
