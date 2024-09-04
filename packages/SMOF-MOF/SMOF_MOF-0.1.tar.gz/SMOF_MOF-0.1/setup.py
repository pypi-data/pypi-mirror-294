from setuptools import setup, find_packages
setup(
    name = 'SMOF_MOF',
    version = "0.1",
    packages=find_packages(),
    install_requires = [
        'numpy>=1.23','numba>=0.56.0','scipy>=1.8.0'
    ],
)