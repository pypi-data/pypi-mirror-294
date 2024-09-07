#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from scipy.integrate import cumtrapz
import os.path
import multiprocessing as mp

from .yso import YSO
from .pmstracks.pmstracks.pmstracks import PMSTracks
from .io_diskpop import OutfileLeonardo
from .DiscEvolution.src.constants import Msun, G, Mearth, AU, yr

def select_parameters(key, params, defaults):
    try:
        return params[key]
    except KeyError:
        return defaults[key]


def evol_one_yso(args):
    # This wrapper function is used in the multiprocessing version to
    # call the right method to evolve a single yso to a given target age

    evolve_to = args[0]._yso_age_at_time(args[1].target_age, args[2])
    if evolve_to > 0.:
        args[1].evolve(evolve_to)
        args[1].born = True
        args[1].evol_status="Evolved from {0} to {2} (evolved for {2})".format(args[1].target_age, args[2], evolve_to)
    else:
        args[1].evol_status="Remained at {0}, evolve_to {1}".format(args[1].target_age, evolve_to)
    return args[1]


class Population(object):
    """
    Docstring

    """

    def __init__(self, parameters_user, default_pars, outfile_name = None):
        """
        Docstring

        """

        #
        # fill in the parameters, using defaults as appropriate
        self.parameters = {key: select_parameters(key, parameters_user, default_pars) for key in
                           default_pars}
        
        if self.parameters['parallel_evol']:
            if self.parameters['all_available_proc']:
                self.parameters['nprocs'] = mp.cpu_count()

        self.parameters['ntimes'] = len(self.parameters['times_snapshot'])

        self._alpha = self.parameters['alpha']
        self._leverarm = self.parameters['leverarm']

        if self.parameters['init'] == True:
            self.kroupa_imf_initialize(self)

        #
        # Save the status of the random number generator at runtime I THINK THIS IS OUTDATED
        if self.parameters['set_rand_state']:
            if not self.parameters['initial_rand_state']:
                raise ValueError("Need to specify a valid initial random state")
            else:
                np.random.set_state(self.parameters['initial_rand_state'])
        #
        self.initial_rand_state = np.random.get_state()

        #
        # Define population run type
        self._def_population_type()

        #
        # Define IMF
        self._IMF_type()
        
        #
        # Define Star Formation History
        self._def_sfh_type()

        #
        # Define method to select PMS tracks
        self._def_pmst_method()

        # Define method to select alpha
        self._def_alpha_method()

        #
        # define output file, returns False if the run will not
        #    write an output file and True otherwise
        self.do_write = self._setup_outfile(outfile_name)

    # Evolve each YSO by a dt (how many real internal timesteps are required is decided by each YSO internally)
    def evolve_dt(self, dt):
        for myyso in self.ysos:
            myyso.evolve(myyso.star.age+dt)

    def evolve_to_age(self, time):
        for myyso in self.ysos:

            evolve_to = self._yso_age_at_time(myyso.target_age, time)
            if evolve_to > 0.:
                myyso.evolve(evolve_to)
                myyso.born = True
            else:
                pass

    def evolve_to_age_mp(self, time):
        # This function is used in the parallel version to
        # evolve YSOs in parallel at each time step the input "time" is the
        # age of the population to evolve to

        nproc = min(len(self.ysos),self.parameters['nprocs'])

        myargs = []
        for yso in self.ysos:
            yso.evol_status = "Not yet evolved"
            myargs.append([self, yso, time])

        with mp.Pool(nproc) as p:
            self.ysos = p.map(evol_one_yso, myargs)

    def _yso_age_at_time(self, target_age, time):
    #
    # Returns the time to evolve the YSO to.
    # - self.parameters['age'] is the actual age of the region of interest, e.g. 3 Myr for Lupus (its dimension is Myr so in this case self.parameters['age'] = 3).
    # - time is the age at which we want to know the disc properties (e.g. 5 Myr - can be more or less than the actual age of the region of interest, it's theoretical in a sense).
    # - target_age is the age of the single YSO when evolved inside of its region: it is extracted by get_target_age, using a constant/normal/lognormal method with mean value self.parameters['age'] and spread self.parameters['sage'].
    # This means that target_age - self.parameters['age'] returns the spread in the YSO age with respect to the age of the region, and adding this spread to time gives the age to which the YSO must be evolved. If the star is not born yet at t = time, the returned age is < 0.
    # Yso age at time mean: at t = time, how old is the yso? Its age is not necessarily equal to time, it depends on the time when it was born.

        return time + (target_age - self.parameters['age']*1.e6)

    #
    # Setup the output file and return the value for
    #    whether the run will write output or not
    def _setup_outfile(self, outfile_name):				# Setting the output filename. Usually passed thought the
        #								# constructor, else defined hereby.
        file_set = False
        if not outfile_name:
            self.outfile_name = None
            self.outfile = None
        else:
            self.outfile_name = outfile_name
            self.outfile = OutfileLeonardo(outfile_name)
            self.outfile.create_file(self.parameters)
            file_set = True
        #
        return file_set

    #
    # Select method for producing alpha (Shakura & Sunyaev 1973)
    #     single:   single value
    #     normal: normal distribution
    #     lognormal:   lognormal distribution
    def _def_alpha_method(self):
        if self.parameters['alpha_method'] == 'lognormal':
            self.get_alpha = self.lognormal
        elif self.parameters['alpha_method'] == 'flat':
            self.get_alpha = self.flat
        elif self.parameters['alpha_method'] == 'normal':
            self.get_alpha = self.normal
        elif self.parameters['alpha_method'] == 'single':
            self.get_alpha = self.single
        else:
            raise ValueError("Alpha distribution type {} not available".format(self.parameters['alpha_method']))
        
    #
    # Select the type of population to produce
    #     snapshot:   a single population where each YSO has been evolved to its prescribed age
    #     evolving:   an evolving population with a set of snapshots as the population is evolved
    def _def_population_type(self):
        if self.parameters['pop_type'] == 'snapshot':
            self.pop_gen = self.generate_snapshot
        elif self.parameters['pop_type'] == 'evolving':
            self.pop_gen = self.generate_evolving
        else:
            raise ValueError("Population type {} not available".format(self.parameters['pop_type']))
            
    #
    # Initialise the stellar mass array, depending on the chosen IMF.
    #       
    #
    def _IMF_type(self):
        if self.parameters['options.MONTECARLO'] == False or self.parameters['imf'] == 'custom':
            self._init_mstar = self.custom_imf_population        
        elif self.parameters['imf'] == 'single':
            self._init_mstar = self.single_imf_population
        elif self.parameters['imf'] == 'kroupa':
            self._init_mstar = self.kroupa_imf_population

        else:
            raise ValueError("IMF type {} not available".format(self.parameters['imf']))

    #
    # Select the Star Formation History prescription
    #     constant:  uniform from age-sage to age+sage
    #     normal:    gaussian centered at age and with sigma=sage
    #     lognormal: log10(age) is normal centered at log10(age) and with sigma=sage
    def _def_sfh_type(self):
        if self.parameters['sfh'] == 'constant':
            self.get_target_age = self.const_sfh
        elif self.parameters['sfh'] == 'normal':
            self.get_target_age = self.normal_sfh
        elif self.parameters['sfh'] == 'lognormal':
            self.get_target_age = self.lognormal_sfh
        else:
            raise ValueError("SFH type {} not available".format(self.parameters['sfh']))

    #
    # Select pms tracks selection method
    #     simple:   one set of pmstracks for the whole population
    def _def_pmst_method(self):
        if self.parameters['tracks_select'] == 'single':
            self.mypmst = PMSTracks(tracks=self.parameters['pmst'], verbose=False)
            self.get_pmst = self.simple_pmst
        else:
            raise ValueError("PMST type {} not available".format(self.parameters['pmst']))
            
    #
    # Initialise the betas array. If you have a file -> read from it, if not make an array with the chosen distribution but this will not make any sense so just one option
    #       
    #
    # def _betas_type(self):
    #     #opzione 1: leggi da file - to be implemented
    #     # #opzione 2: calcoli con Mstar
    #     # #opzione 3: tutti i beta sono 1 OPPURE tutti i beta sono 0 (se non hai MHD)
    #     # if self.parameters['options.MHD'] == False or self.parameters['options.MONTECARLO'] == False:
    #     #     self._init_beta_mag = self.single_beta_mag
    #     # else:
    #     #     self._init_beta_mag = self.beta_mag_corr


    #     # if self.parameters['options.MONTECARLO'] == False or self.parameters['imf'] == 'custom':
    #     #     self._init_mstar = self.custom_imf_population        
    #     # elif self.parameters['imf'] == 'single':
    #     #     self._init_mstar = self.single_imf_population
    #     # elif self.parameters['imf'] == 'kroupa':
    #     #     self._init_mstar = self.kroupa_imf_population

    #     # else:
    #     #     raise ValueError("IMF type {} not available".format(self.parameters['imf']))

    #
    # Select method for producing the magnetisation parameter beta - NO CORRELATION
    #     lognormal: lognormal distribution
    #     normal: normal distribution
    #     flat: flat distribution
    #     single: single value

    # def get_beta_mag_nocorr(self):
    #     if self.parameters['options.MHD'] == False:
    #         beta_mag = 0
    #     else:
    #         beta_mag = 1
    #     return beta_mag


