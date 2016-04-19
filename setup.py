# Setup script for the wqio package
#
# Usage: python setup.py install
#
import os
from setuptools import setup, find_packages

DESCRIPTION = ("dockside: A python utility to download United States "
    "Geological Survey (USGS) National Water Information System (NWIS) data")
LONG_DESCRIPTION = DESCRIPTION
NAME = "dockside"
VERSION = "0.0.1"
AUTHOR = "Lucas Nguyen (Geosyntec Consultants)"
AUTHOR_EMAIL = "lnguyen@geosyntec.com"
URL = "https://github.com/Geosyntec/pynwis"
DOWNLOAD_URL = "https://github.com/Geosyntec/pynwis/archive/master.zip"
LICENSE = "BSD 3-clause"
PLATFORMS = "Python 2.7, 3.4 and later."
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.5',
]
INSTALL_REQUIRES = ['pandas']
PACKAGE_DATA = {
}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    package_data=PACKAGE_DATA,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
)
