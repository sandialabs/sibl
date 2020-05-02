"""
This module defines the butterworth.Process class
"""

# from ..xybase import XYBase  # fix this relative import later
from xyfigure.xybase import XYBase  # fixed

class Process(XYBase):
    """
    The butterworth.Process class defines the API to the Butterworth filter.
    """
    def __init__(self, **kwargs):
        """
        The init method of the butterworth.Process class

        Args:
            **kwargs (**dict):  The keys and values that specify the Butterworth filter.
        """
        super().__init__(**kwargs)