#!/usr/bin/env python

"""The setup script."""

import io
from os import path as op
from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

here = op.abspath(op.dirname(__file__))

# get the dependencies and installs
with io.open(op.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]

requirements = []

setup_requirements = []

test_requirements = []

setup(
    author="Liang Zhang, Ezra Kissel",
    author_email="lzhang9@es.net, kissel@es.net",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    description="QN Server (Controller) of Quant-Net",
    install_requires=install_requires,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="quant-net controller server",
    name="quantnet_controller",
    packages=find_packages(include=["quantnet_controller", "quantnet_controller.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/quant-net/quant-net-server",
    version="0.0.1",
    zip_safe=False,
    package_data={},
    entry_points={
        "console_scripts": [
            "quantnet_controller=quantnet_controller.cli:main",
        ],
    },
)
