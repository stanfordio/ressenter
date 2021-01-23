import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ressenter",
    version="0.0.3",
    description="Toolkit for Dissenter",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stanfordio/ressenter",
    author_email="mccain@stanford.edu",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["beautifulsoup4", "requests", "click", "unicodecsv", "dateparser"],
    entry_points={
        "console_scripts": [
            "rissenter=rissenter.cli:cli",
        ]
    },
)