#!/usr/bin/env python

from setuptools import setup

setup(
    name='pymicha',
    version='0.0.1',
    description='Misc. code that Micha thinks is useful',
    author='Micha Gorelick',
    author_email='mynameisfiber@gmail.com',
    url='http://github.com/mynameisfiber/pymicha/',
    download_url='https://github.com/mynameisfiber/pymicha/tarball/master',
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",

    packages=['pymicha'],

    install_requires=[
        "numpy",
    ],
    extras_require={
        "keras": ["keras", ],
        "plot": ["seaborn", "matplotlib"],
        "prob_ds": ["pybloom-live"],
    }
)
