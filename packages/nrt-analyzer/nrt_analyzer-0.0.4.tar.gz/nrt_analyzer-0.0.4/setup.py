#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
from importlib.metadata import version
__version__ = version(__package__)


def run_setup():
    _folder = os.path.dirname(os.path.realpath(__file__))
    requirement_path = _folder + os.path.sep + 'requirements.txt'
    install_requires = []
    if os.path.isfile(requirement_path):
        with open(requirement_path) as f:
            install_requires = f.read().splitlines()
    setup(name="nrt_analyzer",
          install_requires=install_requires,
          setup_requires=['gitpython'],
          version=__version__,
          packages=find_packages(),
          author="Jaime A. Undurraga",
          author_email="jaime.undurraga@gmail.com",
          description="Tools to pipeline bulk analyses of NRT recordings from Cochlear.",
          long_description="NRT analyzer for ECAP recordings exported from Cochlear Custom Sound",
          license="MIT",
          url="https://gitlab.com/jundurraga/nrt_analyzer",
          package_data={'': ['*.lay', '*.json']},
          include_package_data=True,
          classifiers=[
              'Development Status :: 3 - Alpha',
              'Environment :: Console',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: MIT License',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: Microsoft :: Windows :: Windows 10',
              'Operating System :: POSIX :: Linux',
              'Programming Language :: Python :: 3',
              'Topic :: Scientific/Engineering :: Bio-Informatics'
              ]
          )


if __name__ == '__main__':
    run_setup()
