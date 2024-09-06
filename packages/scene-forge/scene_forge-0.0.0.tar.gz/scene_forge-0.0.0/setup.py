import io
import os
import re

from setuptools import find_packages
from setuptools import setup
import versioneer

exec(open("scene_forge/_version.py").read())

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type("")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())

setup(
    version=__version__,
    name="scene_forge",
    url="https://gitlab.npl.co.uk/eco/tools/scene_forge",
    license="None",
    author="Pieter De Vis",
    author_email="pieter.de.vis@npl.co.uk",
    description="Python package to generate scenes using radiative transfer modelling. This package wraps external radiative transfer codes, and uses these to make simulated scenes for Earth Observation measurements.",
    long_description=read("README.md"),
    packages=find_packages(exclude=("tests",)),
    install_requires=[],
    extras_require={
        "dev": [
            "pre-commit",
            "tox",
            "sphinx",
            "sphinx_book_theme",
            "sphinx_design",
            "ipython",
        ]
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
