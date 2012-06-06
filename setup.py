#!/usr/bin/env python
# Copyright (C) 2012 by Brian Neal.
# This file is part of Py-Enigma, the Enigma Machine simulation.
# Py-Enigma is released under the MIT License (see License.txt).

from distutils.core import setup
from os.path import join, dirname

import enigma

setup(
    name='py-enigma',
    version=enigma.__version__,
    author='Brian Neal',
    author_email='bgneal@gmail.com',
    url='https://bitbucket.org/bgneal/enigma/',
    license='MIT',
    description='A historically accurate Enigma machine simulation library.',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    packages=['enigma', 'enigma.rotors', 'enigma.tests'],
    package_data=dict(enigma=['examples/*.py',
                              'docs/source/*.rst',
                              'docs/source/*.py',
                             ]),
    scripts=['pyenigma.py'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
