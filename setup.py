from importlib_metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
    name = 'MPK API',
    version= '1.0.0',
    description= 'API for MPK LODZ',
    author= 'Rostyslav Mosorov',
    author_email= 'rmosorov@icloud.com',
    license= 'MIT License',
    url = 'https://github.com/rostekus/MPK-API',
    packages = find_packages(where='src',exclude='tests*'),
    package_dir={'': 'src'}

)