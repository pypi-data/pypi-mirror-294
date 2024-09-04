# setup.py
from setuptools import setup, find_packages

setup(
    name="rk-p2",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "rk-p=cli:main",
        ],
    },
    install_requires=[],
    description="A simple package to just troll your friends with to use run: rk-p",
    author="galaxyfounded",
    author_email="host@literun.rf.gd",
)
