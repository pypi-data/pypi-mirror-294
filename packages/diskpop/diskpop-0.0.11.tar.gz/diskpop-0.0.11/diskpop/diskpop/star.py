#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from .io_diskpop import OutfileLeonardo
from .pmstracks.pmstracks.pmstracks import PMSTracks


def select_parameters(key, params, defaults, no_default):
    try:
        return params[key]
    except KeyError:
        if no_default and (key != 'llum' and key != 'teff'):
            raise ValueError("Cannot initiate Star with default values")
        else:
            return defaults[key]
     


class Star(object):
    """
    This class defines a Star object that contains that stellar parameters
    for a single star and the methods to evolve it.

    When the object is instantiated, there is a default set of parameters
    derived from the Siess+2000 tracks for a 1.0 Msun star, but, unless the default
    is overwritten, the object recalculates the photospheric parameters using the
    tracks (unless the constant_star method is selected).

    The stellar parameters contained in the object are the actual parameters
    (i.e. no history of the object is retained)

    The following parameters are stored:
    mass : stellar mass in Msun
    L_x  : stellar luminosity in erg/s, used for internal photoevaporation
    age  : age of star in Myr
    llum : stellar luminosity in Log10(L/Lsun)
    teff : photopheric effective temperature in K
    mdot : mass accretion rate in Msun/yr

    evolve_method and pmst store the star evolution method (at the moment constant_star or pmstracks_star)
        and the PMS Tracks that can be used to evolve the object.

    """

    default_parameters = {'mass': 1.0,
                          'teff': 4125.,
                          'llum': np.log10(12.166239),
                          'age': 1.1082734205E+05,
                          #'L_x': 0,
                          'mdot_evolution': False,  # Use mdot to evolve stellar mass
                          'mdot': 0.0,
                          'reset_lt': True,  # This is used to set up L,T from tracks
                          'pmstracks': None,
                          'evolve_method': 'constant',
                          'parent_yso': 'no_parent_yso',
                          'outfile': None,
                          }

    def __init__(self, parameters_user):
        """
        Docstring

        """
        if 'no_default' in parameters_user:
            self.no_default = parameters_user['no_default']
        else:
            self.no_default = True

        self.parameters = {key: select_parameters(key, parameters_user, self.default_parameters, self.no_default) for key in
                           self.default_parameters}

        self.star_par = self.parameters  #

        if self.no_default and ((not self.star_par['llum'] or not self.star_par['teff']) and not self.star_par['reset_lt']):
            raise ValueError("If reset_lt=False you need to initialize llum and teff for Star")
        else:
            self.star_par['teff'] = self.default_parameters['teff']
            self.star_par['llum'] = self.default_parameters['llum']

        # Default is chosen for 1.0Msun star from Siess+2000 tracks
        self.mass = self.star_par['mass']
        #self.L_x = self.star_par['L_x']
        self.teff = self.star_par['teff']
        self.llum = self.star_par['llum']
        self.age = self.star_par['age']
        self.mdot_evolution = self.star_par['mdot_evolution']
        self.mdot = self.star_par['mdot']
        self.mass_mdot = self.mass
        self.reset_lt = self.star_par['reset_lt']  # This is used to set up L,T from tracks
        #
        # Default is to NOT evolve following pms tracks,
        #
        self.pmst = self.star_par['pmstracks']
        self.evolve_method = self.star_par['evolve_method']
        #
        self.outfile = self.star_par['outfile']

        if self.evolve_method == 'constant':
            self.evolved_par = self.constant_star
            if self.reset_lt and (not self.pmst):
                raise ValueError("Cannot reset stellar L, Teff with pmstracks=None")
        elif self.evolve_method == 'pmstracks':
            if not self.pmst:
                raise ValueError("Cannot evolve star with pmstracks=None, pass valid pmstracks to Star")
            self.evolved_par = self.pmstracks_star
            # if reset_lt = True than the initial L,T are set from tracks (no evolution, obviously)
            if self.reset_lt:
                self.mass, self.llum, self.teff = self.evolved_par(self.age)
        else:
            raise ValueError("No valid evolve method specified in Star parameters.")



    def Omega_k(self,  r):
        '''Keplerian angular speed of a test particle.
        
        args:
            r : distance, AU
        returns:
           Omega : 2 Pi AU / yr
        '''
        return np.sqrt(self.mass / (r*r*r))

    def v_k(self,  r):
        '''Keplerian velocity of a test particle.
        
        args:
            r : distance, AU
        returns:
           Omega : 2 Pi AU / yr
        '''
        return np.sqrt(self.mass / r)



    def r_Hill(self, R, M):
        '''Compute the hill radius of a planet

        args:
            R : radius, AU
            M : planet mass
        '''
        return R * (M / (3*self.mass))**(1/3.)



    def _io_star_parameters(self, mode):
        if mode == 'write':
            self.io_star_attributes = self.star_par
            self.io_star_data = {'mass': self.mass,
                                 #'L_x': self.L_x,
                                 'teff': self.teff,
                                 'llum': self.llum,
                                 'age': self.age,
                                 'mdot': self.mdot,
                                 'mass_mdot': self.mass_mdot,
                                 }
        elif mode == 'read':
            self.star_par = self.io_star_attributes
            self.mass = self.io_star_data['mass']
            #self.L_x = self.io_star_data['L_x']
            self.teff = self.io_star_data['teff']
            self.llum = self.io_star_data['llum']
            self.age = self.io_star_data['age']
            self.mdot = self.io_star_data['mdot']
            self.mass_mdot = self.io_star_data['mass_mdot']

    #
    # Method to write/read data to hdf5
    def io_star_hdf5(self, myhdf5file, operation, i_pop, i_time, i_yso):
        #
        #
        if operation == 'write':
            self._io_star_parameters(operation)
            self.outfile.write_data_to_hdf5(self.outfile.star_paths_list[i_pop][i_time][i_yso],
                                            self.io_star_data, self.io_star_attributes)
        elif operation == 'read':
            if not self.outfile:
                self.outfile = OutfileLeonardo(myhdf5file)
            self.io_star_data, self.io_star_attributes = self.outfile.read_data_from_hdf5(self.outfile.star_paths_list[i_pop][i_time][i_yso])
            self._io_star_parameters(operation)
