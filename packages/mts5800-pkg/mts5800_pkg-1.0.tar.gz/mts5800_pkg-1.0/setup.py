# setup.py

from setuptools import setup, find_packages

setup(
    name="mts5800_pkg",
    version="1.0",
    packages=find_packages(),
    install_requires=[],  # Add dependencies here if any
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yatinarora01/mts5800_pkg",  # Replace with your project's URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify compatible Python versions
)
