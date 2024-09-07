from setuptools import setup, find_packages
import os

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md"), "r") as fh:
    LONG_DESCRIPTION = fh.read()

# Read the requirements from requirements.txt
with open(os.path.join(HERE, 'requirements.txt')) as f:
    required = f.read().splitlines()

VERSION = '2.1'
DESCRIPTION = 'OmniMorpher - Code based video editor'

setup(
    name="OmniMorpher", 
    version=VERSION,
    author="Hanan Basheer",
    author_email="hanan.basheer@iitb.ac.in",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,  # Use the requirements read from the file
    keywords=['python', 'OmniMorpher', 'video', 'editor'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)