########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkv65.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from ._solver import ExplicitSolver


# SOLVERS ==============================================================================

class RKV65(ExplicitSolver):
    """
    9-stage 6-th order with embedded 5-th order Runge-Kutta method from Verner 
    with 6-th order truncation error estimate.

    This is the 'most robust' 9, 6(5) pair of Jim Verner's Refuge for Runge-Kutta Pairs
    URL: https://www.sfu.ca/~jverner/
    """

    def __init__(self, initial_value=0, func=lambda x, u, t: u, jac=None, tolerance_lte=1e-6):
        super().__init__(initial_value, func, jac, tolerance_lte)

        #counter for runge kutta stages
        self.stage = 0

        #flag adaptive timestep solver
        self.is_adaptive = True

        #slope coefficients for stages
        self.Ks = {}

        #intermediate evaluation times
        self.eval_stages = [0.0, 9/50, 1/6, 1/4, 53/100, 3/5, 4/5, 1.0, 1.0]

        #extended butcher table 
        self.BT = {0:[             9/50],
                   1:[           29/324, 25/324],
                   2:[             1/16,      0,           3/16],
                   3:[     79129/250000,      0, -261237/250000,      19663/15625],
                   4:[  1336883/4909125,      0,   -25476/30875,    194159/185250,       8225/78546],
                   5:[-2459386/14727375,      0,    19504/30875, 2377474/13615875, -6157250/5773131,   902/735],
                   6:[        2699/7410,      0,      -252/1235, -1393253/3993990,     236875/72618,   -135/49,   15/22], 
                   7:[           11/144,      0,              0,          256/693,                0,   125/504, 125/528,        5/72], 
                   8:[           28/477,      0,              0,          212/441,   -312500/366177, 2125/1764,       0, -2105/35532, 2995/17766]}

        #5-th order solution at stage 9
        self.xh = None


    def error_controller(self, dt):
        """
        compute scaling factor for adaptive timestep 
        based on local truncation error estimate and returns both
        """
        if self.xh is None: 
            return True, 0.0, 1.0

        #compute and clip truncation error
        truncation_error = np.max(np.clip(abs(self.x-self.xh), 1e-18, None))
        
        #compute error ratio
        error_ratio = self.tolerance_lte / truncation_error
        success = error_ratio >= 1.0

        #compute timestep scale
        timestep_rescale = 0.9 * (error_ratio)**(1/6)        

        return success, truncation_error, timestep_rescale


    def step(self, u, t, dt):
        """
        performs the (explicit) timestep for (t+dt) 
        based on the state and input at (t)
        """

        #buffer intermediate slope
        self.Ks[self.stage] = self.func(self.x, u, t)
        
        #compute slope at stage
        slope = 0.0
        for i, b in enumerate(self.BT[self.stage]):
            slope += self.Ks[i] * b

        #error and step size control
        if self.stage < 8:
            #stepping with 6-th order solution
            self.x = dt * slope + self.x_0
            self.stage += 1
            return True, 0.0, 1.0
        else: 
            #save 5-th order solution for error control at last stage
            self.xh = dt * slope + self.x_0
            self.stage = 0
            return self.error_controller(dt)