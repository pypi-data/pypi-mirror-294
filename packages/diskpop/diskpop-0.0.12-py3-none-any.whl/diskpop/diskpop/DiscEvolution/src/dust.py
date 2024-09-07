# dust.py
#
# Author: R. Booth
# Date : 10 - Nov - 2016
#
# Classes extending accretion disc objects to include dust models.
################################################################################
from __future__ import print_function

import numpy as np
from .constants import *
from .disc import AccretionDisc

class DustyDisc(AccretionDisc):
    '''Dusty accretion disc. Base class for an accretion disc that also
    includes one or more dust species.
    
    args:
        grid     : Disc gridding object
        star     : Stellar object
        eos      : Equation of state
        rho_s    : solid density, default=1
        feedback : When False, the dust mass is considered to be a negligable 
                   fraction of the total mass.
    '''
    def __init__(self, grid, star, eos, Sigma=None, rho_s=1., feedback=True):

        super(DustyDisc, self).__init__(grid, star, eos, Sigma)

        self._rho_s = rho_s
        self._Kdrag = (np.pi * rho_s) / 2.

        self._feedback = feedback


    def Stokes(self, Sigma=None, size=None):
        '''Stokes number of the particle'''
        if size is None:
            size = self.grain_size
        if Sigma is None:
            Sigma = self.Sigma_G
            
        return self._Kdrag * size / (Sigma + tiny)

    def mass(self):
        '''Grain mass'''
        return (4*np.pi/3) * self._rho_s * self.grain_size**3 

    @property
    def integ_dust_frac(self):
        '''Total dust to gas ratio, or zero if not including dust feedback'''
        if self._feedback:
            return self.dust_frac.sum(0)
        else:
            return 0

    @property
    def dust_frac(self):
        '''Dust mass fraction'''
        return self._eps

    @property
    def grain_size(self):
        '''Grain size in cm'''
        return self._a

    @property
    def feedback(self):
        '''True if drag from the dust on the gas is to be included'''
        return self._feedback

    @property
    def area(self):
        '''Mean area of grains'''
        return self._area


    # Overload Accretion disc densities to make it dusts

    @property
    def Sigma_G(self):
        return self.Sigma * (1-self.integ_dust_frac)

    @property
    def Sigma_D(self):
        return self.Sigma * self.dust_frac
    
    @property
    def midplane_dust_density(self):
        return self.Sigma_D / (np.sqrt(2*np.pi) * self.Hp * AU)
    
    @property
    def midplane_density(self):
        return self.midplane_gas_density + self.midplane_dust_density.sum(0)
    
    @property
    def Hp(self):
        '''Dust scale height'''

        St = self.Stokes()
        a  = self.alpha
        eta = 1 - 1. / (2 + 1./St)

        return self.H * np.sqrt(eta * a / (a + St))

    def update_ices(self, chem):
        '''Update ice fractions'''
        pass

    def header(self):
        '''Dusty disc header'''
        head = super(DustyDisc, self).header() + '\n'
        head += '# {} feedback: {}, rho_s: {}g cm^-3'
        return head.format(self.__class__.__name__,
                           self.feedback, self._rho_s)

        
################################################################################
# Growth model
################################################################################
class FixedSizeDust(DustyDisc):
    '''Simple model for dust of a fixed size
    
    args:
        grid     : Disc gridding object
        star     : Stellar object
        eos      : Equation of state
        eps      : Initial dust fraction (must broadcast to [size.shape, Ncell])
        size     : size, cm (float or 1-d array of sizes)
        rhos     : solid density, default=1 g / cm^3
        feedback : default=True
    '''
    def __init__(self, grid, star, eos, eps, size, Sigma=None, rhos=1, feedback=True):

        super(FixedSizeDust, self).__init__(grid, star, eos,
                                            Sigma, rhos, feedback)

        shape = np.atleast_1d(size).shape + (self.Ncells,)
        self._eps  = np.empty(shape, dtype='f8')
        self._a    = np.empty(shape, dtype='f8')
        self._eps.T[:] = np.atleast_1d(eps).T
        self._a.T[:]   = size

        self._area = np.pi * self._a**2

