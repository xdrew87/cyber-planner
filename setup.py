#!/usr/bin/env python3
"""
Setup script for Cyber Planner
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cyber-planner",
    version="2.0.0",
    author="galmx (xdrew87)",
    author_email="your-email@example.com",
    description="A powerful, dark-themed task scheduling and planning application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xdrew87/cyber-planner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt6>=6.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "PyInstaller>=5.0.0",
            "flake8>=3.9.0",
            "pylint>=2.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "cyber-planner=main:main",
        ]
    },
)
