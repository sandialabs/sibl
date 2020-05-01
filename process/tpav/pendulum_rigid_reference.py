#!/usr/bin/env python
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import rc
from scipy.integrate import odeint
import csv  # comma separated value
# import scipy.special as sp

# References:
# https://en.wikipedia.org/wiki/Pendulum_(mathematics) 
# https://kitchingroup.cheme.cmu.edu/pycse/pycse.html
# Section 10.1.16 Phase portraits of a system of ODEs, and
# http://matlab.cheme.cmu.edu/2011/08/09/phase-portraits-of-a-system-of-odes/
# http://www.motiongenesis.com/MGWebSite/MGGetStarted/MGExamplePendulum/MGExamplePendulumSingle.html
# http://www.motiongenesis.com/MGWebSite/MGGetStarted/MGExamplePendulum/RigidBodyPendulumInstructor.pdf
# https://en.wikipedia.org/wiki/List_of_moments_of_inertia
# http://www-users.math.umd.edu/~petersd/246/matlabode2.html

# User input begin
kitchin_example = 0  # 0 or 1, toggle online versus actual problem of interest
save_figure = 0  # 0 or 1
pdf_format = 1  # 0 for .svg format, 1 for .pdf format
write_data_file = 0  # 0 or 1
LATEX = 1  # 0 or 1
# User input end

if LATEX:
  rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
  rc('text', usetex=True)

# Algorithm
#fig, ax = plt.subplots(figsize=fig_size)
fig, ax = plt.subplots()

if kitchin_example:
    title_string = 'kitchin'
    G = 2.0  # so K=1, below
    L = 3.0  # so K=1, below
    q_min = -2.0
    q_max = 8.0
    qdot_min = -2.0
    qdot_max = 2.0 
    plt.xlim([q_min, q_max])
    plt.ylim([-4.0, 4.0])  # bigger than [qdot_min, qdot_max], plot example 1
    # plt.ylim([-1.5, 2.5])  # bigger than [qdot_min, qdot_max], plot example 2
    tspan = np.linspace(0.0, 5.0, 40)
    y0 = [0.0, 1.0]  # [q0, qdot0] initial conditions
    fig_size = (8, 8)

else:
    title_string = 'simo'
    G = 9.81  # m/s^2
    L = 1.0  # m
    q_min = -2 # -np.pi
    q_max = 8 # 3*np.pi
    qdot_min = -20.0
    qdot_max = -1.0*qdot_min
    plt.xlim([q_min, q_max])
    plt.ylim([1.8 * qdot_min, 1.8 * qdot_max])
    # tspan = np.linspace(0.0, 2.0, 40)
    tspan = np.linspace(0.0, 2.0, 200)
    y0 = [np.pi/2.0, 0.0]  # [q0, qdot0] initial conditions
    fig_size = 2.5 * np.array([4, 3])  # (horizontal, vertical)

fig.set_size_inches(fig_size[0], fig_size[1])


K = np.sqrt((3*G)/(2*L))  # used as a global variable (yuck!)

n_q_points = 20
n_qdot_points = 20


# governing second-order nonlinear ODE
# ddot(q) + k^2 sin(q) = 0, where k = sqrt((3*g)/(2*L))

# solve with systems of first-order nonlinear ODEs
# y1 = q
# y2 = dot(y1)
#
# then
# dot(y1) = y2
# dot(y2) = -k^2 sin(y1)
#
# let Y = <y1, y2>^T
#

def f(Y, t):
    # ugly but I think necessary to use scipy odeint:
    # t is unused variable in the implementation, and
    # K is a global variable (yuck!)
    y1, y2, = Y  # unpack vector tuple
    return [y2, -K*K*np.sin(y1)]

# POINTS_Y1 = np.linspace(-2.0, 8.0, 20)  # rotation q
POINTS_Y1 = np.linspace(q_min, q_max, n_q_points)  # rotation q
# POINTS_Y2 = np.linspace(-2.0, 2.0, 20)  # rotation rate dot(q)
# POINTS_Y2 = np.linspace(-5.0, 5.0, 20)  # rotation rate dot(q)
POINTS_Y2 = np.linspace(qdot_min, qdot_max, n_qdot_points)  # rotation rate dot(q)

Y1, Y2 = np.meshgrid(POINTS_Y1, POINTS_Y2)

t=0  # required to get scipy odeint to work

u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

NI, NJ = Y1.shape

for i in range(NI):
    for j in range(NJ):
        x = Y1[i, j]
        y = Y2[i, j]
        yprime = f([x, y], t)
        u[i, j] = yprime[0]
        v[i, j] = yprime[1]

Q = plt.quiver(Y1, Y2, u, v, color='r')

# overlay a trajectory
# tspan = np.linspace(0.0, 1.5, 20)
# y0 = [np.pi/2.0, 0.0]  # q0, qdot0
ys = odeint(f, y0, tspan)
plt.plot(ys[:, 0], ys[:, 1], 'b-')  # path, blue line
plt.plot([ys[0, 0]], [ys[0, 1]], 'go')  # start of path, green circle
plt.plot([ys[-1, 0]], [ys[-1, 1]], 'ks')  # end of path, black square

# ax.set_aspect(1.0)
# ax.xaxis.set_major_formatter(FormatStrFormatter('%g $\pi$'))
ax.xaxis.set_major_locator(MultipleLocator(base=np.pi))
plt.xlabel(r'rotation $q = y_1$ (rad)')
plt.ylabel(r'angular velocity $\dot{q} = y_2$ (rad/s)')
# plt.title(title_string)
plt.show()

if save_figure:
    script_path = os.getcwd()
    if pdf_format:
        figure_string = title_string + '.pdf'
    else:
        figure_string = title_string + '.svg'
    fig.savefig(figure_string, dpi=300)
    print('Saved figure to ' + os.path.join(script_path, figure_string))

if write_data_file:
    script_path = os.getcwd()
    file_string = title_string + '.csv'
    with open(file_string, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['time', 'q', 'qdot'])
        for i in range(len(tspan)):
            writer.writerow([tspan[i], ys[i, 0], ys[i, 1]])
    print('Wrote tabular data to ' + os.path.join(script_path, file_string))

# t = np.linspace(0.0, 2.0*3.14159, 10)
# y = np.sin(t)
# sn_index = 0
# ye = sp.ellipj(t, 1.0/(np.sqrt(2.0)))[sn_index]
# 
# fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(2, 1, 1, aspect=1)
# 
# ax.grid(linestyle='--', linewidth=0.5, color='0.25', zorder=-10)
# 
# ax.plot(t, y)
# ax.plot(t, ye)
# 
# # second axis
# L = 1.0
# g = 9.81
# 
# 
# t2 = np.linspace(0.0, 2.0, 10)
# 
# sn_kernel = sp.ellipj(t2*np.sqrt(3*g/(2*L)), 1.0/(np.sqrt(2.0)))[sn_index]
# 
# y_position = 1.0*
# theta = 2.0*np.arcsin(1.0/(np.sqrt(2.0) * sn_kernel))
# x_position = 1.0*np.cos(theta)
# 
# ax2 = fig.add_subplot(2, 1, 2)
# ax2.plot(t2, x_position)
# 
# ax2.grid(linestyle='--', linewidth=0.5, color='0.25', zorder=-10)
# 
# plt.show()
