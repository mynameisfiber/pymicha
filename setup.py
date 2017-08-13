#!/usr/bin/env python

from setuptools import setup, find_packages
from pymicha import __version__


extras_require = {
    "keras": ["keras", "theano"],
    "plot": ["seaborn", "matplotlib", "numpy"],
    "prob_ds": ["pybloom-live"],
    "ds": ["sharedmem"],
    "extra": ["tqdm", "sklearn", "nltk"]
}

extras_require['full_noex'] = list({r
                                    for k, rs in extras_require.items()
                                    if k != 'extra'
                                    for r in rs})
extras_require['full'] = list({r
                               for rs in extras_require.values()
                               for r in rs})

setup(
    name='pymicha',
    version=__version__,
    description='Misc. code that Micha thinks is useful',
    author='Micha Gorelick',
    author_email='mynameisfiber@gmail.com',
    url='http://github.com/mynameisfiber/pymicha/',
    download_url='https://github.com/mynameisfiber/pymicha/tarball/master',
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",

    packages=find_packages(),
    extras_require=extras_require,
)
