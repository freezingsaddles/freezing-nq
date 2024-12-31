#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

version = "0.4.1"

long_description = """
freezing-nq is the Freezing Saddles component for receiving
strava webhook events and enquing them for processing.
"""

install_reqs = [
    "envparse",
    "falcon",
    "greenstalk",
    "gunicorn",
    "python-mimeparse",
    "six",
    "freezing-model",
    "arrow",
]

setup(
    name="freezing-nq",
    version=version,
    author="Hans Lellelid",
    author_email="hans@xmpl.org",
    url="http://github.com/freezingsaddles/freezing-nq",
    license="Apache",
    description="Freezing Saddles activity receive and enqueue worker",
    long_description=long_description,
    packages=["freezing.nq", "freezing.nq.api"],
    install_requires=install_reqs,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=True,
)
