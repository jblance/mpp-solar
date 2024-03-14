#!/bin/bash
#
# grab pyproject.toml version and update version.py
# (for use with makefile that bumps the poetry version)
#
awk '/^version/ {print "__version__ = " $3}' pyproject.toml > mppsolar/version.py