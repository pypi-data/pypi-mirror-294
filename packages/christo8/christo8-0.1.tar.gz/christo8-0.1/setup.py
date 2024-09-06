from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() #Gets the long description from Readme file

setup(
    name='christo8',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Add a comma here
    author='Aswin Christo',
    author_email='christopython20006@gmail.com',
    description='This is a python predefined function containg some of the basic code ',

    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
     project_urls={
           'Source Repository': 'https://github.com/AswinChristo17/christo_python_module' #replace with your github source
    },
     
)
