#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

with open(here / "README.rst") as readme_file:
    readme = readme_file.read()

with open(here / "HISTORY.rst") as history_file:
    history = history_file.read()

setup(
    author="Michael Aye",
    author_email="kmichael.aye@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Tools for working with LRO Diviner data",
    entry_points={
        "console_scripts": [
            "divinerpy=divinerpy.cli:main",
        ],
    },
    install_requires=[
        "pandas",
        "importlib_resources; python_version<'3.9'",
    ],
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="divinerpy",
    name="divinerpy",
    package_dir={"": "src"},
    package_data={"divinerpy": ["data/*"]},
    packages=find_packages(where="src"),
    test_suite="tests",
    tests_require=["pytest"],
    url="https://github.com/michaelaye/divinerpy",
    version="0.2.0",
    zip_safe=False,
)
