#!/usr/bin/env python
# Client to create figures for Military Specification journal manuscript.
# To run from command line with Python3:
# [base_directory]: $ python ~/sibl/xyfigure/client.py input_file.json

# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports

# related third-party imports

# local application/library specific imports
# from xyfigure.xymodel import XYModel
# from xyfigure.code.xymodel import XYModel
from xyfigure.xymodel import XYModel, XYModelAbaqus

# from xyfigure.xyview import XYView
# from xyfigure.code.xyview import XYView
from xyfigure.xyview import XYView, XYViewAbaqus

# Figure Factory
FACTORY_ITEMS = {
    "model": XYModel,
    "view": XYView,
    "model_abaqus": XYModelAbaqus,
    "view_abaqus": XYViewAbaqus,
}


class XYFactory:
    """The one and only (singleton) factory for XY items."""

    @staticmethod
    def create(item, **kwargs):
        "Main factory method, returns XY objects."
        instance = FACTORY_ITEMS.get(kwargs["class"], None)
        if instance:
            return instance(item, **kwargs)

        # If we get here, we did not return an instance, so warn.
        print(f"Warning: key 'class' specified 'value' of '{item}', which is unknown.")
        print("This key will be skipped.")
        return None


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
