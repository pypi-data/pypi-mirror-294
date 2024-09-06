from setuptools import setup, find_packages

setup(
    name="ulti-manager",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ulti=ulti.main:main',
        ],
    },
    description="A plugin-based CLI framework",
)