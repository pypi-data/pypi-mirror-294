#! /usr/bin/env python
# -*- coding: utf-8 -*-
# from numpy.distutils.core import setup, Extension
from setuptools import setup, find_packages

# set the version number
with open('diskpop/_version.py') as f:
    exec(f.read())

setup(
    name = "diskpop",
    version = '0.0.7',
    description = "A Python code to perform protoplanetary disc population synthesis",
    author = "Alice Somigliana, Giovanni Rosotti, Marco Tazzari, Leonardo Testi, Giuseppe Lodato, Claudia Toci, Rossella Anania, Benoit Tabone",
    author_email = "alice.somigliana@eso.org",
    packages = find_packages(),
    #packages=['diskpop', 'pmstracks', 'DiscEvolution'],
    url = "https://bitbucket.org/ltesti/diskpop/",
    license = "GPL",
    long_description = open("README.md").read() + "\n\n"
                    + "Changelog\n"
                    + "---------\n\n"
                    + open("HISTORY.rst").read(),
    package_data = {"": ["LICENSE", "AUTHORS.rst"]},
    include_package_data = True,
    install_requires = ["matplotlib", "numpy", "scipy", "pandas"],
    classifiers = [
        "Development Status :: 0 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
    # ext_modules = ["DiscEvolution"]
)
