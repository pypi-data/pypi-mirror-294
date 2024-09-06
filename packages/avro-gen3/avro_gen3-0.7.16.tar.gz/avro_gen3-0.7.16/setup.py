"""
A setuptools-based setup module.

See:
https://github.com/acryldata/avro_gen
"""

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
if path.exists(path.join(here, "README.md")):
    with open(path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="avro-gen3",
    version="0.7.16",
    description="Avro record class and specific record reader generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acryldata/avro_gen",
    author="Harshal Sheth",
    author_email="hsheth2@gmail.com",
    license="License :: OSI Approved :: Apache Software License",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: Apache Software License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="avro class generator",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    package_data={
        "avrogen": ["py.typed"],
    },
    install_requires=[
        "avro>=1.10",
        "six",
    ],
)
