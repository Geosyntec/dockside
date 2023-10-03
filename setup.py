# Setup script for the wqio package
#
# Usage: python setup.py install
#
import os
import re
from setuptools import setup, find_packages


def search(substr: str, content: str):
    found = re.search(substr, content)
    return found.group(1) if found else ""


with open("dockside/__init__.py", encoding="utf8") as f:
    content = f.read()
    version = search(r'__version__ = "(.*?)"', content)
    author = search(r'__author__ = "(.*?)"', content)

DESCRIPTION = (
    "dockside: A python utility to download United States "
    "Geological Survey (USGS) National Water Information System (NWIS) data"
)
LONG_DESCRIPTION = DESCRIPTION
NAME = "dockside"
VERSION = version
AUTHOR = author
URL = "https://github.com/Geosyntec/dockside"
DOWNLOAD_URL = "https://github.com/Geosyntec/dockside/archive/master.zip"
LICENSE = "BSD 3-clause"
PLATFORMS = "Python 3.8 and later."
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
INSTALL_REQUIRES = ["pandas", "requests"]
PACKAGE_DATA = {}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
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
