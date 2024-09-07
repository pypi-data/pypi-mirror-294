##################################################
##
##    DISKPOP - A population synthesis code for protoplanetary discs
##    
##
##    Question or bugs? Please contact the diskpopteam:
##    
##    G. Rosotti         g.rosotti@leicester.ac.uk
##    M. Tazzari         mtazzari@ast.cam.ac.uk
##    C. Toci            claudia.toci@inaf.it
##    A. Somigliana      alice.somigliana@eso.org
##    L. Testi           ltesti120a@gmail.com
##    G. Lodato          giuseppe.lodato@unimi.it
## 
##################################################

options = type('test', (object,), {})()

##################################################

default_pars = {'init': True,                         # Whether to initialize or not the IMF (always True, except in analysis)
               'pop_type': 'snapshot',  			  # Type of population evolution
               'corr': True,                          # Correlation - can be True or False
               'times_snapshot': [0, 1.],			  # Times for writing the population properties (in Myr/2pi)
               'pop_id': 'test_pop',  				  # Population ID string
               'npops': 1,         					  # Number of stars in population - I really don't think so
               'nysos': 2,         					  # Number of stars in population

               'mmin': 1.e-2,        				  # Minimum stellar mass [Msun]
               'mmax': 50.,        					  # Maximum stellar mass [Msun]
               'imf': 'single',      				  # Chosen prescription for the IMF (if 'single' = we're not performing MC; if 'custom' = stellar masses are custom chosen)
               'imf_consts': [0., 0., 0., 0., 0.],	  # Initialization of array of constants for the IMF (continuity, norm)

               'mstar': 1,

               'beta': -0.5,						  # Slope of H/R with Mstar (H/R \propto M_{\star}^{\beta}) (tested values: 0, -0.5, -0.425)
               
               'mdisc_mean': 0.05,                    # Initial disc mass [Msun] - No correlation
               'mdisc_method': 'lognormal',           # Distribution of initial disc masses - Either correlation or no correlation
               'mdisc_spread': 0.5,                   # Initial disc mass dispersion (dex)
               'mdisc_norm': 5e-3,					  # Alpha parameter for the Mdisc-Mstar correlation (Ansdell+ 2017)
               'mdisc_slope': 1.7,					  # Beta parameter for the Mdisc-Mstar correlation (Ansdell+ 2017) 
               
               'log_mdot_norm': -8.44,                # Logarithm(base 10) of the normalisation of the accretion rate
               'mdot_slope': 2.,					  # Slope of Mdot with Mstar (\dot M \propto M_{\star}^{\mdot_slope}) (typically 2 \pm 0.2)

               'beta_mag_method': 'lognormal',        # Distribution of beta (where beta is the magnetisation)
               'beta_mag_slope': -1,                  # Slope of beta with Mstar (\beta \propto M_{\star}^{\beta_mag_slope})
               'beta_mag_spread': 0,                  # Spread of beta with Mstar (where beta is the magnetisation)
               'beta_mag_norm': 1e5,                  # Intercept of beta with Mstar (where beta is the magnetisation)
               'beta_mag_mean': 1e6,                  # Mean magnetisation parameter beta

               'rdisc_mean': 10.,     				  # Initial disc scaling radius [au] - No correlation
               'rdisc_method': 'lognormal', 		  # Distribution of initial disc radius - Either correlation or no correlation
               'rdisc_spread': 0.5,     		      # Initial disc radius spread (dex)
               'rd_norm': 10.,                        # Value of Rc for a solar-type star [au]
               'rdisc_slope': -0.5,                   # Slope of the Rc - Mstar correlation (to be determined in rd_zero_corr_in)
               
               'age':  1.,         					  # Population mean age (Myr) (used to simulate YSO's age)
               'sage': 0.0,        					  # Population age dispersion (Myr)
               'initial_stellar_age': 1.e4,  		  # Initial stellar age [yr]
               'pmst': 'Siess00',  					  # PMS Tracks to use
               'tracks_select': 'single',  			  # 'single' or TBD
               'reset_lt': True,   					  # if True: computes L, Teff from tracks
               'star_evolve_method': 'constant',	  # 'pmstracks' or 'constant'
               'mdot': 0.0,        					  # Mass accretion rate initialization
               'sfh': 'constant',  					  # Population Star Formation History (constant, normal, lognormal)

               'flag_dispersion': False,

               'alpha': 1.e-3,     					 # Shakura & Sunayev (1973) alpha parameter
               'alpha_method': 'lognormal', 		 # Distribution of alpha (constant, normal, lognormal)
               'alpha_spread': 0.0,					 # Initial spread in alpha
                          
               'alpha_DW_mean': 1.e-3,     		     # Tabone et al. (2021) alpha disc wind parameter - mean: if correlations are used, it is determined from the magnetisation
               'leverarm': 2,                        # Tabone et al. (2021) lever arm parameter (lambda)
               'omega': 0,                           # Tabone et al. (2021) omega parameter

               'mdot_photoev_norm': 6.25e-9,         # Normalisation of the internal photoevaporation mass loss rate [Msun/yr] (for a solar mass star)
               'mdot_photoev_slope': -0.068,         # Slope of the internal photoevaporation mass loss rate with the stellar mass
               'mdot_photoev_spread': 0.5,           # Spread of the internal photoevaporation mass loss rate [dex]
               'mdot_photoev_mean': 1e-9,            # Mean value of the internal photoevaporation mass loss rate [Msun/yr] (if there are no correlations)
               'mdot_photoev_method': 'lognormal',   # Distribution of the internal photoevaporation mass loss rate
                          
               'L_x_mean': 1e30,                     # Mean value of the X luminosity of the star [erg/s]
               'L_x_spread': 0.1,                    # Spread of the X luminosity of the star [dex]
               'L_x_slope': 1.44,                    # Slope of the X luminosity - stellar mass correlation
               'L_x_norm': 30.37,                    # Normalisation of the X stellar luminosity for 1 Msun [erg/s]
               'L_x_method': 'lognormal',            # Distribution of the X luminosity of the star

               'limit_discmass': 1e-100,             # Minimum disc mass, after which the disc is killed

               'SlopeCs': -0.25,   					 # Slope of the sound speed with radius
               'Hr0': 1. / 30.,    					 # H/R at R = 1 au

               'rin_disc': 0.03,					 # Disc inner radius [au]
               'rout_disc': 10000,					 # Disc outer radius [au]
               'nr_disc': 1000,    					 # Number of radial points in disc
               'rd_spacing': 'natural',				 # Spacing algorithm for radial points

               'analytic': False,    				 # Whether to use the analytic solution to evolve the disc
               'gamma': 1.,							 # Slope of the viscosity with radius

               'dust': False,  						 # Use dust evolution module in DiscEvolution
               'd2g': 0.01,         				 # Dust-to-gas ratio
               'feedback': True,   					 # Feedback of the dust onto the gas

               'star_mdot_evolution': False,  		 # Use mdot to evolve star mass
               'star_no_default': True,  			 # Do not use defaults for Star
               'yso_no_default': True,  			 # Do not use defaults for YSO
               'set_rand_state': False,  			 # Do we want to restore a random generator state
               'initial_rand_state': None,  		 # No default for the random state

               'parallel_evol': False,               # Parallel YSO evolution by default
               'all_available_proc': True,           # use all available processes
               'nprocs': 2,                          # by default use all available CPUs

               'options.MONTECARLO': True,
               'options.CORRELATIONS': True,
               'options.REPRODUCIBILITY': True,
               'options.MHD': True,
               'options.INTERNAL_PHOTOEV': False,

               'seed': 1
                          }