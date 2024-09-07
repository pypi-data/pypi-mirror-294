########################################################################################
##
##                EXPLICIT ADAPTIVE TIMESTEPPING RUNGE-KUTTA INTEGRATORS
##                                 (solvers/rkf45.py)
##
##                                 Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from ._solver import ExplicitSolver


# SOLVERS ==============================================================================

class RKF45(ExplicitSolver):
    """
    6-stage 4-th order embedded Runge-Kutta-Fehlberg method 
    with 5-th order truncation error estimate that can be used to 
    adaptively control the timestep. 

    Absolute classic but relatively slow.
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
        self.eval_stages = [0.0, 1/4, 3/8, 12/13, 1, 1/2]

        #extended butcher table 
        self.BT = {0:[      1/4],
                   1:[     3/32,       9/32],
                   2:[1932/2197, -7200/2197,  7296/2197],
                   3:[  439/216,         -8,   3680/513, -845/4104],
                   4:[    -8/27,          2, -3554/2565, 1859/4104, -11/40],
                   5:[   25/216,          0,  1408/2565, 2197/4104,   -1/5, 0]}

        #coefficients for local truncation error estimate
        self.TR = [1/360, 0, -128/4275, -2197/75240, 1/50, 2/55]


    def error_controller(self, dt):
        """
        compute scaling factor for adaptive timestep 
        based on local truncation error estimate and returns both
        """
        if len(self.Ks)<len(self.TR): 
            return True, 0.0, 1.0

        #compute local truncation error slope
        slope = 0.0
        for i, b in enumerate(self.TR):
            slope += self.Ks[i] * b

        #compute and clip truncation error
        truncation_error = np.max(np.clip(abs(dt*slope), 1e-18, None))
        
        #compute error ratio
        error_ratio = self.tolerance_lte / truncation_error
        success = error_ratio >= 1.0

        #compute timestep scale
        timestep_rescale = 0.9 * (error_ratio)**(1/5)        

        return success, truncation_error, timestep_rescale


    def step(self, u, t, dt):
        """
        performs the (explicit) timestep for (t+dt) 
        based on the state and input at (t)
        """

        #buffer intermediate slope
        self.Ks[self.stage] = self.func(self.x, u, t)
        
        #update state at stage
        slope = 0.0
        for i, b in enumerate(self.BT[self.stage]):
            slope += self.Ks[i] * b
        self.x = dt * slope + self.x_0

        #error and step size control
        if self.stage < 5:
            self.stage += 1
            return True, 0.0, 1.0
        else: 
            self.stage = 0
            return self.error_controller(dt)