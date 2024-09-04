# setup.py

from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='unit_ease',
    version='0.1',
    description='A simple unit converter package for length, temperature, weight, and volume conversions',
    long_description=long_description,  # Use the README file for the long description
    long_description_content_type='text/markdown',  # Ensures markdown is rendered correctly on PyPI
    author='Hari K',
    author_email='hariswdeveloper@gmail.com',
    packages=find_packages(),
    install_requires=[],  # No external dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='unit converter conversion length temperature weight volume',
)
