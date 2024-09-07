# dust_dynamics.py
#
# Author: R. Booth
# Date: 17 - Nov - 2016
#
# Combined model for the evolution of gas, dust and chemical species in a
# viscously evolving disc.
################################################################################
from __future__ import print_function

import numpy as np
import os

from .diffusion import TracerDiffusion
from .dust import SingleFluidDrift, Advection
from .ViscousEvolution import ViscousEvolution
from .disc_utils import mkdir_p
from .mhd_massloss import MHD_massloss
from .internal_photoev import internal_photoev


class DustDynamicsModel(object):
    """
    Includes dust dynamics, MHD disc winds (Tabone et al. 2021).

    args:
        diffusion           : whether to include diffusion (default = False)
        radial_drift        : whether to include radial drift (default = False)
        viscous_evo         : whether to include viscous evolution (default = True)
        int_photoevaporation: whether to include internal photoevaporation (default = False)
        ext_photoevaporation: whether to include external photoevaporation (default = False)
        setling             : whether to include dust settling (default = False)
        advection           : whether to include MHD advection (default = True)
        alpha_DW            : alpha disc wind parameter (Tabone et al. 2021)
        leverarm            : magnetic leverarm parameter (Tabone et al. 2021)
        xi                  : xi parameter (Tabone et al. 2021)
        Sc                  :
        t0                  : initial time
    """
    def __init__(self, disc,
                 diffusion = False, radial_drift = False, viscous_evo = True, int_photoevaporation = True,
                 ext_photoevaporation = False, settling = False, advection = True, mhd_massloss = True, 
                 alpha_DW = 1e-3, leverarm = 3, omega = 0, tacc0 = 0, xi = 1, Sc = 1, t0 = 0):

        self._disc = disc
        self._flag_dispersion = False
        
        self._visc = None
        if viscous_evo:
            #bound = 'power-law'
            bound = 'Zero'
            # Power law extrapolation fails with zero-density, use simple
            # boundary condition instead
            if ext_photoevaporation: 
                bound = 'Zero'
            
            self._visc = ViscousEvolution(boundary = bound)

        self._diffusion = None
        if diffusion:
            diffusion = TracerDiffusion(Sc)

        # Diffusion can be handled by the radial drift object, without dust we
        # include it ourself.
        self._radial_drift = None
        if radial_drift:
            self._radial_drift = SingleFluidDrift(diffusion, settling)
        else:
            self._diffusion = diffusion

        self._int_photoevaporation = False
        if int_photoevaporation:
            self._int_photoevaporation = internal_photoev(disc)

        self._ext_photoevaporation = False
        if ext_photoevaporation:
            self._ext_photoevaporation = ext_photoevaporation(grid, disc)

        self._advection = False
        if advection:
            self._advection = Advection(alpha_DW = alpha_DW, omega = omega, tacc0 = tacc0)

        self._mhd_massloss = False
        if mhd_massloss:
            self._mhd_massloss = MHD_massloss(alpha_DW, leverarm, omega, xi, tacc0)

        self._t = t0
        
    def max_timestep(self):
        dt = 1e300
        if self._visc:
            dt = min(dt, self._visc.max_timestep(self._disc))
        if self._radial_drift:
            dt = min(dt, self._radial_drift.max_timestep(self._disc))
        if self._advection:
            dt = min(dt, self._advection.max_timestep(self._disc))
        return dt    
            
    def __call__(self, dt):
        """
        Evolve the disc for a single timestep

        args:
            dtmax   : Upper limit to time-step

        returns:
            dt      : Time step taken
        """
        
        disc = self._disc
    
        # Do Advection-diffusion update
        if self._visc:
            dust = None
            size = None
            try:
                dust = disc.dust_frac
                size = disc.grain_size
            except AttributeError:
                pass
            mdot, mdotouter = self._visc(dt, disc, [dust, size])
        else:
            mdot = 0
            mdotouter = 0

        if self._radial_drift:
            self._radial_drift(dt, disc)
            
        # Pin the values to >= 0:
        disc.Sigma[:]     = np.maximum(disc.Sigma, 0)
        try:
            disc.dust_frac[:] = np.maximum(disc.dust_frac, 0)
        except AttributeError:
            pass
        except TypeError:
            pass

        # Internal photoevaporation
        if self._int_photoevaporation:
            self._int_photoevaporation(disc, dt)

            self._flag_dispersion = self._int_photoevaporation.return_flag_dispersion(self._int_photoevaporation)

        # External photoevaporation:
        if self._ext_photoevaporation:
            self._ext_photoevaporation(disc, dt)

        # MHD advection:
        if self._advection:
            mdot_wind, mdotouter_wind = self._advection(disc, dt)

            mdot += mdot_wind
            mdotouter += mdotouter_wind

        if self._mhd_massloss:
            self._mhd_massloss(disc, dt)

        # Now we should update the auxillary properties, do grain growth etc
        disc.update(dt)

        self._t += dt
        return mdot, mdotouter, self._flag_dispersion

    @property
    def disc(self):
        return self._disc

    @property
    def t(self):
        return self._t    

    @property
    def flag_dispersion(self):
        return self._flag_dispersion

    def dump(self, filename):
        '''Write the current state to a file, including header information'''

        # Put together a header containing information about the physics
        # included
        head = self.disc.header() + '\n'
        if self._visc:
            head += self._visc.header() + '\n'
        if self._radial_drift:
            head += self._radial_drift.header() + '\n'
        if self._advection:
            head += self._advection.header() + '\n'
        if self._diffusion:
            head += self._diffusion.header() + '\n'
        try:
            head += self._chem.header() + '\n'
        except AttributeError:
            pass
        
        with open(filename, 'w') as f:
            f.write(head+'# time: {}yr\n'.format(self.t/(2*np.pi)))

            # Construct the list of variables that we are going to print
            Ncell = self.disc.Ncells

            Ndust = 0
            try:
                Ndust = self.disc.dust_frac.shape[0]
            except AttributeError:
                pass
                
            head = '# R Sigma T'
            for i in range(Ndust):
                head += ' epsilon[{}]'.format(i)
            for i in range(Ndust):
                head += ' a[{}]'.format(i)
            chem = None
            try:
                chem = self.disc.chem
                for k in chem.gas:
                    head += ' {}'.format(k)
                for k in chem.ice:
                    head += ' s{}'.format(k)
            except AttributeError:
                pass

            f.write(head)

            R, Sig, T = self.disc.R, self.disc.Sigma, self.disc.T
            for i in range(Ncell):
                f.write("{0} {1} {2} ".format(R[i], Sig[i], T[i]))
                for j in range(Ndust):
                    f.write("{0} ".format(self.disc.dust_frac[j,i]))
                for j in range(Ndust):
                    f.write("{0}".format(self.disc.grain_size[j,i]))
                if chem:
                    for k in chem.gas:
                        f.write("{0} ".format(chem.gas[k][i]))
                    for k in chem.ice:
                        f.write("{0} ".format(chem.ice[k][i]))
                f.write("\n")