class DustGrowthTwoPop(DustyDisc):
    '''Two-population dust growth model of Birnstiel (2011).

    This model computes the flux of two dust populations. The smallest size
    particles are assumed to always be well coupled to the gas. For the larger
    particles we solve their growth up to the most stringent limit set by 
    radial drift and fragmentation. 

    Any dust tracers are assumed to have the same mass distribution as the dust
    particles themselves.

    args:
        Ncells    : Number of cells in grid
        eps       : Initital dust fraction
        rhos      : Grain solid density, default=1.
        uf_0      : Fragmentation velocity (default = 100 (cm/s))
        uf_ice    : Fragmentation velocity of icy grains (default = 1000 (cm/s))
        f_ice     : Ice fraction, default=1
        thresh    : Threshold ice fraction for switchng between icy/non icy
                    fragmentation velocity, default=0.1
        a0        : Initial particle size (default = 1e-5, 0.1 micron)
        f_drift   : Drift fitting factor. Reduce by a factor ~10 to model the 
                    role of bouncing (default=0.55).
        f_frag    : Fragmentation boundary fitting factor (default=0.37).
        feedback  : Whether to include feedback from dust on gas
    '''
    def __init__(self, grid, star, eos, eps, Sigma=None,
                 rho_s=1., uf_0=100., uf_ice=1e3, f_ice=1, thresh=0.1,
                 a0=1e-5, f_drift=0.55, f_frag=0.37, feedback=True):
        super(DustGrowthTwoPop, self).__init__(grid, star, eos,
                                               Sigma, rho_s, feedback)

        
        self._uf_0   = uf_0 / (AU * Omega0)
        self._uf_ice = uf_ice / (AU * Omega0)

        # Fitting factors
        self._ffrag  = f_frag * (2/(3*np.pi)) 
        self._fdrift = f_drift * (2/np.pi)
        self._fmass  = np.array([0.97, 0.75])

        # Initialize the dust distribution
        Ncells = self.Ncells
        self._fm    = np.zeros(Ncells, dtype='f8')
        self._a0    = 0 # Force well-coupled limit
        self._eps   = np.empty([2, Ncells], dtype='f8')
        self._a     = np.empty([2, Ncells], dtype='f8')
        self._eps[0] = eps
        self._eps[1] = 0
        self._a[0]   = a0
        self._a[1]   = a0
        self._amin    = a0

        self._ice_threshold = thresh
        self._uf = self._frag_velocity(f_ice)
        self._area = np.pi * a0*a0

        self._head = (', uf_0: {}cm s^-1, uf_ice: {}cm s^-1, thresh: {}'
                      ', a0: {}cm'.format(uf_0, uf_ice, thresh, a0))
        
        self.update(0)

    def header(self):
        '''Dust growth header'''
        return super(DustGrowthTwoPop, self).header() + self._head

    def _frag_velocity(self, f_ice):
        '''Fragmentation velocity'''
        # Interplate between the icy/ice free region
        f_ice = np.minimum(f_ice/self._ice_threshold, 1)
        f_ice = f_ice*f_ice*f_ice*(10-f_ice*(15-6*f_ice))
        #f_ice = f_ice*f_ice*(3-2*f_ice)

        return self._uf_0 + (self._uf_ice - self._uf_0) * f_ice
        
    def _frag_limit(self):
        '''Maximum particle size before fragmentation kicks in'''
        af = (self.Sigma_G/(self._rho_s*self.alpha)) * (self._uf/self.cs)**2
        return self._ffrag * af

    def a_BT(self, eps_tot=None):
        '''Size at transition between Brownian motion and turbulence dominated
        collision velocities'''
        if eps_tot is None:
            eps_tot = self.integ_dust_frac

        a0  = 8 * self.Sigma / (np.pi * self._rho_s) * self.Re**-0.25
        a0 *= np.sqrt(self.mu*m_H/(self._rho_s*self.alpha)) / (2*np.pi)

        return a0**0.4
        
    def _gammaP(self):
        '''Dimensionless pressure gradient'''
        P = self.P
        R = self.R
        gamma = np.empty_like(P)
        gamma[1:-1] = abs((P[2:] - P[:-2])/(R[2:] - R[:-2]))
        gamma[ 0]   = abs((P[ 1] - P[  0])/(R[ 1] - R[ 0]))
        gamma[-1]   = abs((P[-1] - P[ -2])/(R[-1] - R[-2]))
        gamma *= R/(P+tiny)

        return gamma
        
    def _drift_limit(self, eps_tot):
        '''Maximum size due to drift limit or drift driven fragmentation'''
        gamma = self._gammaP()

        Sigma_D = self.Sigma * eps_tot
        Sigma_G = self.Sigma_G
            
        # Radial drift time-scale limit
        h = self.H / self.R
        ad = self._fdrift * (Sigma_D/self._rho_s) / (gamma * h**2+tiny)

        # Radial drift-driven fragmentation:
        cs = self.cs
        St_d = 2 * (self._uf/cs) / (gamma*h + tiny)
        af = St_d * (2/np.pi) * (Sigma_G / self._rho_s)

        return ad, af

    def _t_grow(self, eps):
        return 1 / (self.Omega_k * eps)

    def do_grain_growth(self, dt):
        '''Apply the grain growth'''

        # Size and total gas fraction
        a = self._a[1]        
        eps_tot = self.dust_frac.sum(0)
        
        afrag_t = self._frag_limit()
        adrift, afrag_d =  self._drift_limit(eps_tot)
        t_grow = self._t_grow(eps_tot)
       
        afrag = np.minimum(afrag_t, afrag_d)
        a0    = np.minimum(afrag, adrift)

        # Update the particle distribution
        #   Maximum size due to growth:
        amax = np.minimum(a0, a*np.exp(dt/t_grow))
        
        # Do not allow the grain size to become smaller than a0
        amax = np.maximum(amax, self._amin)
        
        #   Reduce size due to erosion / fragmentation if grains have grown
        #   above this due to ice condensation
        # amin = a + np.minimum(0, afrag-a)*np.expm1(-dt/t_grow)
        # ignore empty cells:
        ids = eps_tot > 0
        self._a[1, ids] = amax[ids]

        # Update the mass-fractions in each population
        fm   = self._fmass[1*(afrag < adrift)]
        self._fm[ids] = fm[ids]
        
        self._eps[0][ids] = ((1-fm)*eps_tot)[ids]
        self._eps[1][ids] = (   fm *eps_tot)[ids]

        # Set the average area:
        #self._area = np.pi * self.a_BT(eps_tot)**2

    def update_ices(self, grains):
        '''Update the grain size due to a change in bulk ice abundance'''
        eps_new = grains.total_abund
            
        #f = eps_new / (self.integ_dust_frac + tiny)
        #self._a[1] = np.maximum(self._a0, self._a[1]*f**(1/3.))

        self._eps[0] = eps_new*(1-self._fm)
        self._eps[1] = eps_new*   self._fm

        # Update the ice fraction
        f_ice = 0
        for spec in grains:
            if 'grain' not in spec:
                f_ice += grains[spec]
        f_ice /= (eps_new + tiny)

        self._uf = self._frag_velocity(f_ice)

    def initialize_dust_density(self, dust_frac):
        '''Set the initial dust density'''
        self._eps[0] = dust_frac


    def update(self, dt):
        '''Do the standard disc update, and apply grain growth'''
        super(DustGrowthTwoPop, self).update(dt)
        self.do_grain_growth(dt)

    @property
    def amax(self):
        return self.grain_size[1]

