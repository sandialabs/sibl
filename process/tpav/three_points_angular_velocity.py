#!/usr/bin/env python
import numpy as np
# import os
# import sys

def cross_matrix(vec):
    """
    This function computes the cross matrix to execute the cross product.
    """
    # return np.array([[0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0]])
    return np.array([[[0.0, -vec[i, 2], vec[i, 1]],
                      [vec[i, 2], 0.0, -vec[i, 0]],
                      [-vec[i, 1], vec[i, 0], 0.0]]
                     for i in range(len(vec))])

class ThreePointsAngularVelocity:
    """
    Given a time-series of three points' current position and velocity,
    both three-dimensional, calculates the rigid body angular velocity
    using a least-squares methodology.

    : params :
        : rP    Position vector to point P, shape (m, 3) in E3 as (x, y, z).
        : rQ    Position vector to point Q, same shape as rP.
        : rR    Position vector to point R, same shape as rP.
                All position vectors measured from the origin O.
        : vP    Velocity vector of point P in inertial frame F, same shape as rP.
        : vQ    Velocity vector of point Q in inertial frame F, same shape as rQ.
        : vR    Velocity vector of point R in inertial frame F, same shape as rR.

    : returns :
        : wB    Angular velocity vector of rigid body B i frame F, with
                shape (m, 3).

    : reference :
        : Laflin, J. (2019) compute_omega_test.py.
    """

    def __init__(self, rP, rQ, rR, vP, vQ, vR, verbose=0):

        self.verbose = verbose

        if self.verbose:
            print('-------------------------------------------')
            print('Three Points Angular Velocity server start.')

        nts, _ = rP.shape  # number of time steps, number of space dimensions

        # position vector r from point P to point Q
        rPQ = rQ - rP

        # position vector r from point P to point R
        rPR = rR - rP


        # cross_rPQ = self.cross_matrix(rPQ)
        # cross_rPR = self.cross_matrix(rPR)
        cross_rPQ = cross_matrix(rPQ)
        cross_rPR = cross_matrix(rPR)

        # self.A = np.vstack((-cross_rPQ, -cross_rPR))
        self.A = [np.vstack((-cross_rPQ[i], -cross_rPR[i])).tolist() for i in range(nts)]

        # self.b = np.vstack(((vQ - vP).reshape(3, 1), (vR - vP).reshape(3, 1)))
        self.b = [np.vstack(((vQ[i] - vP[i]).reshape(3, 1), (vR[i] - vP[i]).reshape(3, 1))).tolist() for i in range(nts)]

        # self.wB = np.linalg.solve(np.transpose(self.A) @ self.A, np.transpose(self.A) @ self.b)
        # self.wB = [np.linalg.solve(np.transpose(self.A[i]) @ self.A[i], np.transpose(self.A[i]) @ self.b[i]) for i in range(nts)]
        self.wB = [np.linalg.solve(np.transpose(self.A[i]) @ self.A[i], np.transpose(self.A[i]) @ self.b[i]).tolist() for i in range(nts)]

        self.wB = [np.squeeze(np.reshape(self.wB[i], (1, 3))).tolist() for i in range(nts)]

        if self.verbose:
            print(f'rP = {rP}')
            print(f'rQ = {rQ}')
            print(f'rR = {rR}')
            print('')
            print(f'vP = {vP}')
            print(f'vQ = {vQ}')
            print(f'vR = {vR}')
            print('')
            print(f'rPQ = {rPQ}')
            print(f'rPR = {rPR}')
            print('')
            rPQ_length = [np.linalg.norm(rPQ[i]) for i in range(nts)]
            rPR_length = [np.linalg.norm(rPR[i]) for i in range(nts)]

            if rPQ_length[0] > 0 and rPR_length[0] > 0:
                rPQ_hat = [np.array(rPQ[i])/rPQ_length[i] for i in range(nts)]
                rPR_hat = [np.array(rPR[i])/rPR_length[i] for i in range(nts)]

                print(f'rPQ_hat = {rPQ_hat}')
                print(f'rPR_hat = {rPR_hat}')

                print('Dot product between unit vectors rPQ_hat and rPR_hat [0, 1]:')
                print('  0 is best, vectors are perpendicular, adds rank')
                print('  1 is worst, vectors are parallel, fails to add rank')

                dot_product = [np.dot(rPQ_hat[i], rPR_hat[i]) for i in range(nts)]
                print(f'  (rPQ_hat . rPR_hat) = {dot_product}')

            AtransposeA = [np.transpose(self.A[i]) @ self.A[i] for i in range(nts)]
            print('[A^T A] matrix =')
            print(f'{AtransposeA}')
            print('')

            rank = [np.linalg.matrix_rank(AtransposeA[i]) for i in range(nts)]
            print(f'Rank of [A^T A] matrix = {rank}')
            print('')

            print(f'A = {self.A}')
            print('')
            print(f'wB = {self.wB}')
            print('')
            print(f'b = {self.b}')
            print('')

            print('Three Points Angular Velocity server stop.')
            print('------------------------------------------')

#    def cross_matrix(self, vec):
#        """ 
#        This function computes the cross matrix to execute the cross product.
#        """
#        # return np.array([[0, -vec[2], vec[1]], [vec[2], 0, -vec[0]], [-vec[1], vec[0], 0]])
#        return np.array([[[0.0, -vec[i, 2], vec[i, 1]], 
#                          [vec[i, 2], 0.0, -vec[i,0]], 
#                          [-vec[i, 1], vec[i, 0], 0.0]] 
#                          for i in range(len(vec))])

    def angular_velocity(self):
        """
        Computes the estimates angular velocity of rigid body B in frame F.
        """
        if self.verbose:
            print(f'calculated angular velocity = {self.wB}')
        return self.wB

    def A_matrix(self):
        """
        Computes the least-squares matrix A, in A w = b, used to compute
        the angular velocity w.
        """
        return self.A

    def b_vector(self):
        """
        Computes the vector right-hand-side, in A w = b, used to compute
        the angular velocity w.
        """
        return self.b
