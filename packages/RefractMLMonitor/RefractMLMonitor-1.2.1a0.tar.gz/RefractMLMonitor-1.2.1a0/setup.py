# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

VERSION = '1.2.1a0'
DESCRIPTION = 'A Python package to monitor the drift in the machine learning models leveraging Snowflake ML Capabilities'

with open("drift/requirements.txt") as f:
    requirements =  f.read().splitlines()


setup(
    name = "RefractMLMonitor",
    version = VERSION,
    packages = find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author_email="mahesh.gadipea@fosfor.com",
    install_requires = requirements,
    include_package_data=True
)
