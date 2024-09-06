from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ulti-manager',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'ulti=ulti_manager.cli:cli',
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
