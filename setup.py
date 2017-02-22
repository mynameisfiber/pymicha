#!/usr/bin/env python

from setuptools import setup

extras_require = {
    "keras": ["keras", "theano"],
    "plot": ["seaborn", "matplotlib", "numpy"],
    "prob_ds": ["pybloom-live"],
    "extra": ["tqdm", "sklearn", "nltk"]
}
extras_require['full'] = [r for rs in extras_require.values() for r in rs]

setup(
    name='pymicha',
    version='0.0.2',
    description='Misc. code that Micha thinks is useful',
    author='Micha Gorelick',
    author_email='mynameisfiber@gmail.com',
    url='http://github.com/mynameisfiber/pymicha/',
    download_url='https://github.com/mynameisfiber/pymicha/tarball/master',
    license="GNU Lesser General Public License v3 or later (LGPLv3+)",

    packages=['pymicha'],
    extras_require=extras_require,
)
