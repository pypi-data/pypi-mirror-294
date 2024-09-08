#!/usr/bin/env python

import os
from pathlib import Path
from setuptools import find_packages, setup


setup(
    name="expert_doc",
    version="v0.1.1",
    description="Document parser for 'expert'",
    author="Liam Tengelis",
    author_email="liam.tengelis@blacktuskdata.com",
    packages=find_packages(),
    package_data={
        "": ["*.yaml", "requirements.txt"],
        "expert_doc": ["py.typed"],
    },
    install_requires=[
        "pikepdf",
        "pypdfium2",
    ],
)
