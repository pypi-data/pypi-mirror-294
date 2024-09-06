"""scene_forge - Python package to generate scenes using radiative transfer modelling. This package wraps external radiative transfer codes, and uses these to make simulated scenes for Earth Observation measurements."""

__author__ = "Pieter De Vis <pieter.de.vis@npl.co.uk>"
__all__ = []

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
