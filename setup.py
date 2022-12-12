from setuptools import setup, find_packages
import pkg_resources
import pathlib

import scpkit

with pathlib.Path("requirements.txt").open() as requirements_txt:
    requires = [ str(r) for r in pkg_resources.parse_requirements(requirements_txt) ]

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name = 'scpkit',
    version = scpkit.__version__,
    author="Aquia",
    author_email="info@aquia.us",
    url="https://github.com/aquia-inc/scpkit",
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = find_packages(exclude=['tests*']),
    entry_points = {
        'console_scripts': [ 'scpkit=scpkit.main:main']
    },
    install_requires = requires
)