#!/usr/bin/env python
# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import os
import sys
import argparse
import json

# related third-party imports
import numpy as np

# local application/library specific imports
from process.tpav.three_points_angular_velocity import (
    ThreePointsAngularVelocity as tpav,
)


parser = argparse.ArgumentParser()
parser.add_argument(
    "history",
    help="history is a '.csv' that contains the SSM tracer points output file",
)
parser.add_argument(
    "history_to_tpav",
    help="history_to_tpav is a '.json' file that maps 'history.csv' to tpav API format [t, rPx, rPy, rPz, rQx, rQy, rQz, rRx, rRy, rRz, vPx, vPy, vPz, vQx, vQy, vQz, vRx, vRy, vRz]; use 'identity_to_tpav.json' instead of 'history_to_tpav.json' if the 'history.csv' file already has the correct API order; in both .json cases, check the skip_rows number is correct (default is 3); output angular velocity file is 'angular_velocity.csv'",
)
parser.add_argument(
    "--verbose", help="increased feedback in command line", action="store_true"
)
args = parser.parse_args()

# b = os.path.splitext(args.history_to_tpav)
# file_output = b[0] + '.csv'
file_output = "angular_velocity.csv"

with open(args.history_to_tpav) as fin:
    jmap = json.load(fin)

skip_header_rows = jmap["skip_rows"]

if args.verbose:
    print("--------------------------------------------------")
    print("Three points angular velocity (tpav) client begin.")
    print(f"  From path: {os.getcwd()}")
    print(f"  processing SSM tracer points output file: {args.history}")
    print(f"    with number of initial rows skipped = {skip_header_rows}")
    print(f"    with tpav point extraction file: {args.history_to_tpav}")
    print(f"  Output file: {file_output}")


data = np.genfromtxt(
    args.history, dtype="float", delimiter=",", skip_header=skip_header_rows
)

# time
t = data[:, jmap["t"]]

# position point P
rOP_x = data[:, jmap["rPx"]]
rOP_y = data[:, jmap["rPy"]]
rOP_z = data[:, jmap["rPz"]]
rOP = np.array([[rOP_x[i], rOP_y[i], rOP_z[i]] for i in range(len(t))])

# position point Q
rOQ_x = data[:, jmap["rQx"]]
rOQ_y = data[:, jmap["rQy"]]
rOQ_z = data[:, jmap["rQz"]]
rOQ = np.array([[rOQ_x[i], rOQ_y[i], rOQ_z[i]] for i in range(len(t))])

# position point R
rOR_x = data[:, jmap["rRx"]]
rOR_y = data[:, jmap["rRy"]]
rOR_z = data[:, jmap["rRz"]]
rOR = np.array([[rOR_x[i], rOR_y[i], rOR_z[i]] for i in range(len(t))])

# velocity point P
vP_x = data[:, jmap["vPx"]]
vP_y = data[:, jmap["vPy"]]
vP_z = data[:, jmap["vPz"]]
vP = np.array([[vP_x[i], vP_y[i], vP_z[i]] for i in range(len(t))])

# velocity point Q
vQ_x = data[:, jmap["vQx"]]
vQ_y = data[:, jmap["vQy"]]
vQ_z = data[:, jmap["vQz"]]
vQ = np.array([[vQ_x[i], vQ_y[i], vQ_z[i]] for i in range(len(t))])

# velocity point R
vR_x = data[:, jmap["vRx"]]
vR_y = data[:, jmap["vRy"]]
vR_z = data[:, jmap["vRz"]]
vR = np.array([[vR_x[i], vR_y[i], vR_z[i]] for i in range(len(t))])

# tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR, args.verbose)
tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR)

omega = np.transpose(tpav_object.angular_velocity())  # [omega_x, omega_y, omega_z]

np.savetxt(
    file_output,
    np.transpose([t, omega[0], omega[1], omega[2]]),
    delimiter=",",
    header="time (s), omega_x (rad/s), omega_y (rad/s), omega_z (rad/s)",
)

if args.verbose:
    print("Three points angular velocity (tpav) client end.")
    print("------------------------------------------------")
