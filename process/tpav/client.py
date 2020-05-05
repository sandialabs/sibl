#!/usr/bin/env python
import os
import sys
import argparse

import numpy as np

from process.tpav.three_points_angular_velocity import ThreePointsAngularVelocity as tpav

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="increased feedback in command line", action="store_true")
parser.add_argument("file_input", help="t, rPx, rPy, rPz, vPx, vPy, vPz, rQx, rQy, rQz, vQx, vQy, vQz, rRx, rRy, rRz, vRx, vRy, vRz in .csv format")
parser.add_argument("skip_header_rows", type=int, help="number of header rows of file_input to skip")
args = parser.parse_args()

if args.verbose:
    print("--------------------------------------------------")
    print("Three points angular velocity (tpav) client begin.")
    print(f'  Processing input file: {args.file_input}')
    print(f'  located in path: {os.getcwd()}')

    b = os.path.splitext(args.file_input)
    file_output = b[0] + '_omega' + b[1]
    print(f'  Output file: {file_output}')

data =  np.genfromtxt(args.file_input, dtype='float', delimiter=',', skip_header=args.skip_header_rows)

# time
t = data[:, 0]

# point P position
rOP_x = data[:, 1]
rOP_y = data[:, 2]
rOP_z = data[:, 3]
rOP = np.array([[rOP_x[i], rOP_y[i], rOP_z[i]] for i in range(len(t))])

# point P velocity
vP_x = data[:, 4]
vP_y = data[:, 5]
vP_z = data[:, 6]
vP = np.array([[vP_x[i], vP_y[i], vP_z[i]] for i in range(len(t))])

# point Q position
rOQ_x = data[:, 7]
rOQ_y = data[:, 8]
rOQ_z = data[:, 9]
rOQ = np.array([[rOQ_x[i], rOQ_y[i], rOQ_z[i]] for i in range(len(t))])

# point Q velocity
vQ_x = data[:, 10]
vQ_y = data[:, 11]
vQ_z = data[:, 12]
vQ = np.array([[vQ_x[i], vQ_y[i], vQ_z[i]] for i in range(len(t))])

# point R position
rOR_x = data[:, 13]
rOR_y = data[:, 14]
rOR_z = data[:, 15]
rOR = np.array([[rOR_x[i], rOR_y[i], rOR_z[i]] for i in range(len(t))])

# point R velocity
vR_x = data[:, 16]
vR_y = data[:, 17]
vR_z = data[:, 18]
vR = np.array([[vR_x[i], vR_y[i], vR_z[i]] for i in range(len(t))])

# tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR, args.verbose)
tpav_object = tpav(rOP, rOQ, rOR, vP, vQ, vR)

omega = np.transpose(tpav_object.angular_velocity()) # [omega_x, omega_y, omega_z]

# if args.verbose:
#    print(f'Angular velocity = {omega}')

np.savetxt(file_output, np.transpose([t, omega[0], omega[1], omega[2]]), delimiter=',')


if args.verbose:
    print("Three points angular velocity (tpav) client end.")
    print("------------------------------------------------")
