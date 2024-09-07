# disc.py
#
# Author: R. Booth
# Date: 8 - Nov - 2016
#
# Base class for an accretion disc. Used on its own, the AccretionDisc class
# represents a dust-free accretion disc, in which the total density is just the
# gas density.
#
################################################################################
import numpy as np
from .constants import AU, sig_H2, m_H

class AccretionDisc(object):

    def __init__(self, grid, star, eos, Sigma=None, mdot_photoev = 0, L_x = 0):
        self._grid = grid
        self._star = star
        self._eos  = eos
        self._mdot_photoev = mdot_photoev
        self._L_x = L_x
        if Sigma is None:
            Sigma = np.zeros_like(self.R)
        self._Sigma = Sigma


    def header(self):
        '''Write header information about the disc'''
        head  = ''
        head += self._grid.header() + '\n'
        head += self._star.header() + '\n'
        head += self._eos.header() 
        return head

    @property
    def star(self):
        return self._star

    @property
    def R(self):
        '''Cell centre radii'''
        return self._grid.Rc

    @property
    def R_edge(self):
        '''Cell edge radii'''
        return self._grid.Re

    @property
    def grid(self):
        return self._grid

    @property
    def Sigma(self):
        '''Surface density'''
        return self._Sigma

    @property
    def Sigma_G(self):
        '''Gas surface density'''
        return self.Sigma 

    @property
    def cs(self):
        '''Sound speed'''
        return self._eos.cs

    @property
    def T(self):
        '''Temperature'''
        return self._eos.T

    @property
    def mu(self):
        return self._eos.mu
    
    @property
    def H(self):
        '''Scale-height'''
        return self._eos.H

    @property
    def P(self):
        return self.midplane_gas_density * self.cs**2 

    @property
    def midplane_gas_density(self):
        return self.Sigma_G / (np.sqrt(2*np.pi) * self.H * AU)

    @property
    def midplane_density(self):
        return self.Sigma / (np.sqrt(2*np.pi) * self.H * AU)

    @property
    def Ncells(self):
        return self._grid.Ncells

    @property
    def alpha(self):
        return self._eos.alpha

    @property
    def nu(self):
        return self._eos.nu
    
    @property
    def Re(self):
        '''Reynolds number'''
        return (self.alpha*self.Sigma_G*sig_H2) / (2*self._eos.mu*m_H)

    @property
    def Pr(self):
        '''Prandtl number'''
        return self._eos.Pr

    @property
    def Omega_k(self):
        return self._star.Omega_k(self.R)

    @property
    def dust_frac(self):
        return 0

    @property
    def amax(self):
        return 0

    @property
    def mdot_photoev(self):
        return self._mdot_photoev

    @property
    def L_x(self):
        return self._L_x

    def discmass(self):
        """
        Compute the disc mass in Msun. See the documentation for details on the 1.5e33**2/2e33 factor.
        """
        mass_tmp = 2. * np.pi*np.trapz(self.R*self.Sigma_G, self.R)
        mass = mass_tmp*(1.5e13)**2/2e33
        return mass

    def set_surface_density(self, Sigma):
        self._Sigma[:] = Sigma

    def update(self, dt):
        '''Update the disc properites and age'''

        self._star.evolve(dt/(2*np.pi))
        self._eos.update(dt, self.Sigma, self._star)

    def interp(self, R, data):
        '''Interpolate disc data to new radii
        
        args:
            R    : new radii
            data : data defined at grid locations
        '''
        return self.grid.interp_centre(R, data)
