#!/usr/bin/env python

from setuptools import find_packages, setup


def from_file(file_name: str):
    with open(file_name, "r") as f:
        return f.read().splitlines()


def long_description():
    text = open("README.md", encoding="utf-8").read()
    # SVG images are not readable on PyPI, so replace them  with PNG
    text = text.replace(".svg", ".png")
    return text


setup(
    name="corider",
    version="0.1.4",
    description="Tiny configuration library tailored for Deep Learning project and the Ride.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    author="Lukas Hedegaard",
    author_email="lxhdgd@gmail.com",
    url="https://github.com/LukasHedegaard/co-rider",
    install_requires=[],
    extras_require={
        "dev": ["isort", "black", "flake8", "flake8-black"],
        "test": ["pytest", "pytest-cov", "flake8", "flake8-black", "ray[tune]"],
        "build": ["setuptools", "wheel", "twine"],
    },
    packages=find_packages(),
    keywords=["deep learning", "configuration", "ride"],
    classifiers=[
        "Environment :: Console",
        "Natural Language :: English",
        # How mature is this project? Common values are
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        # Pick your license as you wish
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
