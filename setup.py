#! /usr/bin/python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description' : "Subversion simple client",
    'author' : "Rodrigo Santellan",
    'url' : "https://github.com/rsantellan/python-subversion-simple-client",
    'download_url' : 'https://github.com/rsantellan/python-subversion-simple-client',
    'author_email' : 'rsantellan@gmail.com',
    'version' : '0.0.1',
    'install_requieres' : ['nose'],
    'packages' : ['subversion-simple-client'],
    'scripts' : [],
    'name' : 'Subversion simple client'
}

setup(**config)
