#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='suppliers',
    version='1.0',
    description='Shows suppliers.',
    author='Luke Shiner',
    author_email='luke@lukeshiner.com',
    install_requires=['django'],
    packages=find_packages(),
    include_package_data=True,
    )
