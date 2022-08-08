from setuptools import setup, find_packages
import pkg_resources
import pathlib

import scptool

with pathlib.Path("requirements.txt").open() as requirements_txt:
    requires = [ str(r) for r in pkg_resources.parse_requirements(requirements_txt) ]

setup(
    name = 'scptool',
    version = scptool.__version__,
    packages = find_packages(),
    entry_points = {
        'console_scripts': [ 'scptool=scptool.main:main']
    },
    install_requires = requires
)