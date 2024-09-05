#!/usr/bin/env python

import os
from pathlib import Path
from setuptools import find_packages, setup


def load_requirements():
    with open(Path(lib_folder) / "requirements.txt") as f:
        return f.read().split()
    pass


setup(
    name="expert_kb",
    version="v0.1.0",
    description="Knowledge base interface for 'expert'",
    author="Liam Tengelis",
    author_email="liam.tengelis@blacktuskdata.com",
    packages=find_packages(),
    package_data={
        "": ["*.yaml", "requirements.txt"],
        "expert_kb": ["py.typed"],
    },
    install_requires=[
        "sqlite-vec",
    ],
)
