from setuptools import setup, find_packages
setup(
    name = 'SMOF_MOF',
    version = "0.2",
    packages=find_packages(),
    install_requires = [
        'numpy>=1.23','numba>=0.56.0','scipy>=1.8.0','scikit-learn>=1.2.0',
    ],
)