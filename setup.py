#!/usr/bin/env python

from distutils.core import setup

setup(name='oemclient',
	version='0.1',
	description='Oemclient',
	author='Tony Pelletier',
	author_email='tony.pelletier@gmail.com',
	packages = ['oemclient'],
	package_data = {'package' : 'files'},
	py_modules = ['oemclient'],
)
