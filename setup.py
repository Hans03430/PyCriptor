import os

from setuptools import find_packages, setup
from typing import List


setup(
    name='pycryptor',
    author='Hans Matos',
    author_email='hans.matos@pucp.edu.pe',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'ciphers @ git+ssh://git@github.com/Hans03430/Ciphers@main'
    ],
    package_data={'': ['*.glade', '*.png']},
    #entry_points={
    #"console_scripts": [
    #    "mathmagic=mathmagic.command_line:main"]
    #}
)
