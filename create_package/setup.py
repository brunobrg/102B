"""
teste
~~~~~

To create a Kivy *.kex extension file for this extension, run this file like
so::

    python setup.py create_package

That will turn your current Kivy extension development folder into a *.kex Kivy
extension file that you can just drop in one of the extensions/ directories
supported by Kivy.
"""
from distutils.core import setup
from distutils.cmd import Command

import teste
long_desc = teste.__doc__


import os
from os.path import join
from shutil import copy
from subprocess import call
import sys


class PackageBuild(Command):
    description = 'Create Extension Package'
    user_options = []

    def run(self):
        # Call this file and make a distributable .zip file that has our desired
        # folder structure
        call([sys.executable, 'setup.py', 'install', '--root', 'output/',
            '--install-lib', '/', '--install-platlib', '/', '--install-data',
            '/teste/data', 'bdist', '--formats=zip'])
        files = os.listdir('dist')
        if not os.path.isdir('kexfiles'):
            os.mkdir('kexfiles')
        for file in files:
            # Simply copy & replace...
            copy(join('dist', file), join('kexfiles', file[:-3] + "kex"))
        print('The extension files are now available in kexfiles/')

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


cmdclass = {'create_package': PackageBuild}


setup(
    name='teste',
    version='0.1',
    url='<enter URL here>',
    license='<specify license here>',
    author='gagos',
    author_email='brunobraganca@aluno.unb.br',
    description='<enter short description here>',
    long_description=long_desc,
    packages=['teste'],
    cmdclass=cmdclass,
    classifiers=[
        # Add your own classifiers here
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