class IO_Controller(object):
    '''Handles time and book-keeping for when to dump data to file / screen.

    args:
        t_print  : times to print to screen
        t_save   : times to save files
        t_inject : times to inject planets
    '''
    def __init__(self, t_print=[], t_save=[], t_inject=[]):
        self._tprint  = sorted(t_print)
        self._tsave   = sorted(t_save)
        self._tinject = sorted(t_inject)

        self._nsave  = 0
        self._nprint = 0

    @property
    def t_next(self):
        '''Next time to print or save'''
        t_next = np.inf
        if self._tprint : t_next = min(t_next, self._tprint[0])
        if self._tsave  : t_next = min(t_next, self._tsave[0])
        if self._tinject: t_next = min(t_next, self._tinject[0])

        return t_next

    def need_print(self, t):
        '''Check whether we need to print to screen'''
        if self._tprint: return self._tprint[0] <= t
        return False

    def need_save(self, t):
        '''Check whether we need to print to screen'''
        if self._tsave: return self._tsave[0] <= t
        return False

    def need_injection(self, t):
        '''Check whether we need to inject planets'''
        if self._tinject: return self._tinject[0] <= t
        return False

    @property
    def nprint(self):
        return self._nprint
    @property
    def nsave(self):
        return self._nsave

    def pop_times(self, t):
        '''Remove any elapsed times from save & print lists'''
        while self._tprint and self._tprint[0] <= t:
            self._tprint.pop(0)
            self._nprint += 1
            
        while self._tsave and self._tsave[0] <= t:
            self._tsave.pop(0)
            self._nsave += 1
            
        while self._tinject and self._tinject[0] <= t:
            self._tinject.pop(0)

            
    @property
    def finished(self):
        return not (self._tprint or self._tsave or self._tinject)
        


