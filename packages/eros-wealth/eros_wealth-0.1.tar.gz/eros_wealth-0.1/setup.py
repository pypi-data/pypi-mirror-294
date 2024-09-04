# setup.py
from setuptools import setup, find_packages
import os

# Περιλαμβάνει τα αρχεία που δημιουργήθηκαν από Cython ή PyArmor
packages = find_packages()

setup(
    name='eros_wealth',
    version='0.1',
    packages=packages,
    include_package_data=True,
    ext_modules=[],  # τα modules θα περιλαμβάνονται ως προ-compiled αρχεία
    install_requires=[
        # Προσθήκη άλλων εξαρτήσεων αν χρειάζονται
    ],
)
