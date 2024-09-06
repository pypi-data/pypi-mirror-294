from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.6'
DESCRIPTION = 'mlplay'
LONG_DESCRIPTION = 'radip development of models '

# Setting up
setup(
    name="mlplay",
    version=VERSION,
    author="onemriganka",
    
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["torch","matplotlib","torchvision"],
    keywords=[ 'ml','onemriganka','codes'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
