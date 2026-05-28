#!/usr/bin/env python3
"""Setup script for Squad Content Digest CLI"""

from setuptools import setup

setup(
    name="squad-content-digest",
    version="1.4.1",
    description="Content Digest CLI for Seneca - Scans learnings/ for tweet drafts and blog angles",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="OpenSeneca",
    author_email="admin@openseneca.org",
    url="https://github.com/OpenSeneca/squad-content-pipeline",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'content-digest=content_pipeline.main:main',
        ],
    },
)