#            tracknames = self.star_par['pmstracks']
            #self.star_par['pmstracks'] = PMSTracks(tracks=tracknames, verbose=False)
            self.pmst = self.star_par['pmstracks']
            pass
        else:
            raise ValueError("Error io in Star: operation has to be read/write (operation={})".format(operation))


    #
    # Method that changes the stellar parameters
    def evolve(self, delta_t):
        new_age = self.age + delta_t
        self.mass, self.llum, self.teff = self.evolved_par(new_age)
        self.age = new_age

    #
    # Star not evolving, just changing age
    #   returns constant parameters, except age
    def constant_star(self, new_age):
        #
        #
        return self.mass, self.llum, self.teff

    #
    # Star evolving through the pmstracks, changing age and photospheric parameters
    def pmstracks_star(self, new_age):
        #
        # Change mass if mdot is different from 0.0
        self.mass_mdot = self.mass_mdot + self.mdot * (new_age - self.age)
        if self.mdot_evolution:
            new_mass = self.mass_mdot
        else:
            new_mass = self.mass
        #
        # Calls the track interpolation method
        new_llum, llum_stat, llum_message = self.pmst.interpolator_bilinear(new_mass, np.log10(new_age), 'llum')
        new_teff, teff_stat, teff_message = self.pmst.interpolator_bilinear(new_mass, np.log10(new_age), 'teff')
        #
        if (llum_stat != 0) or (teff_stat != 0):
            print('PMSTracks limits warning: {0}:{1}, {2}:{3}'.format(llum_stat, llum_message, teff_stat, teff_message))
        #
        # returns the updated parameters
        return new_mass, new_llum, new_teff

    #
    # Method to estimate the safe timestep to evolve the star so that
    #   stellar parameters change by less than partoler
    #   returns True/False if the timestep is ok (or not) and the guess timestep
    #   to meet the requirement (obtained by linear expansion/guess)
    def check_time_step(self, delta_t, partoler=0.05):
        new_age = self.age + delta_t
        new_mass, new_llum, new_teff = self.evolved_par(new_age)
        mst, mdt = self._par_ev_check(self.mass, new_mass, delta_t, partoler)
        lst, ldt = self._par_ev_check(10.**self.llum, 10.**new_llum, delta_t, partoler)
        tst, tdt = self._par_ev_check(self.teff, new_teff, delta_t, partoler)
        #
        return (mst and lst and tst), min([mdt, ldt, tdt]), \
               [mst, mdt, self.mass - new_mass, lst, ldt, self.llum - new_llum, tst, tdt, self.teff - new_teff]

    @staticmethod
    def _par_ev_check(old_par, new_par, delta_t, partoler):
        #
        dp = abs(old_par - new_par)/abs(old_par)
        #
        if dp <= partoler:
            check = True
        else:
            check = False
        #
        if dp != 0.:
            guess_dt = partoler/dp * delta_t
        else:
            guess_dt = delta_t
        #
        return check, guess_dt


    # method to compute Rstar
    # Rstar is returned in Solar radii
    def compute_rstar(self):
        #
        # sigma = 5.6704e-5  #  Stefan-Boltzmann constant in erg s-1 cm-2 K-4
        # rsun = 6.96e10     #  Rsun in cm
        # lsun = 3.826e+33   #  Lsun in erg s-1
        # f = np.sqrt(lsun/(4.*np.pi*sigma))/rsun
        f = 33292887.502709724
        #lstar = 10.**self.llum
        return f*np.sqrt(1./self.teff**4.)

