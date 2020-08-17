#!/usr/bin/env python
# Client to create figures for Military Specification journal manuscript.
# To run from command line with Python3:
# [base_directory]: $ python ~/sibl/xyfigure/client.py input_file.json

# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports

# related third-party imports

# local application/library specific imports
# from xyfigure.xymodel import XYModel
from xyfigure.code.xymodel import XYModel

# from xyfigure.xyview import XYView
from xyfigure.code.xyview import XYView

# Figure Factory
FACTORY_ITEMS = {"model": XYModel, "view": XYView}


class XYFactory:
    """The one and only (singleton) factory for XY items."""

    @staticmethod
    def create(item, **kwargs):
        "Main factory method, returns XY objects."
        instance = FACTORY_ITEMS.get(kwargs["class"], None)
        if instance:
            return instance(item, **kwargs)

        # If we get here, we did not return an instance, so warn.
        print(f"Warning: {item} requested but not provided by this factory,")
        print("returning None.")
        return None
