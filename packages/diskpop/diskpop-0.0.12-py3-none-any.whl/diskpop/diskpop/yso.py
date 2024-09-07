#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import numpy as np

from .DiscEvolution.src.grid import Grid
from .DiscEvolution.src.ViscousEvolution import ViscousEvolution, LBP_Solution, PL_sigma
from .analytic_disc import MHD_Solution_fiducial, MHD_Solution_omega
from .analytic_disc import MHD_Solution_fiducial, MHD_Solution_omega
from .DiscEvolution.src.disc import AccretionDisc
from .DiscEvolution.src.dust_dynamics import DustDynamicsModel
from .DiscEvolution.src.dust import DustGrowthTwoPop
from .eos_diskpop import LocallyIsothermalEOS, SimpleIrradiatedDisc_EOS

from .io_diskpop import OutfileLeonardo

from .io_diskpop import save_snapshot
from .star import Star

from .analytic_disc import MockAnalyticDynamicsModel


def select_parameters(key, params, defaults, no_default):
    try:
        return params[key]
    except KeyError:
        if no_default:
            raise ValueError("Cannot initiate YSO/disc with default values ({})\n {}".format(key,params))
        else:
            return defaults[key]

def make_LB(Md, Rd, eos, grid, tacc0 = None, omega = None, leverarm = None):
    """
    Return the Lynden-Bell&Pringle (1974) solution.
    """
    nud = np.interp(Rd, grid.Rc, eos.nu)				
    sol = LBP_Solution(Md, Rd, nud, 1)					# Lynden - Bell & Pringle solution with gamma = 1
    return sol(grid.Rc, 0)

def make_hybrid(Md, Rd, grid, tacc0, leverarm, omega = None, eos = None):
    sol = MHD_Solution_fiducial(Md, Rd, grid._R0, tacc0, leverarm)
    return sol(grid.Rc, 0)

def make_mhd_omega(Md, Rd, grid, tacc0, omega, leverarm, eos = None):
    sol = MHD_Solution_omega(Md, Rd, grid._R0, tacc0, omega, leverarm = leverarm)
    return sol(grid.Rc, 0)


def mass(disc):
    return (disc.Sigma*2*np.pi*disc.grid.Rc*disc.grid._dRe).sum()


