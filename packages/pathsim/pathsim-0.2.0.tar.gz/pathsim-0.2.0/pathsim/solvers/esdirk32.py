########################################################################################
##
##                   EMBEDDED DIAGONALLY IMPLICIT RUNGE KUTTA METHOD
##                                (solvers/esdirk32.py)
##
##                                  Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import numpy as np

from ._solver import ImplicitSolver
from ..utils.funcs import numerical_jacobian


# SOLVERS ==============================================================================

class ESDIRK32(ImplicitSolver):
    """
    Williams et.al constructed an ESDIRK method of order 3 with four stages.
    This method is constructed such that it is applicable to index-2 
    differential algebraic systems.
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
        self.eval_stages = [0.0, 1.0, 3/2, 1.0]

        #butcher table
        self.BT = {0:[0.0],
                   1:[1/2, 1/2],
                   2:[5/8, 3/8, 1/2],
                   3:[7/18, 1/3, -2/9, 1/2]}

        #coefficients for truncation error estimate
        self.TR = [-1/9, -1/6, -2/9, 1/2]


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
        timestep_rescale = 0.9 * (error_ratio)**(1/3)        

        return success, truncation_error, timestep_rescale



    def solve(self, u, t, dt):
        """
        Solves the implicit update equation via anderson acceleration.
        """

        #first stage is explicit
        if self.stage == 0:
            return 0.0
            
        #update timestep weighted slope 
        self.Ks[self.stage] = self.func(self.x, u, t)

        #update fixed-point equation
        slope = 0.0
        for i, b in enumerate(self.BT[self.stage]):
            slope += self.Ks[i] * b

        #use the jacobian
        if self.jac is not None:

            #compute jacobian of fixed-point equation
            jac_g = dt * b * self.jac(self.x, u, t)

            #anderson acceleration step with local newton
            self.x, err = self.acc.step(self.x, dt*slope + self.x_0, jac_g)

        else:
            #anderson acceleration step (pure)
            self.x, err = self.acc.step(self.x, dt*slope + self.x_0, None)

        #return the fixed-point residual
        return err


    def step(self, u, t, dt):
        """
        performs the timestep update
        """

        #first stage is explicit
        if self.stage == 0:
            self.Ks[self.stage] = self.func(self.x, u, t)

        #restart anderson accelerator 
        self.acc.reset()

        #error and step size control
        if self.stage < 3:
            self.stage += 1
            return True, 0.0, 1.0
        else: 
            self.stage = 0
            return self.error_controller(dt)