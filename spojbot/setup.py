#!/usr/bin/env python

from setuptools import setup

setup(
    name='spojbot',
    version='0.1a',
    description='Spoj Solution Submitter',
    long_description='An Experiment on submitting solutions to spoj through a bot',
    author='Srinivas Devaki',
    author_email='mr.eightnoteight@gmail.com',
    url='https://github.com/eightnoteight/spojbot',
    install_requires=[
        "requests>=2.3.0",
        "beautifulsoup4>=4.3.2"
    ],
    packages=[
        'spojbot'
    ],
    license='apache'
)
