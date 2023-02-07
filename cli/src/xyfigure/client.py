#!/usr/bin/env python
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import sys
import json

# related third-party imports

# local application/library specific imports
# from xyfigure.factory import XYFactory
# from xyfigure.code.factory import XYFactory
from xyfigure.factory import XYFactory

# from xyfigure.xymodel import XYModel
# from xyfigure.code.xymodel import XYModel
from xyfigure.xymodel import XYModel, XYModelAbaqus

# from xyfigure.xyview import XYView
# from xyfigure.code.xyview import XYView
from xyfigure.xyview import XYView, XYViewAbaqus


def main(argv):
    """Client to generate a XYFigure from an 'input_file.json' file.

    Preconditions:
    $ conda activate siblenv
    $ ~/sibl/cli/io/example/input_file.json  # recipie to create XYFigure object(s)

    Use:
    $ cd ~/sibl/cli/io/example/
    $ python ~/sibl/cli/src/xyfigure/client.py input_file.json
    """

    # to do, add argparse with verbose flag, for now, hard code
    # verbose = False
    verbose = True

    help_string = "$ python ~/sibl/cli/src/xyfigure/client.py input_file.json"
    try:
        input_file = argv[0]
    except IndexError as error:
        print(f"Error: {error}.")
        print("check script pattern: " + help_string)
        print("Abnormal script termination.")
        sys.exit("No input file specified.")

    with open(input_file) as f:
        database = json.load(f)

    items = []  # cart of items is empty, fill from factory
    # factory = XYFactory()  # it's static!

    for item in database:
        kwargs = database[item]
        i = XYFactory.create(item, **kwargs)
        if i:
            items.append(i)
        else:
            print("Item is None from factory, nothing added to Client items.")

    models = [i for i in items if isinstance(i, (XYModel, XYModelAbaqus))]
    views = [i for i in items if isinstance(i, (XYView, XYViewAbaqus))]

    for view in views:
        if verbose:
            print(f'Creating view with guid = "{view.guid}"')

        if view.model_keys:  # register only selected models with current view
            if verbose:
                print(f"  Adding {view.model_keys} model(s) to current view.")
            view.models = [m for m in models if m.guid in view.model_keys]
            view.figure()  # must be within this subset scope
        else:
            if verbose:
                print("  Adding all models to current view.")
            view.models = models  # register all models with current view
            view.figure()  # must be within this subset scope

    if verbose:
        print("====================================")
        print("End of xyfigure/client.py execution.")


if __name__ == "__main__":
    main(sys.argv[1:])


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
