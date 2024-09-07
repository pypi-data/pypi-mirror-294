#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TwoLayerSurfDens(object):
    def __init__(self, disc):
        # TODO: check how it is called the surfdens stored in disc.
        self.surfdens = disc.surfdens

        # this is a hack for TwoLayer, must be 0
        self.npar = 0

    def __call__(self, *args, **kwargs):
        return self.surfdens


class SEDGenerator(object):

    def __init__(self, model_type, star, disc):
        """
        Note: here I assumed star and disc are "streamlined" versions containing:
            star: lum, temp, mass, dist (see units below)
            disc: gridrad, surfdens
        self.model_type = model_type


        """
        self.model_type = model_type

        if self.model_type == '2layer':
            # star is required to init TwoLayer, but actually
            # it is not needed in terms of calculations
            # at some point I will change this in py2layer
            # so that we can avoid passing star in the init.
            from .py2layer.py2layer import TwoLayer

            self.default_2layer_pars = {
                'nrad': 600,
                'rmin': 0.1,  # au
                'rmax': 600.,  # au
                'nsize': 200,
                'amin': 5.e-7 , # [cm]
                'amax': 10.,  # [cm]
                'a0min': {'mid': 1.e-6,  # cm
                          'sur': 1.e-6},
                'a0max': {'sur': 1.e-4},  # cm
                'q': {'mid': 3.0, 'sur': 3.5},
                'bmax': {'sur': 0.},
                'ncomp': 4,
                'opt_const_filenames': {"Si": 'in_silicate.dat',
                                         "Ca": 'in_aC_ACH2_Zubko.dat',
                                         "WaterIce": 'in_H2Oice_Warren.dat'},
                'fractions': {"Si": 5.4e-2,
                              "Ca": 20.6e-2,
                              "WaterIce": 43.999e-2},
                'nwle': 200,  # if > 400 the model crashes
                'wlemin': 1.e-5 , # [cm]
                'wlemax': 1.,  # [cm]

                'wle_out_mm': [0.89],  # mm
                'sigma_prescription': 'g',
            }

            # use same radial grid as in disc
            self.default_2layer_pars.update(nrad=disc.nr)
            self.default_2layer_pars.update(rmin=disc.rin)
            self.default_2layer_pars.update(rmax=disc.rout)

            self.disc_model = TwoLayer(star, self.default_2layer_pars)
            self.disc_model.compute_grids()

    def compute(self, star, disc):
        """
        Computes the SED.

        Here I require the star and disc objects to be passed again after init,
        the reasons being:
          1) TowLayer.compute_grids() takes time as it computes the
        optical efficiencies for a given dust composition.
          2) we might want to recompute the SED for different stars and disc surfa densities
        but same dust composition

        Return
        ------
        dict: containing the SED ('spectrum'), and the corresponding grid of frequencies ('gridfra')
        and wavelengths ('gridwle') on which it is computed.

        """
        if self.model_type == '2layer':
            # hack to change the star properties at any time,
            # required since in Twolayer the star is set at the init()
            # Warning: careful with the units
            self.disc_model.lstar = star.lum  # erg/s
            self.disc_model.tstar = star.temp  # K
            self.disc_model.mstar = star.mass  # g
            self.disc_model.dist = star.dist

            # hack to change the surface density generator
            self.disc_model.surface_density = TwoLayerSurfDens(disc)

            # TODO: feed the correct a0max, bmax and inc computed from DiscEvolution
            a0max = 1.0
            bmax = 0.
            results = self.disc_model.compute(a0max, bmax, inc=0., return_opacity=False)
            # Warning: return_opacity=True makes results much bigger.

            return {x: results[x] for x in ['gridfra', 'gridwle', 'spectrum']}




# typical usage:

# somewhere else, e.g. in an analysis script:
from .streamlinedstar import StreamlinedStar

# s_star = StreamlinedStar(star)
# s_disc = StreamlinedDisc(disc)

s_star = None
s_disc = None

sed = SEDGenerator('2layer', s_star, s_disc)
sed.compute(s_star, s_disc)
