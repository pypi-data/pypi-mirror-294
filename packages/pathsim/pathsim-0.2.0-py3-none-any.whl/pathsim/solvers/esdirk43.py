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

class ESDIRK43(ImplicitSolver):
    """
    6 stage 4-th order ESDIRK method with embedded 3-rd order method for stepsize control. 
    The first stage is explicit, followed by 5 implicit stages.
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
        self.eval_stages = [0.0, 1/2, (2-np.sqrt(2))/4, 2012122486997/3467029789466, 1.0, 1.0]

        #butcher table
        self.BT = {0:[0.0],
                   1:[1/4, 1/4],
                   2:[-1356991263433/26208533697614, -1356991263433/26208533697614, 1/4],
                   3:[-1778551891173/14697912885533, -1778551891173/14697912885533, 
                      7325038566068/12797657924939, 1/4],
                   4:[-24076725932807/39344244018142, -24076725932807/39344244018142, 
                      9344023789330/6876721947151, 11302510524611/18374767399840, 1/4],
                   5:[657241292721/9909463049845, 657241292721/9909463049845, 
                      1290772910128/5804808736437, 1103522341516/2197678446715, -3/28, 1/4]}

        #coefficients for truncation error estimate
        self.A1 = [657241292721/9909463049845, 657241292721/9909463049845, 
                   1290772910128/5804808736437, 1103522341516/2197678446715, -3/28, 1/4]
        self.A2 = [-71925161075/3900939759889, -71925161075/3900939759889, 
                   2973346383745/8160025745289, 3972464885073/7694851252693, 
                   -263368882881/4213126269514, 3295468053953/15064441987965]
        self.TR = [a1 - a2 for a1, a2 in zip(self.A1, self.A2)]


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
        
        #compute error ratio and success
        error_ratio = self.tolerance_lte / truncation_error
        success = error_ratio >= 1.0

        #compute timestep scale
        timestep_rescale = 0.9 * (error_ratio)**(1/4)        

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
        if self.stage < 5:
            self.stage += 1
            return True, 0.0, 1.0
        else: 
            self.stage = 0
            return self.error_controller(dt)