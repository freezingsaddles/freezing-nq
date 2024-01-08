# -*- coding: utf-8 -*-
import os.path
import re
import warnings

from setuptools import setup

version = "0.3.6"

long_description = """
freezing-nq is the Freezing Saddles component for receiving
strava webhook events and enquing them for processing.
"""

install_reqs = [
    "envparse==0.2.0",
    "falcon==2.0.0",
    "greenstalk==1.0.1",
    "gunicorn==20.0.4",
    "python-mimeparse==1.6.0",
    "six==1.14.0",
    "freezing-model",
    "arrow==0.15.5",
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
