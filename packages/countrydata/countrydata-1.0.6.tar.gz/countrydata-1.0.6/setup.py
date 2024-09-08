#importing libaries
from setuptools import setup

def readme():
    with open('README.md', encoding="utf8") as f:
        README = f.read()
    return README

#keywords for better performance
keywords = ['country', 'countrydata', 'countryinfo', 'country information' ,'country data' ,'country info']

setup(
    name="countrydata",
    version='1.0.6',
    # version = '1.0.9',
    description="An improved python package for retrieving data of all the countries in the world. Based on Manoj's",
    long_description=readme(),
    long_description_content_type="text/markdown",
    contact_email = 'gfxsetup@gmail.com',
    url="",
    author="Gabi",
    author_email="gfxsetup@gmail.com",
    keywords = keywords,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["countrydata"], #modules 
    include_package_data=True,
    install_requires=[""], #3rd party install requirements
    entry_points={
        "console_scripts": [
            "countrydata=countrydata.cli:main",
        ]
    },
)
