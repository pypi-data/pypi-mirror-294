A Python code for population synthesis of protoplanetary discs
----------------------------------------------------------------


Diskpop is a Python code used to generate and evolve synthetic populations of protoplanetary discs. It includes the viscous, hybrid and MHD-wind driven accretion prescriptions, internal and external photoevaporation, as well as dust evolution.

To analyse the raw output of Diskpop, the Python library popcorn is available. Both codes have been published in Somigliana et al. 2024 (ADD LINK).


Using Diskpop for your work
----------------------------

Diskpop and popcorn are freely available for the community to use. If you use Diskpop simulations in your work, please make sure to cite Somigliana et al. (2024) ADD LINK. Additionally, as the dust evolution module is forked from Richard Booth's repository, if you use include dust in your simulations please cite also `Booth et al. (2017) <https://ui.adsabs.harvard.edu/abs/2017MNRAS.469.3994B/abstract>`_.


Installation
-------------

Diskpop can be installed from terminal as

.. code::

	pip install diskpop

Alternatively, it is also possible to clone the Bitbucket repository. The same applies to the output analysis library, popcorn:

.. code::

	pip install popcorn_diskpop


Diskpop Team
-------------

Diskpop and popcorn have been developed by Alice Somigliana, Giovanni Rosotti, Marco Tazzari, Leonardo Testi, Giuseppe Lodato, 
Claudia Toci, Rossella Anania, and Benoit Tabone. Both codes are under active development.


Diskpop papers
---------------

At `this link <https://ui.adsabs.harvard.edu/user/libraries/OgnSMEn2QJ-bQamef0f7TA>`_ you can find an up-to-date list of papers employing Diskpop (including its pre-release versions).

Documentation
--------------

The Diskpop documentation is available `here <https://alicesomigliana.github.io/diskpop-docs/index.html>`_


Acknowledgements
------------------

This project was partly supported by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) - Ref no. 325594231 FOR 2634/2 TE 1024/2-1, by the DFG Cluster of Excellence Origins (www.origins-cluster.de). This projec has received funding from the European Research Council (ERC) via the ERC Synergy Grant ECOGAL (grant 855130).