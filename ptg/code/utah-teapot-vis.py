# utah teapot visualization

# import numpy as np

# functional programming, named tuple, Dan Bader, Real Python
# https://realpython.com/lessons/immutable-data-structures-namedtuple/
# import collections

# csv file to namedtuple
# https://stackoverflow.com/questions/9007174/what-is-the-pythonic-way-to-read-csv-file-data-as-rows-of-namedtuples


import csv
from collections import namedtuple

# input file begin
file_control_points = 'utah_teapot_coordinates.csv'
data_type_string = 'float'
data_type_delimiter = ','
n_headers = 0  # no headers in the file_control_points csv file

# input file end

# visualize control points

## tea pot bottom

# named tuple, a named tuple instance is immutable
# ControlPoint = collections.namedtuple('ControlPoint', ['x', 'y', 'z'])
# ControlPoint = namedtuple('ControlPoint', ['x', 'y', 'z'])

control_points_list = []  # this feel wrong b/c it is mutable

with open(file_control_points, mode='rt') as fin:
    reader = csv.reader(fin)
    # ControlPoint = namedtuple("ControlPoint", next(reader))
    ControlPoint = namedtuple("ControlPoint", ['x', 'y', 'z'])
    for data in map(ControlPoint._make, reader):
        print(data.x)
        control_points_list.append(ControlPoint)


control_points = tuple(control_points_list)

a = 4

# with open(file_control_points) as fin:
#     data = np.genfromtxt(file_control_points,
#                          dtype=data_type_string,
#                          delimiter=data_type_delimiter, 
#                          skip_header=n_headers)



## tea pot original (without bottom)


# label control points

# visualize low-frequency Bezier surface

# visualize high-frequency Bezier surface