#######################################################

    #
    # Method to generate a snapshot
    def generate_snapshot(self):
        """
        Docstring


        """
        self.generate_population()

        new_write = True
        for i_time in range(len(self.parameters['times_snapshot'])):

            time = 1.e6 * self.parameters['times_snapshot'][i_time]
            print("Step {0} of {1}: evolving to age = {2}".format(i_time+1, len(self.parameters['times_snapshot']), time/(2*np.pi*1e6))," Myr") # HERE I HAVE TO DIVIDE BY 2PI TO HAVE TIME IN MYR

            if self.parameters['parallel_evol']:
                self.evolve_to_age_mp(time)
            else:
                self.evolve_to_age(time)

            if self.do_write:								   # Writing data on the output file.
                self.io_pop_hdf5(self.outfile_name, 'write', 0, i_time, newpop=new_write)
                new_write = False

    #
    # This method generates a population using the parameters provided
    def generate_population(self):
        self.ysos = []
        
        self._init_mstar(self)
        #self._init_betas(self)

        for yso_index in range(self.parameters['nysos']):
            yso_id = str(yso_index)  # Unique identifier
            yso_type = 'ClassII'

            #
            yso_parameters = self._generate_yso_pars(yso_index)
            yso_parameters.update({'yso_id': yso_id, 'yso_type': yso_type,})
            self.ysos.append(self.generate_yso(yso_parameters, self.parameters['init']))

    def _generate_yso_pars(self, index):
        target_age = self.get_target_age(self.parameters['age'], self.parameters['sage'])
        return {'target_age': target_age, #'evolve_at_generation': self.parameters['evolve_at_generation'],
                'no_default': self.parameters['yso_no_default'],
                'outfile': self.outfile, 'index': index, 'flag_dispersion': False
                }

    #
    # private method to convert-read the parameters that we want to read/write in the hdf5 file
    #    for the populations.
    def io_pop_hdf5(self, myhdf5file, operation, i_pop, i_time, newpop=True):
        #
        if operation == 'write':
            if newpop:

                self.io_pop_data_to_write = {'ages': self.parameters['age']}

                self.outfile.write_data_to_hdf5(self.outfile.pop_paths[i_pop],
                                            self.io_pop_data_to_write, self.parameters)
            for i_yso in range(self.parameters['nysos']):
                self.ysos[i_yso].io_yso_hdf5(myhdf5file, operation, i_pop, i_time, i_yso)

        elif operation == 'read':
            if not self.outfile:
                self.outfile = OutfileLeonardo(myhdf5file)
            self.io_pop_data_to_write, self.parameters = self.outfile.read_data_from_hdf5(
                                                   self.outfile.pop_paths[i_pop])

            self.parameters['age'] = self.io_pop_data_to_write['ages']
            
            self.ysos = []

            for i in range(self.parameters['nysos']):
                yso_id = str(i)
                yso_data, yso_pars_read_from_hdf5 = self.outfile.read_data_from_hdf5(
                                                     self.outfile.yso_paths_list[i_pop][i_time][i])
                yso_type = yso_pars_read_from_hdf5['yso_type']
                yso_parameters = self._generate_yso_pars(index=i)
                yso_parameters.update({'yso_id': yso_id, 'yso_type': yso_type})
                self.ysos.append(self.generate_yso(yso_parameters, False))
                self.ysos[i].io_yso_hdf5(self.outfile_name, operation, i_pop, i_time, i)
        else:
            raise ValueError("Error io in Population: operation has to be read/write (operation={})".format(operation))


    def generate_evolving(self, delta_t, **kwargs):
        """
        Docstring


        """
        pass


    #
    # Method to generate a YSO

    def generate_yso(self, yso_parameters, init):

        flag_dispersion = False
       
        if init == True:
            
            mstar = self.get_mstar(self, yso_parameters['index'])

            pmst = self.get_pmst(mstar)

            # Splitting into correlation/no correlation to account for the different types of extraction of the parameters

            if self.parameters['corr'] == True:
                self._beta_mag = self.get_parameter_corr(self, mstar, 'beta_mag', self.parameters['beta_mag_method'], self.parameters['beta_mag_slope'], self.parameters['beta_mag_norm'], self.parameters['beta_mag_spread'])
            else:
                self._beta_mag = self.get_parameter_nocorr(self, self.parameters['beta_mag_method'], self.parameters['beta_mag_mean'], self.parameters['beta_mag_spread'])
        

            # MHD parameters
            
            self._alpha_DW = self.get_alpha_DW(self._beta_mag)
        
            if self._alpha != 0:
                self._psi = self._alpha_DW/self._alpha
                self._xi = (self._psi+1)/4. * (np.sqrt(1 + (4.*self._psi)/((self._leverarm-1)*(self._psi+1)**2)) -1)

            else:
                self._xi = 1/(2*(self._leverarm - 1))
            # MHD parameters - end

            self.rdisc_corr_initialize(self)

            solarToCodeMass = 2e33/(1.5e13)**2

            if self.parameters['corr'] == True:
                mdisc = self.get_parameter_corr(self, mstar, parameter = 'mdisc', parameter_method = self.parameters['mdisc_method'], parameter_slope = self.parameters['mdisc_slope'], parameter_normalisation = self.parameters['mdisc_norm'], parameter_spread = self.parameters['mdisc_spread'])
                rdisc = self.get_parameter_corr(self, mstar, parameter = 'rdisc', parameter_method = self.parameters['rdisc_method'], parameter_slope = self.parameters['rdisc_slope'], parameter_normalisation = 0,  parameter_spread = self.parameters['rdisc_spread'])
                mdot_photoev = self.get_parameter_corr(self, mstar, parameter = 'mdot_photoev', parameter_method = self.parameters['mdot_photoev_method'], parameter_slope = self.parameters['mdot_photoev_slope'], parameter_normalisation = self.parameters['mdot_photoev_norm'],  parameter_spread = self.parameters['mdot_photoev_spread'])
                L_x = self.get_parameter_corr(self, mstar, parameter = 'L_x', parameter_method = self.parameters['L_x_method'], parameter_slope = self.parameters['L_x_slope'], parameter_normalisation = self.parameters['L_x_norm'],  parameter_spread = self.parameters['L_x_spread'])
            else:
                mdisc = solarToCodeMass*self.get_parameter_nocorr(self, parameter_method = self.parameters['mdisc_method'], mean = self.parameters['mdisc'], spread = self.parameters['mdisc_spread'])
                rdisc = self.get_parameter_nocorr(self, parameter_method = self.parameters['rdisc_method'], mean = self.parameters['rdisc_mean'], spread = self.parameters['rdisc_spread'])
                mdot_photoev = self.get_parameter_nocorr(self, parameter_method = self.parameters['mdot_photoev_method'], mean = self.parameters['mdot_photoev_mean'], spread = self.parameters['mdot_photoev_spread'])
                L_x = self.get_parameter_nocorr(self, parameter_method = self.parameters['L_x_method'], mean = self.parameters['L_x_mean'], spread = self.parameters['L_x_spread'])

        elif init == False:
        
            mstar = 1
            pmst = self.get_pmst(mstar)
            rdisc = 1
            mdisc = 1
            self._alpha = 1e-3
            self._alpha_DW = 1e-3
            self._beta_mag = 1e-5
            mdot_photoev = self.get_parameter_nocorr(self, parameter_method = self.parameters['mdot_photoev_method'], mean = self.parameters['mdot_photoev_mean'], spread = self.parameters['mdot_photoev_spread'])
            L_x = self.get_parameter_nocorr(self, parameter_method = self.parameters['L_x_method'], mean = self.parameters['L_x_mean'], spread = self.parameters['L_x_spread'])
            
        star_parameters = {'mass': mstar,
                           'age': self.parameters['initial_stellar_age'],
                           #'L_x': L_x,
                           'pmstracks': pmst,
                           'mdot_evolution': self.parameters['star_mdot_evolution'],
                           'mdot': self.parameters['mdot'],
                           'reset_lt': self.parameters['reset_lt'],
                           'evolve_method': self.parameters['star_evolve_method'],
                           'no_default': self.parameters['star_no_default'],
                           'parent_yso': yso_parameters['yso_id'],
                           'outfile': self.outfile,}
        disc_parameters = {'rin': self.parameters['rin_disc'],  			# Inner radius of the disc [au]
                           'rout': self.parameters['rout_disc'],  			# Outer radius of the disc [au]
                           'nr': self.parameters['nr_disc'],  				# Number of points in radial grid
                           'spacing': self.parameters['rd_spacing'],  		# Type of spacing of the grid
                           'alpha': self._alpha,  							# Shakura & Sunayev (1973) alpha parameter
                           'beta_mag': self._beta_mag,                      # Beta magnetisation parameter
                           'alpha_DW': self._alpha_DW,                      # Tabone et al. (2022) alpha disc wind parameter
                           'leverarm': self.parameters['leverarm'],         # Tabone et al. (2022) lever arm parameter (lambda)
                           'omega': self.parameters['omega'],               # Tabone et al. (2022) omega parameter: alpha_DW \propto \Sigma_c^{-\omega}
                           'mdot_photoev': mdot_photoev,                    # Internal photoevaporation mass loss rate
                           'L_x': L_x,
                           'limit_discmass': self.parameters['limit_discmass'],
                           'analytic': self.parameters['analytic'], 		# Whether to use analytic solution
                           'beta': self.parameters['beta'],                 # Power-law index of H/R with Mstar (H/R \propto M_{\star}^{\beta})
                           'SlopeCs': self.parameters['SlopeCs'],  			# Slope of the sound speed with radius
                           'Hr0': self.parameters['Hr0'],  					# H/R at R = 1 au
                           'Rd': rdisc,  									# Initial scaling radius of the disc [au]
                           'Md': mdisc, 									# Initial disc mass [Msun]
                           'd2g': self.parameters['d2g'],         			# Dust-to-gas ratio
                           'feedback': self.parameters['feedback'],   		# Feedback of the dust onto the gas
                           'dust': self.parameters['dust'],  				# Whether to use dust
                           'outfile': self.outfile,
                           'gamma': self.parameters['gamma'],
                           }

        return YSO({'star': star_parameters, 'disc': disc_parameters, 'yso': yso_parameters})

    #
    # Methods for deciding which pmst tracks to use
    #  ToDo: implement a method that allows to use different sets of tracks for different masses
    #
    def simple_pmst(self, mstar):
        #
        # ToDo catch a problem with mstar out of tracks
        #
        return self.mypmst

    # IMF methods

    #
    # Obtaining the value of the stellar mass for a given YSO of index i
    #
    #
    @staticmethod
    def get_mstar(self, i):
        return self._mstar_array[i]
        
    #
    # Single IMF: sets _mstar_array to be an array of ones.
    #
    #
    @staticmethod
    def single_imf_population(self):
        self._mstar_array = np.ones(self.parameters['nysos'])
        return 0
        
        
        
    #
    # Custom IMF: sets _mstar_array reading from the file mstar.txt
    #
    #
    @staticmethod
    def custom_imf_population(self):
    
        masses = []
  
        if not os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'mstar.txt')):
            raise ValueError("File 'mstar.txt' does not exist - please, fill it with the custom stellar masses")
        else:
            masses = np.loadtxt(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'mstar.txt')))

        if len(masses) != self.parameters['nysos']:
            self.parameters['nysos'] = len(masses)
            
        self._mstar_array = np.zeros((len(masses)))
        
        length = np.arange(0, len(masses))
        inc = 0
        for i, mass in zip(length, masses):
            inc += 1
            self._mstar_array[i] = mass
            

    # 
    # Kroupa IMF: setting where the power-law changes
    #
    #
    @staticmethod
    def kroupa_set_limits(self):

        self._limits = np.zeros(8)

        self._limits[0] = self.parameters['mmin']			# Liminf_0: set by the user, needs to be lower than the first step of the IMF (0.08 Msun)
        self._limits[1] = 0.08                    		    # Limsup_0: hard-coded, it's in the Kroupa IMF definition
        self._limits[2] = self._limits[1]						    # Liminf_1
        self._limits[3] = 0.5                     		    # Limsup_1: hard-coded, it's in the Kroupa IMF definition
        self._limits[4] = self._limits[3]						    # Liminf_2
        self._limits[5] = 1                           	    # Limsup_2: hard-coded, it's in the Kroupa IMF definition
        self._limits[6] = self._limits[5]						    # Liminf_3
        self._limits[7] = self.parameters['mmax']			# Limsup_3: set by the user, needs to be higher than the last step of the IMF (1 Msun)

        return 0
            

    #
    # Kroupa IMF: sets _mstar_array to be an array of random numbers generated through the Kroupa initial mass function.
    #
    #
    @staticmethod
    def kroupa_imf_population(self): # CAMBIA NOME

        masses_0 = np.linspace(self._limits[0], self._limits[1], 100)
        masses_1 = np.linspace(self._limits[2] + 1e-10, self._limits[3], 100)
        masses_2 = np.linspace(self._limits[4] + 1e-10, self._limits[5], 100)
        masses_3 = np.linspace(self._limits[6] + 1e-10, self._limits[7], 100)
        masses = np.concatenate((masses_0, masses_1, masses_2, masses_3))

        # Creating the PDF and CDF through the self methods

        pdf = self.pdf_imf(self, masses, self._limits)
        cdf = self.cdf_imf(self, masses, masses_0, masses_1, masses_2, masses_3, self._limits)

        # Actually extracting the random number!

        y = np.random.rand(self.parameters['nysos'])
        x = np.zeros(self.parameters['nysos'])

        for i in range(0, self.parameters['nysos']):
            index = np.searchsorted(cdf, y[i])
    
            ind0 = np.int(index)-1
            ind1 = np.int(index)

            y0 = cdf[ind0]
            y1 = cdf[ind1]
            x0 = masses[ind0]
            x1 = masses[ind1]

            x[i] = (x1-x0)/(y1-y0)*y[i] - (x1-x0)/(y1-y0)*y0 + x0
            
        self._mstar_array = x
        return 0


    #
    # Method to evaluate the constants involved in the Kroupa IMF - a, b, c for continuity and k for normalization (see documentation)
    #
    #
    @staticmethod
    def kroupa_imf_initialize(self):

        # Number of stars to be extracted
        
        N = self.parameters['nysos']
        self.kroupa_set_limits(self)

        # Mass thresholds at which the slope of the IMF changes: the extremes are set by the user, the steps are hard-coded from the Kroupa definition.

        # Slopes in the different mass regimes: hard-coded, come from the Kroupa IMF definition.

        self._mslope_0 = 0.3
        self._mslope_1 = 1.3
        self._mslope_2 = 1.3
        self._mslope_3 = 2.3

        # Arrays of masses to evaluate the IMF and the integral for normalization

        masses_0 = np.linspace(self._limits[0], self._limits[1], 100)
        masses_1 = np.linspace(self._limits[2] + 1e-10, self._limits[3], 100)
        masses_2 = np.linspace(self._limits[4] + 1e-10, self._limits[5], 100)
        masses_3 = np.linspace(self._limits[6] + 1e-10, self._limits[7], 100)
        masses = np.concatenate((masses_0, masses_1, masses_2, masses_3))

        # Array of constants (in the doc: a, b, c) needed to have a continuous IMF
    
        self.parameters['imf_consts'][0] = 1.
        self.parameters['imf_consts'][1] = self.parameters['imf_consts'][0]*(self._limits[1])**(-self._mslope_0)/(self._limits[2])**(-self._mslope_1)
        self.parameters['imf_consts'][2] = self.parameters['imf_consts'][1]*((self._limits[3])**(-self._mslope_1)/(self._limits[4])**(-self._mslope_2))
        self.parameters['imf_consts'][3] = self.parameters['imf_consts'][2]*((self._limits[5])**(-self._mslope_2)/(self._limits[6])**(-self._mslope_3))

        # Array of integrals to evaluate the constant k for normalization

        integral = np.zeros(4)

        integral[0] = np.trapz(self.pdf_imf(self, masses_0, self._limits), masses_0, dx = 0.0001)
        integral[1] = np.trapz(self.pdf_imf(self, masses_1, self._limits), masses_1, dx = 0.0001)
        integral[2] = np.trapz(self.pdf_imf(self, masses_2, self._limits), masses_2, dx = 0.0001)
        integral[3] = np.trapz(self.pdf_imf(self, masses_3, self._limits), masses_3, dx = 0.0001)

        self.parameters['imf_consts'][4] = 1/(integral[0]+integral[1]+integral[2]+integral[3])

        return 0

    #
    # Method to evaluate the PDF through the Kroupa IMF - UNNORMALIZED
    #
    #
    @staticmethod
    def pdf_imf(self, masses, limits): # this gives me the PDF

        p = np.zeros(len(masses))
        alpha = 0
        constant = self.parameters['imf_consts']
    
        for i in range(0, len(masses)):
            if self._limits[0] <= masses[i] < self._limits[1]:
                alpha = self._mslope_0
                constant = self.parameters['imf_consts'][0]
            elif self._limits[2] <= masses[i] < self._limits[3]:
                alpha = self._mslope_1
                constant = self.parameters['imf_consts'][1]
            elif self._limits[4] <= masses[i] < self._limits[5]:
                alpha = self._mslope_2
                constant = self.parameters['imf_consts'][2]
            elif masses[i] >= limits[6]:
                alpha = self._mslope_3
                constant = self.parameters['imf_consts'][3]

            p[i] = (constant*masses[i]**(-alpha))/self.parameters['nysos']
        
        return p


    #
    # Method to evaluate the CDF of the Kroupa PDF
    #
    #
    @staticmethod
    def cdf_imf(self, masses, masses_0, masses_1, masses_2, masses_3, limits):
        #
        pdf = self.pdf_imf(self, masses, limits)
        return cumtrapz(self.parameters['imf_consts'][4]*pdf, masses, initial = 0)


    #
    # Star formation history methods
    @staticmethod
    def const_sfh(age, sage):
        #
        return 1.e6*((age-sage) + np.random.random()*(2.*sage))

    @staticmethod
    def normal_sfh(age, sage):
        #
        return 1.e6*(age + np.random.randn() * sage)

    @staticmethod
    def lognormal_sfh(age, sage):
        #
        return 1.e6*10**(np.log10(age) + np.random.randn() * np.log10(sage))

    #
    # Random methods
    @staticmethod
    def single(x, dx):
        #
        return x

    @staticmethod
    def flat(x, dx):
        #
        return (x-dx) + np.random.random()*(2.*dx)

    @staticmethod
    def normal(x, sig):
        #
        return x + np.random.randn() * sig

    @staticmethod
    def lognormal(lx, sig):
        if lx == 0:
            return 0
        else:
        #
            return 10**(np.log10(lx) + (np.random.randn() * sig))

    
    @staticmethod
    def get_parameter_corr(self, mstar, parameter, parameter_method, parameter_slope, parameter_normalisation, parameter_spread):

        conversion = 1

        if parameter == 'beta_mag':
            parameter_normalisation = np.log10(parameter_normalisation)
            if self.parameters['options.MHD'] == False:
                return 0
            
        elif parameter == 'mdisc':
            solarToCodeMass = 2e33/(1.5e13)**2	
            conversion = Mearth*solarToCodeMass/(self.parameters['d2g']*Msun)
            q_Ansdell = np.log10(parameter_normalisation*Msun*self.parameters['d2g']/Mearth)    # For how the correlation is defined, the normalisation is actually 10**q_Ansdell - hence this calculation, to translate the input normalisation [Msun]
            parameter_normalisation = q_Ansdell                      

        elif parameter == 'rdisc':
            conversion =  self.parameters['rdisc_msun']

        elif parameter == 'mdot_photoev':
            if parameter_normalisation == 0:
                return 0
            else:
                parameter_normalisation = np.log10(parameter_normalisation)

        elif parameter == 'L_x':
            if parameter_normalisation == 0:
                return 0
            else:
                parameter_normalisation = np.log10(parameter_normalisation)


        mean = mstar**(parameter_slope)*10**(parameter_normalisation)*conversion

        result = self.draw_from_distribution(self, parameter_method, mean, parameter_spread)

        return result
    

    @staticmethod
    def get_parameter_nocorr(self, parameter_method, mean, spread):
        result = self.draw_from_distribution(self, parameter_method, mean, spread)
        return result
    

    @staticmethod
    def draw_from_distribution(self, parameter_method, mean, spread):
        
        if parameter_method == 'lognormal':
            result = self.lognormal(mean, spread)

        elif parameter_method == 'normal':
            result = self.normal(mean, spread)

        elif parameter_method == 'flat':
            result = self.flat(mean, spread)   

        return result


    #
    # Select method for producing alpha (Shakura & Sunyaev 1973)
    #     single:   single value
    #     normal: normal distribution
    #     lognormal:   lognormal distribution
    def get_alpha_DW(self, beta_mag):   
        if beta_mag == 0:
            return 0
        else:    
            # Eq. 69 in Tabone et al. 2022a: we are neglecting the radial dependence, hence the Hr0 in the formula. If we do want to include it, then we need to use H/R at all radii
            alpha_DW = 2e-3*(beta_mag/1e4)**(-1)*(self.parameters['Hr0']/0.1)**(-1)
            return alpha_DW


    @staticmethod
    def rdisc_corr_initialize(self):
        #       
        G1 = 6.67*10**(-8)								            # cm^3/(g s^2)
        R0 = 1.											            # R0 [AU]
        Mdot_at_Msun = 10**(self.parameters['log_mdot_norm'])
        Mdot_at_Msun_cgs = Mdot_at_Msun*Msun/yr                     # Mdot for a solar mass star (Manara et al. 2017) [g/s]

        # Finding the slope of the Rc-Mstar correlation

        self._mu = self.parameters['mdisc_slope'] - self.parameters['mdot_slope'] + 0.5 + 2*self.parameters['beta']   # slope of tnu with Mstar, which coincides with delta_0 in the purely viscous case

        self.parameters['rdisc_slope'] = self._mu/(self._xi + 1)

        # Finding Rc for a solar mass star - R_{c, M_{\odot}} both in cm and in AU

        if self.parameters['alpha'] != 0:
            q_Ansdell = np.log10(self.parameters['mdisc_norm']*Msun*self.parameters['d2g']/Mearth)
            rdisc_msun_cm = (1/(Mdot_at_Msun_cgs))*(3/2)*np.sqrt(G1*Msun/(R0*AU))*(10**(q_Ansdell)*Mearth)*(2-self.parameters['gamma'])*self.parameters['alpha']*(self.parameters['Hr0'])**2/(self.parameters['d2g'])
            rdisc_msun_au = rdisc_msun_cm/AU
        else:
            rdisc_msun_au = 15.
        
        self.parameters['rdisc_msun'] = rdisc_msun_au

        return 0