################################################################################
# Radial drift
################################################################################
class SingleFluidDrift(object):
    '''Radial Drift in the single fluid approximation with the short friction 
    time limit.

    This class computes the single-fluid update of the dust fraction,
        d(eps_i)/dt = - (1/Sigma) grad [Sigma eps_i (Delta v_i - eps Delta v)],
    which is a vertically integrated version of equation (98) of Laibe & Price 
    (2014). Note that the time-derivative on the LHS is the Lagrangian 
    derivative in centre of mass frame. If an Eulerian (fixed) grid is used the
    advection step must be handled seperately.
    
    The dust-gas relative velocity, Delta v_i, is calculated following 
    Tanaka+ (2005).

    Note:
        This currently neglects the viscous velocity, which can be important 
        for small grains.

    args:
        diffusion : Diffusion algorithm, default=None
        settling  : Include settling in the velocity calculation, default=False
    '''
    def __init__(self, diffusion=None, settling=False):
        self._diffuse = diffusion
        self._settling = settling

    def header(self):
        '''Radial drift header'''
        head = ''
        if self._diffuse:
            head += self._diffuse.header() + '\n'
        head += ('# {} diffusion: {} settling: {}'
                 ''.format(self.__class__.__name__,
                           self._diffuse is not None,
                           self._settling))
        return head
        
    def max_timestep(self, disc):
        step = np.inf
        
        dV = abs(self._compute_deltaV(disc))
        dV[dV==0]=np.finfo(float).tiny
        return 0.5 * (disc.grid.dRc / dV).min()


        eps_tot = 0
        if disc.feedback:
            eps_tot = disc.dust_frac.sum(0)

        grid  = disc.grid
        Sigma = disc.Sigma*(1-eps_tot)
        Om_k  = disc.Omega_k
        cs2   = disc.cs**2

        for a, eps in zip(disc.grain_size, disc.dust_frac):
            if not all((0 <= eps) & ( eps <= 1)):
                print('{}'.format(eps))
            assert(all((0 <= eps) & ( eps <= 1)))        

            ts = disc.Stokes(Sigma, a) / Om_k
            step = min(step,
                       0.25 * (grid.dRe2 / (eps*(1-eps_tot)*ts*cs2)).min())
        return step
    
    def _fluxes(self, disc, eps_i, deltaV_i, St_i):
        '''Update a quantity that moves with the gas/dust'''

        Sigma = disc.Sigma
        grid = disc.grid

        # Add boundary cells
        shape_v   = eps_i.shape[:-1] + (eps_i.shape[-1]+1,)
        shape_rho = eps_i.shape[:-1] + (eps_i.shape[-1]+2,)

        dV_i = np.empty(shape_v, dtype='f8')
        dV_i[...,1:-1] = deltaV_i - self._epsDeltaV
        dV_i[..., 0] = dV_i[..., 1] 
        dV_i[...,-1] = dV_i[...,-2] 

        Sig = np.zeros(shape_rho, dtype='f8')
        eps = np.zeros(shape_rho, dtype='f8')
        Sig[    1:-1] = Sigma
        eps[...,1:-1] = eps_i
        
        # Upwind the density
        Sig = np.where(dV_i > 0, Sig[    :-1], Sig[    1:])
        eps = np.where(dV_i > 0, eps[...,:-1], eps[...,1:])
        
        # Compute the fluxes
        flux = Sig*eps * dV_i


        # Do the update
        deps = - np.diff(flux*grid.Re) / ((Sigma+tiny)*0.5*grid.dRe2)
        if self._diffuse:
            St2 = St_i**2
            Sc = self._diffuse.Sc * (0.5625/(1 + 4*St2) + 0.4375 + 0.25*St2)

            deps += self._diffuse(disc, eps_i, Sc)
            
        return deps

    def _compute_deltaV(self, disc):
        '''Compute the total dust-gas background velocity'''

        Sigma  = disc.Sigma
        SigmaD = disc.Sigma_D
        Om_k   = disc.Omega_k
        a      = disc.grain_size

        # Average to cell edges:        
        Om_kav  = 0.5*(Om_k      [1:] + Om_k      [:-1])
        Sig_av  = 0.5*(Sigma     [1:] + Sigma     [:-1]) + tiny
        SigD_av = 0.5*(SigmaD[...,1:] + SigmaD[...,:-1])
        a_av    = 0.5*(a    [..., 1:] + a     [...,:-1])

        # Compute the density factors needed for the effect of feedback on
        # the radial drift velocity.
        eps_av = 0.
        eps_g = 1.
        SigG_av = Sig_av

        if disc.feedback:
            # By default, use the surface density
            eps_av = SigD_av / Sig_av
            eps_g = np.maximum(1 - eps_av.sum(0), tiny)
                
            SigG_av = Sig_av * eps_g

            # Use the midplane density instead
            if self._settling:
                rhoD = disc.midplane_dust_density
                rhoG = disc.midplane_gas_density
                rhoD_av = 0.5 * (rhoD[...,1:] + rhoD[...,:-1])
                rhoG_av = 0.5 * (rhoG    [1:] + rhoG    [:-1])
                rho_av = rhoD_av.sum(0) + rhoG_av + tiny

                eps_av = rhoD_av / rho_av
                eps_g  = np.maximum(rhoG_av / rho_av, tiny)
                
        # Compute the Stokes number        
        St_av = disc.Stokes(SigG_av, a_av+tiny)

        # Compute the lambda factors
        #   Use lambda * eps_g instead of lambda to avoid 0/0 when eps_g -> 0.
        la0, la1 = 0, 0 
        St_1 = 1 / (1 + St_av**2)

        if disc.feedback:
            la0 = (eps_av / (1     + St_av** 2)).sum(0)
            la1 = (eps_av / (St_av + St_av**-1)).sum(0)

        # Compute the gas velocities:
        rho = disc.midplane_gas_density
        dPdr = np.diff(disc.P) / disc.grid.dRc
        eta = - dPdr / (0.5*(rho[1:] + rho[:-1] + tiny)*Om_kav)

        D_1 = eps_g / ((eps_g + la0)**2 + la1**2)
        u_gas =                la1  * eta * D_1
        v_gas = - 0.5*(eps_g + la0) * eta * D_1

        # Dust-gas relative velocities:
        DeltaV = (2*v_gas / (St_av + St_av**-1) 
                  - u_gas / (1     + St_av**-2))

        # epsDeltaV = v_COM - v_gas (= 0 if dust mass is neglected)
        if disc.feedback:
            self._epsDeltaV = (eps_av * DeltaV).sum(0)
        else:
            self._epsDeltaV = 0

        return DeltaV

    def __call__(self, dt, disc, gas_tracers=None, dust_tracers=None):
        '''Apply the update for radial drift over time-step dt'''
        eps = disc.dust_frac
        a   = disc.grain_size   
        eps_inv = 1. / (disc.integ_dust_frac + np.finfo(eps.dtype).tiny)

        # Compute the dust-gas relative velocity
        DeltaV = self._compute_deltaV(disc)
        
        # Compute and apply the fluxes
        if gas_tracers is not None:
            gas_tracers[:] += dt * self._fluxes(disc, gas_tracers, 0, 0)

        # Update the dust fraction, size and tracers
        d_tr = 0
        for eps_k, dV_k, a_k, St_k in zip(disc.dust_frac, DeltaV,
                                          disc.grain_size, disc.Stokes()):
            if dust_tracers is not None:
                t_k = dust_tracers * eps_k * eps_inv
                d_tr  += dt*self._fluxes(disc, t_k, dV_k, St_k)

            # multiply a_k by the dust-to-gas ratio, so that constant functions
            # are advected perfectly
            eps_a = a_k * eps_k
            eps_a +=  dt*self._fluxes(disc, eps_a, dV_k, St_k)
            
            eps_k[:] += dt*self._fluxes(disc, eps_k, dV_k, St_k)

            a_k[:] = eps_a / (eps_k + tiny)

        if dust_tracers is not None:
            dust_tracers[:] += d_tr


