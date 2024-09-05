from setuptools import setup, find_packages

setup(
    name='weatherAUS',
    version='1.0',
    packages=find_packages(),
    description='A module for reading weatherAUS.csv and analyzing its data.',
    author='Zaq Holdsworth',
    author_email='zaq.holdsworth@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.9', 
)