#!/usr/bin/env python
import os
import sys

import argparse
import json
import numpy as np

from process.tpav.three_points_angular_velocity import ThreePointsAngularVelocity as tpav

parser = argparse.ArgumentParser()
parser.add_argument("history", help="history is a '.csv' that contains the SSM tracer points output file")
parser.add_argument("history_to_tpav", help="history_to_tpav is a '.json' file that maps 'history.csv' to tpav API format [t, rPx, rPy, rPz, rQx, rQy, rQz, rRx, rRy, rRz, vPx, vPy, vPz, vQx, vQy, vQz, vRx, vRy, vRz], output angular velocity file is 'history_to_tpav.csv'")
parser.add_argument("--verbose", help="increased feedback in command line", action="store_true")
# parser.add_argument("skip_header_rows", type=int, help="number of header rows of file_input to skip")
args = parser.parse_args()

b = os.path.splitext(args.history_to_tpav)
file_output = b[0] + '.csv'

if args.verbose:
    print("--------------------------------------------------")
    print("Three points angular velocity (tpav) client begin.")
    print(f'  From path: {os.getcwd()}')
    print(f'  processing SSM tracer points output file: {args.history}')
    print(f'  with tpav point extraction file : {args.history_to_tpav}')
    print(f'  Output file: {file_output}')


with open(args.history_to_tpav) as fin:
    jmap = json.load(fin)

skip_header_rows = jmap["skip_rows"]

data =  np.genfromtxt(args.history, dtype='float', delimiter=',', skip_header=skip_header_rows)

# time
t = data[:, jmap["t"]]

# position point P
# rOP_x = data[:, 1]
# rOP_y = data[:, 2]
# rOP_z = data[:, 3]
rOP_x = data[:, jmap["rPx"]]
rOP_y = data[:, jmap["rPy"]]
rOP_z = data[:, jmap["rPz"]]
rOP = np.array([[rOP_x[i], rOP_y[i], rOP_z[i]] for i in range(len(t))])

# position point Q
# rOQ_x = data[:, 7]
# rOQ_y = data[:, 8]
# rOQ_z = data[:, 9]
rOQ_x = data[:, jmap["rQx"]]
rOQ_y = data[:, jmap["rQy"]]
rOQ_z = data[:, jmap["rQz"]]
rOQ = np.array([[rOQ_x[i], rOQ_y[i], rOQ_z[i]] for i in range(len(t))])

# position point R
# rOR_x = data[:, 13]
# rOR_y = data[:, 14]
# rOR_z = data[:, 15]
rOR_x = data[:, jmap["rRx"]]
rOR_y = data[:, jmap["rRy"]]
rOR_z = data[:, jmap["rRz"]]
rOR = np.array([[rOR_x[i], rOR_y[i], rOR_z[i]] for i in range(len(t))])

# velocity point P
# vP_x = data[:, 4]
# vP_y = data[:, 5]
# vP_z = data[:, 6]
vP_x = data[:, jmap["vPx"]]
vP_y = data[:, jmap["vPy"]]
vP_z = data[:, jmap["vPz"]]
vP = np.array([[vP_x[i], vP_y[i], vP_z[i]] for i in range(len(t))])

# velocity point Q
# vQ_x = data[:, 10]
# vQ_y = data[:, 11]
# vQ_z = data[:, 12]
vQ_x = data[:, jmap["vQx"]]
vQ_y = data[:, jmap["vQy"]]
vQ_z = data[:, jmap["vQz"]]
vQ = np.array([[vQ_x[i], vQ_y[i], vQ_z[i]] for i in range(len(t))])

# velocity point R
# jvR_x = data[:, 16]
# jvR_y = data[:, 17]
# _z = data[:, 18]
vR_x = data[:, jmap["vRx"]]
vR_y = data[:, jmap["vRy"]]
vR_z = data[:, jmap["vRz"]]
vR = np.array([[vR_x[i], vR_y[i], vR_z[i]] for i in range(len(t))])

# tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR, args.verbose)
tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR)

omega = np.transpose(tpav_object.angular_velocity()) # [omega_x, omega_y, omega_z]

# jwith open(file_string, 'w', newline='') as f:
# j    writer = csv.writer(f, delimiter=',')
# j    writer.writerow(['time (s)', 'q (rad)', 'qdot (rad/s)', 'tip_x=sin(q) (m)', 'tip_y=-cos(q) (m)'])
# j    for i in range(len(tspan)):
# j        writer.writerow([tspan[i], ys[i, 0], ys[i, 1], np.sin(ys[i, 0]), -1.0*np.cos(ys[i, 0])])
# ('Wrote tabular data to ' + os.path.join(script_path, file_string))

np.savetxt(file_output, np.transpose([t, omega[0], omega[1], omega[2]]), delimiter=',', header='time (s), omega_x (rad/s), omega_y (rad/s), omega_z (rad/s)')

if args.verbose:
    print("Three points angular velocity (tpav) client end.")
    print("------------------------------------------------")
