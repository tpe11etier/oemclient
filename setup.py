#!/usr/bin/env python
# coding=utf-8

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import multiprocessing
except:
    pass

APP_NAME = 'oemclient'
VERSION = '0.1.1'

# Grab requirments.
with open('requirements.txt') as f:
    required = f.readlines()

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

# Build Helper.
if sys.argv[-1] == 'build':
    try:
        import py2exe
    except ImportError:
        print('py2exe is required to continue.')
        sys.exit(1)

    sys.argv.append('py2exe')

    settings.update(
        zipfile = None,
        options = {
            'py2exe': {
                'compressed': 1,
                'optimize': 0,
                'bundle_files': 1}})

settings.update(
    name=APP_NAME,
    version=VERSION,
    author='Tony Pelletier',
    author_email='tony.pelletier@gmail.com',
    scripts=['oemclient.py'],
    url='https://github.com/tpe11etier/oemclient',
    license='MIT',
    description='oemclient is a client for the Varolii Xpress API',
    long_description=open('README.md').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'oemclient = oemclient:main',
        ],
    }
)

setup(**settings)
