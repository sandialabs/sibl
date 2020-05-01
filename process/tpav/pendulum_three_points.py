#!/usr/bin/env python
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy.integrate import odeint
import csv  # comma separated value

# sys.path.append(os.path.abspath('../'))  # look in parent directory for three_point_angular_velocity server
import three_points_angular_velocity as tpav

# User input begin
save_figure = 1  # 0 or 1
pdf_format = 1  # 0 for .svg format, 1 for .pdf format
# User input end

# plot the angular velocity jfrom the gold standard

n_header_rows = 1  # number of rows that compose the header, skip when reading

data = np.genfromtxt('simo.csv', dtype='float', delimiter=',', skip_header=n_header_rows)

time = data[:, 0]  # column 1
q = data[:, 1]  # column 2
qdot = data[:, 2]  # column 3
x_tip = np.sin(q)  # x-position of the tip
y_tip = -1.0*np.cos(q)  # y-position of the tip

fig = plt.figure(figsize=(16, 8))
fig.suptitle('Rigid Reference')

ax11 = fig.add_subplot(2, 2, 1)
ax11.plot(time, q)
ax11.grid()
ax11.set_xlabel('time (s)')
ax11.set_ylabel('angle (radians)')

ax12 = fig.add_subplot(2, 2, 2)
ax12.plot(time, x_tip)
ax12.grid()
ax12.set_xlabel('time (s)')
ax12.set_ylabel('tip x-position (m)')

ax21 = fig.add_subplot(2, 2, 3)
ax21.plot(time, qdot)
ax21.grid()
ax21.set_xlabel('time (s)')
ax21.set_ylabel('angular velocity (rad/s)')

ax22 = fig.add_subplot(2, 2, 4)
ax22.plot(time, y_tip)
ax22.grid()
ax22.set_xlabel('time (s)')
ax22.set_ylabel('tip y-position (m)')

plt.show()

if save_figure:
    title_string = 'rigid_reference'
    script_path = os.getcwd()
    if pdf_format:
        figure_string = title_string + '.pdf'
    else:
        figure_string = title_string + '.svg'
    fig.savefig(figure_string, dpi=300)
    print('Saved figure to ' + os.path.join(script_path, figure_string))


# plot the angular velocity from the three points algorithm

n_header_rows = 3  # number of rows that compose the header, skip when reading

data = np.genfromtxt('history.csv', dtype='float', delimiter=',', skip_header=n_header_rows)

t_ssm = data[:, 0]  # column 1, from Sierra Solid Mechanics (SSM)

rtip_x = data[:, 25]
rtip_y = data[:, 26]

rOP_x = data[:, 37]
rOP_y = data[:, 38]
rOP_z = data[:, 39]

rOP = np.array([[rOP_x[i], rOP_y[i], rOP_z[i]] for i in range(len(t_ssm))])

vP_x = data[:, 43]
vP_y = data[:, 44]
vP_z = data[:, 45]

vP = np.array([[vP_x[i], vP_y[i], vP_z[i]] for i in range(len(t_ssm))])

rOQ_x = data[:, 49]
rOQ_y = data[:, 50]
rOQ_z = data[:, 51]

rOQ = np.array([[rOQ_x[i], rOQ_y[i], rOQ_z[i]] for i in range(len(t_ssm))])

vQ_x = data[:, 55]
vQ_y = data[:, 56]
vQ_z = data[:, 57]

vQ = np.array([[vQ_x[i], vQ_y[i], vQ_z[i]] for i in range(len(t_ssm))])

rOR_x = data[:, 61]
rOR_y = data[:, 62]
rOR_z = data[:, 63]

rOR = np.array([[rOR_x[i], rOR_y[i], rOR_z[i]] for i in range(len(t_ssm))])

vR_x = data[:, 67]
vR_y = data[:, 68]
vR_z = data[:, 69]

vR = np.array([[vR_x[i], vR_y[i], vR_z[i]] for i in range(len(t_ssm))])

verbose = 0
p = tpav.ThreePointsAngularVelocity(rOP, rOQ, rOR, vP, vQ, vR, verbose)

wB = p.angular_velocity()  # angular velocity of deformable pendulum
wB_z = [i[2] for i in wB]  # third column of angular velocity vector

fig = plt.figure(figsize=(16, 8))
fig.suptitle('Rigid Reference vs. Deformable Three-Point Algorithm (TPA)')

label_standard = 'rigid reference'
label_three_point = 'deformable TPA'

ax11 = fig.add_subplot(2, 2, 1)
ax11.plot(time, q, label=label_standard)
ax11.grid()
ax11.legend()
ax11.set_xlabel('time (s)')
ax11.set_ylabel('angle (radians)')

ax12 = fig.add_subplot(2, 2, 2)
ax12.plot(time, x_tip, label=label_standard)
ax12.plot(t_ssm, rtip_x, '-.', label=label_three_point)
ax12.grid()
ax12.legend()
ax12.set_xlabel('time (s)')
ax12.set_ylabel('tip x-position (m)')

ax21 = fig.add_subplot(2, 2, 3)
ax21.plot(time, qdot, label=label_standard)
ax21.plot(t_ssm, wB_z, label=label_three_point)
ax21.grid()
ax21.legend()
ax21.set_xlabel('time (s)')
ax21.set_ylabel('angular velocity (rad/s)')

ax22 = fig.add_subplot(2, 2, 4)
ax22.plot(time, y_tip, label=label_standard)
ax22.plot(t_ssm, rtip_y, '-.', label=label_three_point)
ax22.grid()
ax22.legend()
ax22.set_xlabel('time (s)')
ax22.set_ylabel('tip y-position (m)')

plt.show()

if save_figure:
    title_string = 'rigid_reference_vs_three_point_algorithm'
    script_path = os.getcwd()
    if pdf_format:
        figure_string = title_string + '.pdf'
    else:
        figure_string = title_string + '.svg'
    fig.savefig(figure_string, dpi=300)
    print('Saved figure to ' + os.path.join(script_path, figure_string))
