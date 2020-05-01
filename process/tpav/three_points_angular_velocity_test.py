#!/usr/bin/env python
import unittest

import numpy as np
import os

import three_points_angular_velocity as tpav


class ThreePointsAngularVelocityTest(unittest.TestCase):
    """
    This is the unit test of the three_points_angular_velocity.py script.
    To run this test on the command line:
    $ python -m unittest -v three_points_angular_velocity_test.py

    To run a single test:
    $ python three_points_angular_velocity_test.py ThreePointsAngularVelocityTest.test_t0
    """
    def __init__(self, *args, **kwargs):
        super(ThreePointsAngularVelocityTest, self).__init__(*args, **kwargs)
        self.tolerance = 1.0e-6  # small tolerance
        self.seed = 1  # make the random seed specific here so it is repeatable
        self.nsd = 3  # number of space dimensions
        self.nts = 1  # number of time steps
        self.verbose = 0  # 0 for terse, 1 for debug

    def test_t0(self):
        """
        This function tests a single time step input.
        """
        np.random.seed(self.seed)  # repeatability from specific random seed

        # known test case values
        rOP_known = [[1.62434536, -0.61175641, -0.52817175]]
        rOQ_known = [[0.55137674, 0.25365122, -2.82971045]]
        rOR_known = [[3.36915713, -1.37296331, -0.20913266]]
        rPQ_known = [[-1.07296862, 0.86540763, -2.3015387]]
        rPR_known = [[ 1.74481176, -0.7612069, 0.3190391]]
        vP_known = [[-0.24937038, 1.46210794, -2.06014071]]
        vQ_known = [[-0.34662714, -0.49644677, -2.75124129]]
        vR_known = [[0.49113439, 3.54318589, -1.14461195]]
        A_known =  np.array([[[0.0, -2.3015387, -0.86540763],
                              [2.3015387, 0.0, -1.07296862],
                              [0.86540763, 1.07296862, 0.0],
                              [0.0, 0.3190391, 0.7612069],
                              [-0.3190391, 0.0, 1.74481176],
                              [-0.7612069, -1.74481176, 0.0]]])
        w_known = np.array([[-0.3224172, -0.38405435, 1.13376944]])

        if self.verbose:
            print(f'A_known = {A_known}')
            print(f'w_known = {w_known}')

        # position vectors, seeded
        rOP = np.random.randn(self.nts, self.nsd)  # arbitrary position vector from origin to P
        rPQ = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to Q
        rPR = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to R

        # position vectors, derived
        rOQ = rOP + rPQ  # position vector from origin to Q in frame F
        rOR = rOP + rPR  # position vector from origin to R in frame F

        # velocity vectors, seeded
        vP = np.random.randn(self.nts, self.nsd)  # arbitrary velocity vector of point P in frame F
        wB = np.random.randn(self.nts, self.nsd)  # angular velocity vector of body B in frame F

        # velocity vectors, derived
        vQ = vP + np.cross(wB, rPQ)
        vR = vP + np.cross(wB, rPR)

        p = tpav.ThreePointsAngularVelocity(rOP, rOQ, rOR, vP, vQ, vR, self.verbose)

        A_calculated = p.A_matrix()
        if self.verbose:
            print(f'A_calculated = {A_calculated}')

        # w_calculated_T = np.squeeze(np.reshape(p.angular_velocity(), (nts, nsd)))
        w_calculated_T = p.angular_velocity()
        if self.verbose:
            print(f'w_calculated_T = {w_calculated_T}')

        self.assertEqual(self.seed, 1, msg='Set to 1 for test repeatibility.')
        self.assertLess(np.linalg.norm(rOP - rOP_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOQ - rOQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOR - rOR_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPQ - rPQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPR - rPR_known), self.tolerance)
        self.assertLess(np.linalg.norm(vP - vP_known), self.tolerance)
        self.assertLess(np.linalg.norm(vQ - vQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(vR - vR_known), self.tolerance)
        self.assertLess(np.linalg.norm(A_known - A_calculated), self.tolerance)
        self.assertLess(np.linalg.norm(w_known - w_calculated_T), self.tolerance)

    def test_t0_t1(self):
        """
        This function tests a double time step input.
        """
        np.random.seed(self.seed)  # repeatability from specific random seed

        # known test case values
        rOP_known = [[1.62434536, -0.61175641, -0.52817175],
                     [1.62434536, -0.61175641, -0.52817175]]

        rOQ_known = [[0.55137674, 0.25365122, -2.82971045],
                     [0.55137674, 0.25365122, -2.82971045]]

        rOR_known = [[3.36915713, -1.37296331, -0.20913266],
                     [3.36915713, -1.37296331, -0.20913266]]

        rPQ_known = [[-1.07296862, 0.86540763, -2.3015387],
                     [-1.07296862, 0.86540763, -2.3015387]]

        rPR_known = [[ 1.74481176, -0.7612069, 0.3190391],
                     [ 1.74481176, -0.7612069, 0.3190391]]

        vP_known = [[-0.24937038, 1.46210794, -2.06014071],
                    [-0.24937038, 1.46210794, -2.06014071]]

        vQ_known = [[-0.34662714, -0.49644677, -2.75124129],
                    [-0.34662714, -0.49644677, -2.75124129]]

        vR_known = [[0.49113439, 3.54318589, -1.14461195],
                    [0.49113439, 3.54318589, -1.14461195]]

        A_known =  np.array([[[0.0, -2.3015387, -0.86540763],
                              [2.3015387, 0.0, -1.07296862],
                              [0.86540763, 1.07296862, 0.0],
                              [0.0, 0.3190391, 0.7612069],
                              [-0.3190391, 0.0, 1.74481176],
                              [-0.7612069, -1.74481176, 0.0]],
                             [[0.0, -2.3015387, -0.86540763],
                              [2.3015387, 0.0, -1.07296862],
                              [0.86540763, 1.07296862, 0.0],
                              [0.0, 0.3190391, 0.7612069],
                              [-0.3190391, 0.0, 1.74481176],
                              [-0.7612069, -1.74481176, 0.0]]])

        w_known = np.array([[-0.3224172, -0.38405435, 1.13376944],
                            [-0.3224172, -0.38405435, 1.13376944]])

        if self.verbose:
            print(f'A_known = {A_known}')
            print(f'w_known = {w_known}')

        # position vectors, seeded
        rOP = np.random.randn(self.nts, self.nsd) # arbitrary position vector from origin to P

        rPQ = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to Q
        rPR = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to R

        # position vectors, derived
        rOQ = rOP + rPQ  # position vector from origin to Q in frame F
        rOR = rOP + rPR  # position vector from origin to R in frame F

        # velocity vectors, seeded
        vP = np.random.randn(self.nts, self.nsd)  # arbitrary velocity vector of point P in frame F
        wB = np.random.randn(self.nts, self.nsd)  # angular velocity vector of body B in frame F

        # velocity vectors, derived
        vQ = vP + np.cross(wB, rPQ)
        vR = vP + np.cross(wB, rPR)

        # convert from numpy arrays to lists
        rOP = np.array([rOP.tolist()[0], rOP.tolist()[0]])
        rPQ = np.array([rPQ.tolist()[0], rPQ.tolist()[0]])
        rPR = np.array([rPR.tolist()[0], rPR.tolist()[0]])
        rOQ = np.array([rOQ.tolist()[0], rOQ.tolist()[0]])
        rOR = np.array([rOR.tolist()[0], rOR.tolist()[0]])
        vP = np.array([vP.tolist()[0], vP.tolist()[0]])
        wB = np.array([wB.tolist()[0], wB.tolist()[0]])
        vQ = np.array([vQ.tolist()[0], vQ.tolist()[0]])
        vR = np.array([vR.tolist()[0], vR.tolist()[0]])

        if self.verbose:
            print(f'rOP = {rOP}')
            print(f'rPQ = {rPQ}')
            print(f'rPR = {rPR}')
            print(f'rOQ = {rOQ}')
            print(f'rOR = {rOR}')
            print(f'vP = {vP}')
            print(f'wB = {wB}')
            print(f'vQ = {vQ}')
            print(f'vR = {vR}')

        p = tpav.ThreePointsAngularVelocity(rOP, rOQ, rOR, vP, vQ, vR, self.verbose)

        A_calculated = p.A_matrix()
        if self.verbose:
            print(f'A_calculated = {A_calculated}')

        # w_calculated_T = np.squeeze(np.reshape(p.angular_velocity(), (nts, nsd)))
        w_calculated_T = p.angular_velocity()
        if self.verbose:
            print(f'w_calculated_T = {w_calculated_T}')

        self.assertEqual(self.seed, 1, msg='Set to 1 for test repeatibility.')
        self.assertLess(np.linalg.norm(rOP - rOP_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOQ - rOQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOR - rOR_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPQ - rPQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPR - rPR_known), self.tolerance)
        self.assertLess(np.linalg.norm(vP - vP_known), self.tolerance)
        self.assertLess(np.linalg.norm(vQ - vQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(vR - vR_known), self.tolerance)
        self.assertLess(np.linalg.norm(A_known - A_calculated), self.tolerance)
        self.assertLess(np.linalg.norm(w_known - w_calculated_T), self.tolerance)

    # def test_pendulum(self):
    #     subdirectory_found = False
    #     try:
    #         input_folder = 'simo'
    #         input_full = os.path.join(os.getcwd(), input_folder)
    #         if self.verbose:
    #             print('Searching for directory:')
    #             print(input_full)
    #         os.chdir(input_full)
    #         subdirectory_found = True
    #         os.chdir('../')
    #         # to finish

    #     except OSError:
    #         print('Error: directory not found.')

    #     self.assertEqual(subdirectory_found, True, msg='Directory not found.')

    def test_t0_insufficient_rank_omega_perpendicular(self):

        """
        This function tests a single time step input with a rank-insufficient
        configuration space (rOR gets set to rOQ, which fails to span R3).
        """
        np.random.seed(self.seed)  # repeatability from specific random seed

        # known test case values
        R = 10 # m
        rOP_known = [[R, 0, 0]]
        rOQ_known = [[R/np.sqrt(2), R/np.sqrt(2), 0]]
        rOR_known = rOQ_known
        rPQ_known = [[R/np.sqrt(2) - R, R/np.sqrt(2), 0]]
        rPR_known =  rPQ_known

        v_mag = 120 # m/s
        vP_known = [[0, v_mag, 0]]
        vQ_known = [[0, -v_mag/np.sqrt(2), v_mag/np.sqrt(2)]] 
        vR_known =  vQ_known

        A_known = np.array([[[0.0, -2.3015387, -0.86540763],
                              [2.3015387, 0.0, -1.07296862],
                              [0.86540763, 1.07296862, 0.0],
                              [0.0, 0.3190391, 0.7612069],
                              [-0.3190391, 0.0, 1.74481176],
                              [-0.7612069, -1.74481176, 0.0]]])

        w_known = np.array([[0, 0, 12]])

        if self.verbose:
            print(f'A_known = {A_known}')
            print(f'w_known = {w_known}')

        # position vectors, seeded
        rOP = np.array(rOP_known)
        print(f'rOP = {rOP}')
        rPQ = np.array(rPQ_known)
        print(f'rPQ = {rPQ}')
        # rPR = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to R
        rPR = rPQ

        # position vectors, derived
        rOQ = np.array(rOP) + rPQ  # position vector from origin to Q in frame F
        rOR = np.array(rOP + rPR)  # position vector from origin to R in frame F

        # velocity vectors, seeded
        vP = np.array(vP_known)
        wB = w_known  # angular velocity vector of body B in frame F

        # velocity vectors, derived
        vQ = vP + np.cross(wB, rPQ)
        vR = vP + np.cross(wB, rPR)

        self.verbose = 0  # manually turn on/off verbosity here
        p = tpav.ThreePointsAngularVelocity(rOP, rOQ, rOR, vP, vQ, vR, self.verbose)

        A_calculated = p.A_matrix()
        if self.verbose:
            print(f'A_calculated = {A_calculated}')

        # w_calculated_T = np.squeeze(np.reshape(p.angular_velocity(), (nts, nsd)))
        w_calculated_T = p.angular_velocity()
        if self.verbose:
            print(f'w_calculated_T = {w_calculated_T}')

        self.assertEqual(self.seed, 1, msg='Set to 1 for test repeatibility.')
        self.assertLess(np.linalg.norm(rOP - rOP_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOQ - rOQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOR - rOR_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPQ - rPQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPR - rPR_known), self.tolerance)
        self.assertLess(np.linalg.norm(vP - vP_known), self.tolerance)
        self.assertLess(np.linalg.norm(vQ - vQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(vR - vR_known), self.tolerance)
        self.assertLess(np.linalg.norm(A_known - A_calculated), self.tolerance)
        self.assertLess(np.linalg.norm(w_known - w_calculated_T), self.tolerance)

    def test_t0_insufficient_rank_omega_parallel(self):

        """
        This function tests a single time step input with a rank-insufficient
        configuration space (rOR gets set to rOQ, which fails to span R3).
        """
        np.random.seed(self.seed)  # repeatability from specific random seed

        # known test case values
        R = 10 # m
        rOP_known = [[R, 0, 0]]
        rOQ_known = [[R, 0, R]]
        rOR_known = rOQ_known
        rPQ_known = [[0, 0, R]]
        rPR_known =  rPQ_known

        v_mag = 120 # m/s
        vP_known = [[0, v_mag, 0]]
        vQ_known = [[0, v_mag, 0]] 
        vR_known =  vQ_known

        A_known = np.array([[[0.0, -2.3015387, -0.86540763],
                              [2.3015387, 0.0, -1.07296862],
                              [0.86540763, 1.07296862, 0.0],
                              [0.0, 0.3190391, 0.7612069],
                              [-0.3190391, 0.0, 1.74481176],
                              [-0.7612069, -1.74481176, 0.0]]])

        w_known = np.array([[0, 0, 12]])

        if self.verbose:
            print(f'A_known = {A_known}')
            print(f'w_known = {w_known}')

        # position vectors, seeded
        rOP = np.array(rOP_known)
        print(f'rOP = {rOP}')
        rPQ = np.array(rPQ_known)
        print(f'rPQ = {rPQ}')
        # rPR = np.random.randn(self.nts, self.nsd)  # position vector in body B from P to R
        rPR = rPQ

        # position vectors, derived
        rOQ = np.array(rOP) + rPQ  # position vector from origin to Q in frame F
        rOR = np.array(rOP + rPR)  # position vector from origin to R in frame F

        # velocity vectors, seeded
        vP = np.array(vP_known)
        wB = w_known  # angular velocity vector of body B in frame F

        # velocity vectors, derived
        vQ = vP + np.cross(wB, rPQ)
        vR = vP + np.cross(wB, rPR)

        self.verbose = 1  # manually turn on/off verbosity here
        p = tpav.ThreePointsAngularVelocity(rOP, rOQ, rOR, vP, vQ, vR, self.verbose)

        A_calculated = p.A_matrix()
        if self.verbose:
            print(f'A_calculated = {A_calculated}')

        # w_calculated_T = np.squeeze(np.reshape(p.angular_velocity(), (nts, nsd)))
        w_calculated_T = p.angular_velocity()
        if self.verbose:
            print(f'w_calculated_T = {w_calculated_T}')

        self.assertEqual(self.seed, 1, msg='Set to 1 for test repeatibility.')
        self.assertLess(np.linalg.norm(rOP - rOP_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOQ - rOQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rOR - rOR_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPQ - rPQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(rPR - rPR_known), self.tolerance)
        self.assertLess(np.linalg.norm(vP - vP_known), self.tolerance)
        self.assertLess(np.linalg.norm(vQ - vQ_known), self.tolerance)
        self.assertLess(np.linalg.norm(vR - vR_known), self.tolerance)
        self.assertLess(np.linalg.norm(A_known - A_calculated), self.tolerance)
        self.assertLess(np.linalg.norm(w_known - w_calculated_T), self.tolerance)



if __name__ == '__main__':
    unittest.main()
