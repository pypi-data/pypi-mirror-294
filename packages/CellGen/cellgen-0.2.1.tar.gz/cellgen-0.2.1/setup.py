
import os
from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name='CellGen',                 # Package name
    version='0.2.1',                         # Version
    author='Rom Uddamvathanak',                      # Your name
    author_email='vathanakuddam@gmai.com',   # Your email
    description='CellGen: a computational model for predicting the cellular response to diverse perturbation',   # Short description
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JinmiaoChenLab/CellGenpy', # Project URL
    packages=find_packages(),                # Automatically find packages
    install_requires=[
        'numpy==1.24.3',
        'pandas==1.5.3',
        'scanpy==1.10.2',
        'scipy==1.12.0',
        'numba==0.57.1',
        'colorcet==3.0.1',
        'scikit-learn==1.3.2',
        'gseapy==1.1.0',
        'seaborn==0.13.0',
        'jupyter'
    ], # Dependencies inlined
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',                 # Minimum Python version
)