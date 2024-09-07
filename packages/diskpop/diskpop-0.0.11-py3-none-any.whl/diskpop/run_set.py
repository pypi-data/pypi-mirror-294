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


"""  
.. _target to runset:

"""


# Do not touch: code libraries 

import numpy as np; np.seterr(invalid = 'raise', divide = 'raise')
import sys, os, json
from datetime import datetime
import argparse
from diskpop import Population

from diskpop.defaults import default_pars

options = type('test', (object,), {})()

# Setup parameters: 

# Name of the input parameters file: if an argument is passed to the command line, that is the name of the parameters file. If no argument is passed, the default filename is parameters.json

parser = argparse.ArgumentParser(description = 'This is the entry point for running diskpop')
parser.add_argument("inputfile", help = 'Name of the input parameters file (must be a .json file)', default = 'parameters.json')
args = parser.parse_args()

with open(args.inputfile) as f:
    parameters = json.load(f)

parameters_options = parameters['parameters_options']
 
options.MONTECARLO, options.CORRELATION, options.REPRODUCIBILITY, options.MHD, options.INTERNAL_PHOTOEV, options.DO_PLOTS = [parameters_options[k] for k in ['options.MONTECARLO', 'options.CORRELATION', 'options.REPRODUCIBILITY', 'options.MHD', 'options.INTERNAL_PHOTOEV', 'options.DO_PLOTS']]
parameters_multiprocessing = parameters['parameters_options']['multiprocessing_options']

parameters_general = parameters['parameters_population'][0]['parameters_general']
parameters_mhd = parameters['parameters_population'][0]['parameters_mhd']
parameters_imf = parameters['parameters_population'][0]['parameters_imf']
parameters_correlation = parameters['parameters_population'][0]['parameters_correlation']
parameters_nocorrelation = parameters['parameters_population'][0]['parameters_nocorrelation']
parameters_spreads = parameters['parameters_population'][0]['parameters_spreads']
parameters_singledisc = parameters['parameters_singledisc']


### CHECKS

if (options.INTERNAL_PHOTOEV and parameters_correlation['mdot_photoev_norm'] != 0 and parameters_correlation['L_x_norm'] != 0) or (options.INTERNAL_PHOTOEV and parameters_nocorrelation['mdot_photoev_mean'] != 0 and parameters_nocorrelation['L_x_mean'] != 0):
    print("Please provide only one of the internal photoevaporation parameters - either mdot_photoev or L_x")
    sys.exit()

if options.INTERNAL_PHOTOEV and parameters_general['analytic'] == True:
    print("Please set 'analytic' to 'false' in order to run a simulation with photoevaporation")
    sys.exit()


if (not options.INTERNAL_PHOTOEV and options.CORRELATION):
    parameters_correlation['mdot_photoev_norm'] = 0
    parameters_correlation['L_x_norm'] = 0
    
if (not options.INTERNAL_PHOTOEV and not options.CORRELATION):
    parameters_nocorrelation['mdot_photoev_mean'] = 0
    parameters_nocorrelation['L_x_mean'] = 0

if (parameters_general['alpha'] != 0 and options.MHD and parameters_mhd['omega'] != 0):
    print("The case where both alpha_SS (Shakura and Sunyaev 1973) and omega (Tabone et al. 2021) are not zero is not implemented yet!")
    sys.exit()

if (not options.MHD and parameters_mhd['omega'] != 0):
    print("Omega (Tabone et al. 2021) is set to be non-zero with alpha disc wind equal to zero (purely viscous case)!")
    sys.exit()

if (not options.MHD and parameters_general['alpha'] == 0):
    print("There is no viscosity and no MHD winds - the discs will never evolve!")
    sys.exit()

if (options.INTERNAL_PHOTOEV and options.CORRELATION and parameters_correlation['L_x_norm'] == 0 and parameters_correlation['mdot_photoev_norm'] == 0) or (options.INTERNAL_PHOTOEV and not options.CORRELATION and parameters_nocorrelation['L_x_mean'] == 0 and parameters_nocorrelation['mdot_photoev_mean'] == 0):
    print("Photoevaporation is on but neither the mass loss rate nor the X luminosity are initialised!")
    sys.exit()

if parameters_general['dust'] == True:
    output_prefix = 'dust'                  
else:
    output_prefix = 'no_dust'

### SETTING THE SIMULATIONS' PARAMETERS

pars = default_pars.copy()
pars.update(parameters_general)
pars.update(parameters_options)
pars.update(parameters_mhd)
pars['times_snapshot'] = np.array(parameters_general['times_snapshot'])
pars['corr'] = parameters_options['options.CORRELATION']

# Parameters specific to Monte Carlo simulations

if options.MONTECARLO:

    pars.update(parameters_imf)
    pars.update(parameters_correlation)
    pars.update(parameters_nocorrelation)
    pars.update(parameters_spreads)
    pars.update(parameters_multiprocessing)
    
# Parameters specific to single discs

if not options.MONTECARLO:

    pars.update(parameters_singledisc)
    if len(pars['mstar']) != pars['nysos']:
        print('WARNING: the number of YSOs and of stellar masses are different. I will proceed with a number of YSOs equal to the number of provided stellar masses.')

# Output file name

if pars['output_name'] == 'default':

    date_time = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")

    if options.MONTECARLO:
        pars['output_name'] = output_prefix + '_Montecarlo_corr=' + str(pars['corr']) + '_' + date_time + '.hdf5'
    else:
        pars['output_name'] = output_prefix+'_' + str(pars['alpha']) + '_'+str(pars['mdisc_mean']) + '_' + str(pars['rdisc_mean']) + '_single_disc' + '_' + date_time + '.hdf5'
else:
    pars['output_name'] = parameters_general['output_name'] + '.hdf5'

# Screen infos

"""
Prints information of the simulation on screen - in particular, the number of discs in the population and the number of timesteps.

"""

if __name__ == '__main__':

    # Checking if the filename already exists - If so, raise an error and stop running to prevent overwriting.

    if os.path.isfile(pars['output_name']):
        raise NameError("Filename already exists - please pick a new name to avoid overwriting your simulations.")
        
    print ('Will now run ', pars['output_name'])

    if options.MONTECARLO:
        print("You will evolve {} discs for {} timesteps.".format(pars['nysos'], len(pars['times_snapshot'])))

    # Do not touch: code libraries 

    pars['times_snapshot'] *= 2*np.pi
    pars['times_snapshot'] = (pars['times_snapshot']).tolist()

    if options.REPRODUCIBILITY:
        if parameters_general['seed'] == None:
            print('Reproducibility is on but seed is set to None - please choose an appropriate seed')
            sys.exit()
        else:
            np.random.seed(parameters_general['seed'])


    mypop = Population(pars, default_pars = default_pars, outfile_name = pars['output_name'])
    mypop.generate_snapshot()

    sys.exit()
