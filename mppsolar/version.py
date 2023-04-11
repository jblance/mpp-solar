#import configparser

#version = configparser.ConfigParser()
#version.read("pyproject.toml")
#__version__ = version["tool.poetry"]["version"].replace('"', "")

__version__ = "0.15.42"
