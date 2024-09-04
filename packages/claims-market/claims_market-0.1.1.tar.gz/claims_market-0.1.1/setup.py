# setup.py

from setuptools import setup, find_packages

setup(
    name="claims_market",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
    ],
    author="Patrick Ashrafi",
    author_email="pa@ai-holding.com",
    description="A library to fetch and process data from the Claims Market API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claims_market",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
