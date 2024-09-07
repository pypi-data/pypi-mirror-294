# mhd_massloss.py
#
# Author: Alice Somigliana
# Date : March 4th, 2022
#
# Computes the mass loss term in the MHD scenario.
################################################################################
from __future__ import print_function

import numpy as np
from .constants import *
from .disc import AccretionDisc
from .dust import Advection

class MHD_massloss():
    """
    Compute the mass loss term in the MHD disc winds + viscosity evolution equation (Tabone et al. 2021).

    args:

        alpha_DW:   alpha disc wind parameter (Tabone et al. 2021)
        leverarm:   lambda parameter (Tabone et al. 2021)
        xi:         xi parameter (Tabone et al. 2021)
    """

    def __init__(self, alpha_DW, leverarm, omega, xi, tacc0):

        self._alpha_DW = alpha_DW
        self._leverarm = leverarm
        self._omega = omega
        self._xi = xi
        self._tacc0_Myr = tacc0
        self._t = 0


    def Sigmadot(self, grid, disc, sigma, alpha_DW_t):
        sigmadot = (3*alpha_DW_t*sigma*disc._eos._f_cs(grid.Rc)**2)/(4*(self._leverarm-1)*grid.Rc**2*disc.Omega_k)
        return sigmadot

    def __call__(self, disc, dt):
        
        grid = disc.grid
        sigma = disc.Sigma

        alpha_DW_t = Advection._compute_alpha_DW_time(self, self._t)

        sigmadot = self.Sigmadot(grid, disc, sigma, alpha_DW_t)
        Sigma_new = disc.Sigma - dt * sigmadot
        
        disc.Sigma[:] = Sigma_new

        disc.Sigma[0] = disc.Sigma[1]*(grid.Rc[1]/grid.Rc[0])**(1-self._xi)
        disc.Sigma[-1] = disc.Sigma[-2]*(grid.Rc[-2]/grid.Rc[-1])**(1-self._xi)
