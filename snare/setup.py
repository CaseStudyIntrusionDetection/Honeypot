#!/usr/bin/env python
from setuptools import find_packages
from distutils.core import setup

setup(name='Snare',
      version='0.3.0',
      description='Super Next generation Advanced Reactive honEypot',
      author='CaseStudyIntrusionDetection',
      url='https://github.com/CaseStudyIntrusionDetection/Honeypot',
      packages=find_packages(exclude=['*.pyc']),
      scripts=['./bin/snare', './bin/clone'],
)