class Advection(object):
    """
    Solution of the advection equation in the case of MHD disc winds

    args:
        
        advection   : whether to solve the advection equation, default = False
        alpha_DW    : alpha disc wind parameter (Tabone et al. 2021)
    """

    def __init__(self, advection = True, alpha_DW = 1e-3, omega = 0, tacc0 = 0):

        self._advection = advection
        self._alpha_DW = alpha_DW
        self._omega = omega
        self._tacc0_Myr = tacc0
        self._t = 0

    def header(self):
        '''Radial drift header'''
        head = ''
        if self._advection:
            head += self._advection.header() + '\n'
        head += ('# {} diffusion: {} settling: {}'
                 ''.format(self.__class__.__name__,
                           self._advection is not None))
        return head
        
    def max_timestep(self, disc):

        alpha_DW_t = self._compute_alpha_DW_time(self._t)
        dV = abs(self._compute_v_DW(disc, alpha_DW_t))
        dV[dV==0]=np.finfo(float).tiny
        dV = dV[    1:-1]
        return 0.1 * (disc.grid.dRc / dV).min()
    
    def _fluxes(self, disc, v_DW):
        """
        Update a quantity that moves with velocity v_DW (DW = disc wind)
        """

        Sigma = disc.Sigma
        grid = disc._grid

        R = grid.Re
        dR2 = grid.dRe2
    
        Sigma_fake = np.r_[Sigma[0], Sigma, Sigma[-1]]
        
        # Upwind the density
        Sigma = np.where(v_DW > 0, Sigma_fake[    :-1], Sigma_fake[    1:])
        
        
        # Compute the fluxes
        flux = Sigma* R*v_DW                      # Flux = transported quantity (R*Sigma) times the involved velocity (v_DW). Units: mass/time
        
        flux[0] = flux[1]
        flux[-1] = flux[-2]

        # Do the update
        deps = - np.diff(flux)/ (0.5*dR2)          # Flux times the surface over volume, which is 2/(*Delta(R^2)). The minus is because diff would subtract i+1/2 - i-1/2, but the algorithm requires the opposite. Units: mass/(area*time)
        deps_mdot_in = -flux[0]                    # The accretion rate is only the flux from one direction, not the difference, hence the scalar value. Units: mass/time
        deps_mdot_out = -flux[-1]                  # Same here, but at the outer disc. Units: mass/time

        return deps, deps_mdot_in, deps_mdot_out


    def _compute_v_DW(self, disc, alpha_DW_t):
        """
        Compute the MHD advection velocity (v disc wind)
        """

        grid = disc._grid

        H = disc._eos._f_H(grid.Re)                                  # Scale height of the disc evaluated at the cell interfaces (because this will be used to determine a velocity)
        cs = disc._eos._f_cs(grid.Re)                                # Sound speed in the disc evaluated at the cell interfaces ("")

        HoverR = H/grid.Re                                          # Aspect ratio of the disc evaluated at the cell interfaces ("")

       # Disc wind velocity (the minus is because it's towards the star):
        v_DW = - 3./2. * alpha_DW_t * HoverR * cs

        return v_DW
    
    def _compute_alpha_DW_time(self, t):

        t_Myr = t/(2*np.pi*1e6)
        t_omega = 1 - ((self._omega*t_Myr)/(2 * self._tacc0_Myr))
        alpha_DW_t = self._alpha_DW*t_omega**(-1)

        return alpha_DW_t


    def __call__(self, disc, dt, gas_tracers=None, dust_tracers=None):
        """
        Apply the update for advection over time-step dt
        """

        self._t = self._t + dt

        # Compute the disc wind advection velocity (Tabone et al. 2021) with time-dependent alpha_DW
        alpha_DW_t = self._compute_alpha_DW_time(self._t)
        v_DW = self._compute_v_DW(disc, alpha_DW_t)

        f, f_mdot_in, f_mdot_out = self._fluxes(disc, v_DW)

        Sigma_new = disc.Sigma + dt * f

        disc.Sigma[:] = Sigma_new

        mdot = f_mdot_in*2*np.pi
        mdotouter = f_mdot_out*2*np.pi
        
        return mdot, mdotouter



    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from grid import Grid
    from eos import LocallyIsothermalEOS
    from star import SimpleStar
    
    Mdot = 1e-8
    alpha = 1e-3

    Mdot *= Msun / (2*np.pi)
    Mdot /= AU**2
    Rd = 100.

    grid = Grid(0.1, 1000, 1000, spacing='log')
    star = SimpleStar()
    eos = LocallyIsothermalEOS(star, 1/30., -0.25, alpha)
    eos.set_grid(grid)
    Sigma =  (Mdot / (3 * np.pi * eos.nu))*np.exp(-grid.Rc/Rd)
    
    settling = True
    
    T0 = (2*np.pi)

    d2g = 0.01
    dust     = DustGrowthTwoPop(grid, star, eos, d2g, Sigma=Sigma)
    dust_ice = DustGrowthTwoPop(grid, star, eos, d2g, Sigma=Sigma)
    ices = {'H2O' : 0.9*d2g*(eos.T < 150), 'grains' : 0.1*d2g}

    class ices(dict):
        def __init__(self, init={}):
            dict.__init__(self, init)
    I = np.ones_like(eos.T)
    ices = ices({'H2O' : 0.9*d2g*(eos.T < 150), 'grains' : 0.1*d2g*I})
    ices.total_abund = np.atleast_2d([ices[x] for x in ices]).sum(0)
    dust_ice.update_ices(ices)

    # Integrate the dust sizes at fixed radial location:
    times = np.array([0, 1e2, 1e3, 1e4, 1e5, 1e6, 3e6]) * T0

    t = 0
    for ti in times:
        dust.do_grain_growth(ti-t)
        dust_ice.do_grain_growth(ti-t)
        t = ti
        Sigma = dust.Sigma
        plt.subplot(211)
        l, = plt.loglog(grid.Rc, dust.Stokes(Sigma)[1])
        l, = plt.loglog(grid.Rc, dust_ice.Stokes(Sigma)[1],'--',c=l.get_color())
        plt.subplot(212)
        l, = plt.loglog(grid.Rc, dust.grain_size[1])
        l, = plt.loglog(grid.Rc, dust_ice.grain_size[1], '--', c=l.get_color())

    plt.subplot(211)
    plt.xlabel('$R\,[\mathrm{au}]$')
    plt.ylabel('Stokes number')

    plt.subplot(212)
    plt.loglog(grid.Rc, dust.a_BT(), 'k:')
    plt.xlabel('$R\,[\mathrm{au}]$')
    plt.ylabel('$a\,[\mathrm{cm}]$')
    # Test the radial drift code
    plt.figure()
    dust = FixedSizeDust(grid, star, eos, 0.01, [0.01, 0.1], Sigma=Sigma)
    drift = SingleFluidDrift(settling=settling)
      
    times = np.array([0, 1e2, 1e3, 1e4, 1e5, 1e6, 3e6]) * 2*np.pi
    
    t = 0
    n = 0
    for ti in times:
        while t < ti:
            dt = 0.5*drift.max_timestep(dust)
            dti = min(ti-t, dt)

            drift(dt, dust)
            t = np.minimum(t + dt, ti)
            n += 1

            if (n % 1000) == 0:
                print('Nstep: {}'.format(n))
                print('Time: {} yr'.format(t/(2*np.pi)))
                print('dt: {} yr'.format(dt / (2*np.pi)))


        print('Nstep: {}'.format(n))
        print('Time: {} yr'.format(t/(2*np.pi)))
        l, = plt.loglog(grid.Rc, dust.Sigma_D[1])
        plt.loglog(grid.Rc, dust.Sigma_D[0], '-.', c=l.get_color())
        

    plt.loglog(grid.Rc, dust.Sigma_G, 'k:')
    plt.loglog(grid.Rc, dust.Sigma, 'k--')
    
    plt.xlabel('$R\,[\mathrm{au}]$')
    plt.ylabel('$\Sigma_{\mathrm{D,G}}$')
    plt.ylim(ymin=1e-10)
    plt.show()
    
