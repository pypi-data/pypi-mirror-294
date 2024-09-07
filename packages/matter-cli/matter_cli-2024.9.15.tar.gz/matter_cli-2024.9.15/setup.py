#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    packages=find_packages(
        exclude=('plugin', 'drivers', 'matter_build', 'matter_android', 'matter_command', 'scripts', 'tests', 'docs', 'matter_tools')
    ),
)