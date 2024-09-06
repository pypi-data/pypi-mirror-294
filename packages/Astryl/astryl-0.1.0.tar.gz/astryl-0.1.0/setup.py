# setup.py
from setuptools import setup, find_packages

setup(
    name="Astryl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'neo4j',
        'pandas',
        # Add other dependencies here
    ],
    author="Heinrich Schanckenberg",
    author_email="heinrich2cs@gmail.com",
    description="A library for managing Neo4j operations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
