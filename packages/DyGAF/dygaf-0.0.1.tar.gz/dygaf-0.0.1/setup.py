from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='DyGAF',
    version='0.0.1',
    description='A package for attention model pipeline and feature analysis',
    long_description=long_description,  # This will pull in the README as the long description
    long_description_content_type='text/markdown',  # Specify that the README is in markdown format
    author='Md Khairul Islam, Prof Hairong Wei',
    author_email='hairong@mtu.edu',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'tensorflow',
        'xgboost',
    ],
    entry_points={
        'console_scripts': [
            'DyGAF=DyGAF.main:main',  # Define the CLI command
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.3',
)
