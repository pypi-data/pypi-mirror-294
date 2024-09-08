"""
Company Name: Parendum OÜ
Creation Date: September 2023
Copyright © 2023 Parendum OÜ. All rights reserved.

Description:
This file is part of Parendum Astra Api library.
Unauthorized use, reproduction, modification, or distribution without the
express consent of Parendum OÜ is strictly prohibited.

Contact:
info@parendum.com
https://parendum.com
"""

from setuptools import setup, find_packages

setup(
    name="parendum_astra_api",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "pycryptodome",
        "requests"
    ],
    author="Parendum OÜ",
    author_email="info@parendum.com",
    description="A library to interact with the Astra Portal API of Parendum.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/parendumteam/parendum-astra-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
