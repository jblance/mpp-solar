#!/bin/bash
#
# grab pyproject.toml version and update version.py (with -dev suffix)
# (for use with makefile that bumps the poetry version)
#
awk '/^version/ {print "__version__ = " substr($3, 1, length($3)-1) "-dev\""}' pyproject.toml > mppsolar/version.py