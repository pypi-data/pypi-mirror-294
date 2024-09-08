#!/usr/bin/env python

import os
from pathlib import Path
from setuptools import find_packages, setup


setup(
    name="expert_kb",
    version="v0.1.1",
    description="Knowledge base interface for 'expert'",
    author="Liam Tengelis",
    author_email="liam.tengelis@blacktuskdata.com",
    packages=find_packages(),
    package_data={
        "": ["*.yaml", "requirements.txt", "*.sql"],
        "expert_kb": ["py.typed"],
    },
    install_requires=[
        "sqlite-vec",
    ],
)
