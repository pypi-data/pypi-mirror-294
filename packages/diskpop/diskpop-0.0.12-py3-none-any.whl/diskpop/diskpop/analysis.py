#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.integrate
from .defaults import default_pars

from diskpop import Population


class EvolvedPopulation(object):
    """
    Container for an evolved population.

    TODO: cache the created tables. Currently the table is re-computed every time.

    """
    def __init__(self, filename):						# Looking for filename - prints an error if not available.
        assert os.path.isfile(filename) is True, \
            "Population filename {} does not exist".format(filename)

        self.snapshots = []
        self.parameters = dict()
        self.read_pops(filename)

    def _add_snapshot(self, population):
        """
        Adds a snapshot of the population to the container.
        # TODO: when time will be stored inside Population, take it from there
        """
        assert isinstance(population, Population)
        self.snapshots.append(population)

    def read_pops(self, filename):
        """
        Read populations from the file.
        Note: each time snapshot is read as a separate population.

        :param filename: string
        :return:

        """
        _ = Population(parameters_user = {'nysos': 1, 'init': False}, default_pars = default_pars)			# Defines _ as a population containing one YSO
        _.io_pop_hdf5(filename, 'read', 0, 0)				# Reads from filename for yso 0 at time 0
        self.parameters = _.parameters						# Sets parameters to _'s parameters - i.e. all default except for nysos and init which were manually set

        for i, time_snapshot in enumerate(self.parameters['times_snapshot']):
            mp = Population(parameters_user = {'nysos': 1, 'init': False}, default_pars = default_pars)		# mp is for My Population - defines a population of 1 YSO
            mp.io_pop_hdf5(filename, 'read', 0, i)				# Reads from filename for yso 0 at time i
            self._add_snapshot(mp)								# Adds a snapshot to mp
            print("Reading time[{}]={}".format(i, time_snapshot))



    def create_table(self, snapshot):
        """
        Create a table collecting the population properties at a given snapshot.

        Parameters
        ----------
        i_time_snapshot : Population
            Population object containing the population at a given snapshot.

        Returns
        -------
        df : pandas.Dataframe
            Object containing the properties of the Population object in table format.

        Notes
        -----
        At this stage, to keep it simple, `disc_sigma` and `disc_grid_rc`
        are not imported as they are arrays and not scalars, like the other quantities.
        Anyway, the structure is ready: if you uncomment the lines regarding
        `disc_sigma` and `disc_grid_rc`, they get imported.

        """
        assert isinstance(snapshot, Population)

        nysos = snapshot.parameters['nysos']
        assert nysos == len(snapshot.ysos)

        # not used for now, for future reference
        # born_mask = np.array([snapshot.ysos[i].born for i in range(nysos)]).astype('bool')

        # import YSOs properties
        star_age = np.zeros(nysos)
        star_llum = np.zeros(nysos)
        star_teff = np.zeros(nysos)
        star_mass = np.zeros(nysos)
        star_mdot = np.zeros(nysos)
        disc_mass = np.zeros(nysos)
        disc_radius = np.zeros(nysos)
        disc_dust_radius = np.zeros(nysos)
        # disc_sigma = []
        # disc_grid_rc =[]

        for i_yso, yso in enumerate(snapshot.ysos):
            if yso.born:
                star_age[i_yso] = yso.star.age
                star_llum[i_yso] = yso.star.llum
                star_teff[i_yso] = yso.star.teff
                star_mass[i_yso] = yso.star.mass
                star_mdot[i_yso] = yso.star.mdot
                # disc_sigma.append(yso.disc.Sigma)
                # disc_grid_rc.append(yso.disc.grid.Rc)
            else:
                pass
                # disc_sigma.append(0)
                # disc_grid_rc.append(0)

        # compute derived quantities
        for i_yso, yso in enumerate(snapshot.ysos):
            if yso.born:
                disc_mass[i_yso] = self.compute_disc_mass(yso.disc.grid.Rc,		
                                                          yso.disc.Sigma)				# Computes disc mass by integration of surface 												density (trapezoid rule).
                disc_radius[i_yso] = self.compute_disc_size(yso.disc.grid.Rc,           # Computes disc size = GAS radius
                                                          yso.disc.Sigma)
                try:
                    disc_dust_radius[i_yso] = self.compute_disc_size(yso.disc.grid.Rc,  # Computes disc size = DUST radius (if there's dust)
                                                          yso.disc.Sigma_D[0,:]+yso.disc.Sigma_D[1,:])
                except AttributeError:
                    pass

        # create data frame
        df = pd.DataFrame({'star_age': star_age,
                     'star_llum': star_llum,
                     'star_teff': star_teff,
                     'star_mass': star_mass,
                     'star_mdot': star_mdot,
                     # 'disc_sigma': disc_sigma,
                     # 'disc_grid_rc': disc_grid_rc,
                     'disc_mass': disc_mass,
                     'dust_radius': disc_dust_radius,
                     'disc_radius': disc_radius})
                     

        return df


    def table(self, i_time_snapshot):
        """
        Return the table corresponding to the snapshot index `i_time_snapshot`.
        According to the actual architecture, the corresponding time is:

            self.parameters['time_snapshots'][i_time_snapshot]

        TODO: by developing this helper function will allows us to cache the tables
        for different time steps, so that `create_table` is called only once.
        At the moment it simply redirects the call to `create_table`.

        Parameters
        ----------
        i_time_snapshot : int
            Index of the time snapshot that should be used to produce the table.

        Returns
        -------
        df : pandas.Dataframe
            See `create_table`.

        """
        return self.create_table(self.snapshots[i_time_snapshot])

    @staticmethod
    def compute_disc_mass(radii, sigma):
        """
        Compute the disc mass.
        TODO: is there another function e.g. in the disc class that we can use instead?
        TODO: check units!

        :param radii: array_like, float
            Radial grid [au]
        :param sigma: array_like, float
            Surface density [g/cm^2]
        :return: mass: float
            Total mass computed with trapezoidal rule, which accounts for the numerical scheme used.

	A: this integration messes up with the units, and the computed mass needs converting - which is actually done in driver
	with solarToCodeMass. Wouldn't it be better to convert here...?

        """
        mass_tmp = np.trapz(radii*sigma,radii)

        return 2. * np.pi * mass_tmp
    
    @staticmethod
    def compute_disc_size(radii,sigma):
        mass_tmp = scipy.integrate.cumtrapz(radii*sigma,radii)
        mass_tmp /= mass_tmp[-1]
        return radii[np.searchsorted(mass_tmp,0.5)]

    def plot(self, ax, xaxis, yaxis, cm_name='Spectral', highlight_first_last=False):
        """
        Plots quantities of the evolved population.
        Currently, it plots all the time steps.

        Parameters
        ----------
        ax : matplotlib.Axes
            Artist object where to perform the plot.
        xaxis : str
            Name of the dataframe column to use a x axis.
        yaxis : str
            Name of the dataframe column to use as y axis.
        cm_name : str, optional
            Colormap name to color-code different time step.
            default: Spectral is similar to RdYlBu but additionally has the green.

        TODO: implement colorbar. Have a look at the listed colormap at
              https://matplotlib.org/examples/api/colorbar_only.html

        """
        cm = plt.cm.get_cmap(cm_name)

        ntimes_snapshots = len(self.parameters['times_snapshot'])
        for itime in range(ntimes_snapshots):

            df = self.table(itime)
            nobjects = len(df)
            assert nobjects == self.parameters['nysos']

            df_columns = df.columns.values.tolist()
            assert xaxis in df_columns,\
                "xaxis '{}' does not exist in the dataframe. Available columns: {}".format(xaxis, df_columns)
            assert yaxis in df_columns, \
                "yaxis '{}' does not exist in the dataframe. Available columns: {}".format(yaxis, df_columns)

            for i in range(nobjects):
                ax.scatter(df.iloc[i][xaxis], df.iloc[i][yaxis], s=35, vmin=0,
                            vmax=1., c=itime/float(ntimes_snapshots), cmap=cm, lw=0.2)

            if highlight_first_last:
                if itime == 0:
                    for i in range(nobjects):
                        ax.plot(df.iloc[i][xaxis], df.iloc[i][yaxis], '+', ms=10, color='cyan', markeredgewidth=1.5)
                if itime == ntimes_snapshots-1:
                    for i in range(nobjects):
                        ax.plot(df.iloc[i][xaxis], df.iloc[i][yaxis], '+', color='blue', markeredgewidth=1.5)
