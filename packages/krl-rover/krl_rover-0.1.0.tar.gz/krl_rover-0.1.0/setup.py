# setup.py
from setuptools import setup, find_packages

setup(
    name="krl_rover",  # Updated package name
    version="0.1.0",
    author="deshik7177",
    author_email="pdhanadeshik7177@gmail.com",
    description="A library to control a rover using Raspberry Pi",
    
    long_description_content_type="text/markdown",
    url="https://github.com/Deshik7177/krl_rover",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