class YSO(object):
    """
    This object handles the evolution of a single star-disc system. For the disc
    part, it takes care of communicating with the DiscEvolution code and setting
    up all the objects it needs.

    """
    default_yso_parameters = {'yso_id': 'test_yso',  			# YSO unique id in population
                              'yso_type': 'ClassII',  			# Type of YSO
                              'target_age': 1,  				# age of the YSO once the population is evolved up to population.py's age
                              'outfile': None,
                              'index': 1,
                              #'L_x': 0,
                              'flag_dispersion': False,
                              }
    default_disc_parameters = {'rin': 0.1,  					# Inner radius of the disc [au]
                               'rout': 1000,  					# Outer radius of the disc [au]
                               'nr': 1000,  					# Number of points in radial grid
                               'spacing': 'natural',  			# Spacing of the grid
                               'analytic': False,   			# Whether to use the analytic solution
                               'alpha': 1e-3,  					# Shakura & Sunayev (1973) alpha parameter
                               'beta_mag': 0,                   # Beta magnetisation parameter
                               'beta_mag': 0,                   # Beta magnetisation parameter
                               'alpha_DW': 1e-3,  			    # Tabone et al. (2021) alpha disc wind parameter
                               'leverarm': 100,					# Tabone et al. (2021) lever arm parameter (lambda)
                               'omega': 0.5,                    # Tabone et al. (2021) omega parameter
                               'mdot_photoev': 1e-9,            # Internal photoevaporation mass loss rate [Msun/yr]
                               'L_x': 0,
                               'limit_discmass': 1e-12,
                               'beta': -0.5,
                               'SlopeCs': -0.25,  				# Slope of the sound speed with radius
                               'Hr0': 1. / 30,  				# H/R at R = 1 au
                               'Rd': 30.,  						# Initial scaling radius of the disc [au]
                               'Md': 1e-2,  					# Initial disc mass [Msun]
                               'd2g': 0.01,  					# Dust-to-gas ratio
                               'feedback': False,				# Feedback of the dust onto the gas
                               'dust': False,  					# Wheter to include dust
                               'outfile': None, 
                               }

    def __init__(self, parameters_user):
        """
        Construct the yso with a list of parameters. See the default parameters
        documentation for their meaning. Parameters that are not initialised
        in the dictionary passed here take their default value.
        """

        if 'no_default' in parameters_user['yso']:
            self.no_default = parameters_user['yso']['no_default']
        else:
            self.no_default = True

        self.parameters = parameters_user

        self.yso_parameters = {key: select_parameters(key, parameters_user['yso'],
                                                      self.default_yso_parameters, self.no_default)
                               for key in self.default_yso_parameters}

        self.parameters['yso'] = self.yso_parameters

        #self.parameters 

        self.outfile = self.yso_parameters['outfile']			# Sets the output file

        # init the star
        self.star = Star(parameters_user['star'])			    # Constructor of an object of class Star, with default parameters unless explicitly passed in parameters_user (which is being used to construct the yso too
        
        #init internal variables
        self.target_age = self.yso_parameters['target_age']
        self.evolution_time = 0.
        #self.disc_mdot = 0.
        self.disc_mdotouter = 0.

        if self.yso_parameters['yso_type'] == 'ClassII':

            self.disc_parameters = {key: select_parameters(key, parameters_user['disc'],
                                                          self.default_disc_parameters, self.no_default)
                                   for key in self.default_disc_parameters}

            #
            self._generate_initial_disc()

            #
            # Select evolver type
            self.evolve = self.evolve_class_ii				# Function for evolution, if class is II
        elif self.yso_parameters['yso_type'] == 'ClassIII':
            #
            # Select evolver type
            self.evolve = self.evolve_class_iii				# Function for evolution, if class is III
        else:
            raise ValueError("yso_type {} not recognized".format(self.yso_parameters['yso_type']))

        #
        #

    def _generate_initial_disc(self):
        # Set up auxiliary objects needed by the disc constructor
        grid = Grid(self.disc_parameters['rin'],
                    self.disc_parameters['rout'],
                    self.disc_parameters['nr'],
                    self.disc_parameters['spacing'])

        # init the equation of state
        eos = LocallyIsothermalEOS(self.star,
                                   self.disc_parameters['Hr0'],
                                   self.disc_parameters['beta'],
                                   self.disc_parameters['SlopeCs'],
                                   self.disc_parameters['alpha'])
        eos.set_grid(grid, self.star)

        tacc0 = self.disc_parameters['Rd']/(3.*(eos._f_H(self.disc_parameters['Rd'])/self.disc_parameters['Rd'])*eos._f_cs(self.disc_parameters['Rd'])*(self.disc_parameters['alpha_DW']+self.disc_parameters['alpha']))
        self.tacc0_Myr = tacc0/(2.*np.pi*1e6)   


        self.disc_parameters['tacc0_Myr'] = self.tacc0_Myr

        self._def_initial_Sigma()

        sigma = self._make_Sigma_init(Md = self.disc_parameters['Md'],
                                      Rd = self.disc_parameters['Rd'],
                                      eos = eos, grid = grid, tacc0 = self.tacc0_Myr,
                                      omega = self. disc_parameters['omega'], leverarm = self.disc_parameters['leverarm'])

        self.flag_dispersion = False


        if self.disc_parameters['alpha'] != 0:
            viscous_evo = True
        else:
            viscous_evo = False

        if self.disc_parameters['alpha_DW'] == 0:
            advection = False
            mhd_massloss = False
        else:
            advection = True
            mhd_massloss = True

        if self.disc_parameters['mdot_photoev'] == 0 and self.disc_parameters['L_x'] == 0:
            int_photoevaporation = False
        else:
            int_photoevaporation = True


        # Construct the disc object
        if self.disc_parameters['dust'] == False:
            self.disc = AccretionDisc(grid, self.star, eos, sigma, mdot_photoev = self.disc_parameters['mdot_photoev'], L_x = self.disc_parameters['L_x'])		# Disc without dust
        else:
            self.disc = DustGrowthTwoPop(grid, self.star, eos, self.disc_parameters['d2g'], Sigma=sigma,
                                         feedback=self.disc_parameters['feedback'])
     
        if self.disc_parameters['analytic']:
            self.evo = MockAnalyticDynamicsModel(self.disc, self.disc_parameters, self.yso_parameters['yso_type'])                   # Evolves analytically - it knows whether to use LBP or Tabone+
            if self.disc_parameters['alpha_DW'] != 0:
                self.disc_parameters['fM0'] = MockAnalyticDynamicsModel(self.disc, self.disc_parameters, self.yso_parameters['yso_type'])._fM0
        else:
            if self.disc_parameters['alpha_DW'] == 0:
                self.evo = DustDynamicsModel(self.disc, diffusion = self.disc_parameters['dust'],
                                        radial_drift = self.disc_parameters['dust'], viscous_evo = True, 
                                        int_photoevaporation = int_photoevaporation, advection = False, mhd_massloss = False)	# Evolves numerically- sets the MHD parameters (advection and mhd_massloss) to zero
            else:
                xi = MockAnalyticDynamicsModel(self.disc, self.disc_parameters, self.yso_parameters['yso_type'])._xi
                self.disc_parameters['fM0'] = MockAnalyticDynamicsModel(self.disc, self.disc_parameters, self.yso_parameters['yso_type'])._fM0
                self.evo = DustDynamicsModel(self.disc, diffusion = self.disc_parameters['dust'],
                                        radial_drift = self.disc_parameters['dust'], viscous_evo = viscous_evo, 
                                        int_photoevaporation = int_photoevaporation, advection = advection, 
                                        mhd_massloss = mhd_massloss, alpha_DW = self.disc_parameters['alpha_DW'], 
                                        leverarm = self.disc_parameters['leverarm'], omega = self.disc_parameters['omega'], tacc0 = self.tacc0_Myr, xi = xi)

    #
    # Write/read from hdf5
    #

    def io_yso_hdf5(self, myhdf5file, operation, i_pop, i_time, i_yso):

        if not self.outfile:
            self.outfile = OutfileLeonardo(myhdf5file)
        
        #
        # First step: star (same for writing and reading)
        #

        self.star.io_star_hdf5(self.outfile.filename, operation, i_pop, i_time, i_yso)


        #
        # Writing
        #
    
        if operation == 'write':

            # YSO

            yso_data_to_write = {'evolution_time': self.evolution_time,
                                        }

            self.outfile.write_data_to_hdf5(self.outfile.yso_paths_list[i_pop][i_time][i_yso],
                                            yso_data_to_write, self.yso_parameters)

            # Disc

            if self.yso_parameters['yso_type'] == 'ClassII':

                disc_data_to_write = {#'mdot': self.disc_mdot,
                                          'mdot_outer': self.disc_mdotouter,
                                          'sigma': self.disc.Sigma,
                                          'T': self.disc.T,
                                          'Rc': self.disc.grid.Rc,
                                          'dust_frac': self.disc.dust_frac,
                                          'amax': self.disc.amax
                                          }

                self.outfile.write_data_to_hdf5(self.outfile.disc_paths_list[i_pop][i_time][i_yso],
                                                disc_data_to_write, self.disc_parameters)


        #
        # Reading
        #

        elif operation == 'read':

            # YSO
            # In order to read, you must create a new population - which is why you are setting the parameters

            yso_data_to_write, self.yso_parameters = self.outfile.read_data_from_hdf5(
                                                     self.outfile.yso_paths_list[i_pop][i_time][i_yso])

            self.evolution_time = yso_data_to_write['evolution_time']

            # Disc

            if self.yso_parameters['yso_type'] == 'ClassII':
                
                disc_data_to_write, self.disc_parameters = self.outfile.read_data_from_hdf5(
                                                            self.outfile.disc_paths_list[i_pop][i_time][i_yso])

                self._generate_initial_disc()
                self.disc_mdotouter = disc_data_to_write['mdot_outer']

                self.disc.Sigma[:] = disc_data_to_write['sigma']
                try:
                    self.disc.dust_frac[:] = disc_data_to_write['dust_frac']
                    self.disc.grain_size[1][:] = disc_data_to_write['amax']
                except TypeError:
                    pass

        else:
            raise ValueError("Error io in YSO: operation has to be read/write (operation={})".format(operation))




    def evolve_class_iii(self, time, **kwargs):
        """
        Evolve the ClassIII star until time t (substepping if necessary)
        """

        while (self.evolution_time) < time:
            dt_star = min(time-self.evolution_time,self.get_star_dt(self.star, partoler=0.1, dtguess=1.e5) )
            self.star.evolve(dt_star)
            self.evolution_time += dt_star


    def evolve_class_ii(self, time, **kwargs):
        """
        Evolve the star and disc system until time t (substepping if necessary)
        """

        while self.evolution_time < time:
            dt_star = self.get_star_dt(self.star, partoler=0.1, dtguess=1.e5)
            dt_disc = self.evo.max_timestep()
            dt = min(dt_star, dt_disc, time-self.evolution_time)

            self.star.evolve(dt)
            self.disc._star = self.star
            self.star.mdot, self.disc_mdotouter, self.flag_dispersion = self.evo(dt)

            self.evolution_time += dt

            if self.disc.discmass() < self.disc_parameters['limit_discmass']:
                self.flag_dispersion = True

            if self.flag_dispersion:
                self.kill_disc()
                print("Disc with identifier", self.yso_parameters['index']+1, "has been dispersed")
                self.evolve_class_iii(time)

    def kill_disc(self):
        """
        Remove the disc from the YSO, changing the type to classIII and the evolution method to evolve_class_iii.
        """
        self.evolve = self.evolve_class_iii
        self.yso_parameters['yso_type'] = 'ClassIII'


    def _def_initial_Sigma(self):
        """
        Define the method to compute the initial surface density.
        In the viscous case, and in the hybrid MHD case (:math:`alpha_{DW} \\neq 0` and :math:`\omega = 0`), it computes
        the Lynden-Bell&Pringle (1974) solution at t = 0. In the MHD case where :math:`\omega != 0`, it uses a constant
        instead (based on the Lynden-Bell&Pringle profile, without the exponential cutoff) to avoid dividing by zero.
        """
        if self.disc_parameters['omega'] != 0:
            self._make_Sigma_init = make_mhd_omega
        elif (self.disc_parameters['alpha'] == 0 and self.disc_parameters['alpha_DW'] != 0):
            self._make_Sigma_init = make_hybrid
        else:
            self._make_Sigma_init = make_LB

    @property    
    def sigma(self):
        return self.disc.Sigma
    
    @property
    def T(self):
        return self.disc.T
    
    @property
    def R(self):
        return self.disc.grid.Rc

    @property
    def tacc0(self):
        return self.tacc0_Myr
        

    @property
    def status(self):
        """
        An updated view of the evolver status.
        TODO: add more status variables, if any.

        """
        return dict(t=self.evolution_time, disc_mdot=self.star.mdot, disc_mdotouter=self.disc_mdotouter)
    

    @staticmethod
    def get_star_dt(mystar, partoler=0.1, dtguess=0.1, dtguesstol=0.1, dtguess_undershoot_factor=0.9):
        #
        check, dtgn, all_pars = mystar.check_time_step(dtguess, partoler=partoler)
        while not (check) and abs((dtguess - dtgn) / dtguess) > dtguesstol:
            dtguess = dtgn * dtguess_undershoot_factor
            check, dtgn, all_pars = mystar.check_time_step(dtguess, partoler=partoler)
        #
        return dtgn
