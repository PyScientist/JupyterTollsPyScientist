from setuptools import find_packages
from distutils.core import setup
import os


if __name__ == '__main__':
    setup(
        name='JupyterToolsPyScientist',
        version=os.getenv('PACKAGE_VERSION', '0.0.0.dev0'),
        author='Sergei Dmitriev',
        author_email='sergei-dmitriev@mail.ru',
        description='Tools for simplifying work with ML in jupyter',
        package_dir={'': 'src'},
        packages=find_packages('src', include=['JupyterTollsPyScientist',]),
    )