if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt
    from grid import Grid
    from eos import LocallyIsothermalEOS, IrradiatedEOS
    from star import SimpleStar
    from dust import DustGrowthTwoPop
    from constants import Msun, AU, Omega0
    from photoevaporation import FixedExternalEvaportation
    
    np.seterr(invalid='raise')

    models = {}
    N = 1
    for Mdot in [1e-8, 1e-9]:
        alpha = 1e-3
        for Rc in [50, 100, 200]:
            model = { 'alpha' : alpha, 'R_d' : Rc, 
                      'Mdot' : Mdot,
                      'name' : 'Rc_{}'.format(Rc) }
            models['{}'.format(N)] = model
            N += 1
        Rc = 100
        for alpha in [5e-4, 1e-3, 5e-3, 1e-2]:
            model = { 'alpha' : alpha, 'R_d' : Rc, 
                      'Mdot' : Mdot,
                      'name' : 'alpha_{}'.format(alpha) }
            models['{}'.format(N)] = model
            N += 1


    try:
        model = models[sys.argv[1]]
    except IndexError:
        model = models['1']

    
    # Model values
    Mdot = model['Mdot'] 
    alpha = model['alpha']
    Rd = model['R_d'] 

    R_in  = 0.1
    R_out = 500

    N_cell = 1000
    
    T0 = 2*np.pi

    Mdot *= Msun / (2*np.pi)
    Mdot /= AU**2

    eos_type = 'irradiated'
    eos_type = 'isothermal'

    DIR = os.path.join('temp', eos_type,
                       model['name'], 'Mdot_{}'.format(model['Mdot']))
    mkdir_p(DIR)

    with open(os.path.join(DIR, 'model.dat'), 'w') as f:
        for k in model:
            f.write("{1} {2}\n".format(k, model[k]))
    
    # Initialize the disc model
    grid = Grid(R_in, R_out, N_cell, spacing='natural')
    star = SimpleStar(M=1, R=2.5, T_eff=4000.)

    eos = LocallyIsothermalEOS(star, 1/30., -0.25, alpha)
    eos.set_grid(grid)
    Sigma = (Mdot / (3 * np.pi * eos.nu))*np.exp(-grid.Rc/Rd)
    if eos_type != 'isothermal':
        # Use a non accreting model to guess the initial density
        eos = IrradiatedEOS(star, alpha, tol=1e-3, accrete=False)     
        eos.set_grid(grid)
        eos.update(0, Sigma)
        
        # Now do a new guess for the surface density and initial eos.
        Sigma = (Mdot / (3 * np.pi * eos.nu))*np.exp(-grid.Rc/Rd)

        eos = IrradiatedEOS(star, alpha, tol=1e-3)
        eos.set_grid(grid)
        eos.update(0, Sigma)

    # Initialize the complete disc object
    disc = DustGrowthTwoPop(grid, star, eos, 0.01, Sigma=Sigma, feedback=True)


    
    # Setup the dust-dynamical model
    evo = DustDynamicsModel(disc,
                            viscous_evo=True,
                            radial_drift=True,
                            diffusion=True,
                            ext_photoevaporation=FixedExternalEvaportation(Mdot=1e-8))


    # Solve for the evolution
    print_times  = np.array([0, 1e5, 5e5, 1e6, 3e6]) * T0
    output_times = np.arange(0, 3e6+1e3, 1e4) * T0

    IO = IO_Controller(t_print=print_times, t_save=output_times)

    n = 0
    while not IO.finished:
        ti = IO.t_next
        while evo.t < ti:
            dt = evo(ti)

            n += 1
            if (n % 1000) == 0:
                print('Nstep: {}'.format(n))
                print('Time: {} yr'.format(evo.t/(2*np.pi)))
                print('dt: {} yr'.format(dt / (2*np.pi)))
                
        if IO.need_save(evo.t) and False:
            evo.dump(os.path.join(DIR, 'disc_{:04d}.dat'.format(IO.nsave)))


        if IO.need_print(evo.t):
            err_state = np.seterr(all='warn')

            print('Nstep: {}'.format(n))
            print('Time: {} yr'.format(evo.t/(2*np.pi)))
            plt.subplot(221)
            l, = plt.loglog(grid.Rc, evo.disc.Sigma_G)
            plt.loglog(grid.Rc, evo.disc.Sigma_D.sum(0), l.get_color() + '--')
            plt.xlabel('$R$')
            plt.ylabel('$\Sigma_\mathrm{G, D}$')
            
            plt.subplot(222)
            l, = plt.loglog(grid.Rc, evo.disc.dust_frac.sum(0))
            plt.xlabel('$R$')
            plt.ylabel('$\epsilon$')
            plt.subplot(223)
            l, = plt.loglog(grid.Rc, evo.disc.Stokes()[1])
            plt.xlabel('$R$')
            plt.ylabel('$St$')
            plt.subplot(224)
            l, = plt.loglog(grid.Rc, evo.disc.grain_size[1])
            plt.xlabel('$R$')
            plt.ylabel('$a\,[\mathrm{cm}]$')


            np.seterr(**err_state)

        IO.pop_times(evo.t)   
 
    plt.show()
