from setuptools import setup, find_packages

setup(
    name="squad-content-pipeline",
    version="1.2.1",
    description="Content Pipeline CLI for Seneca - Scans learnings/ for tweet drafts and blog angles",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="OpenSeneca",
    url="https://github.com/OpenSeneca/squad-content-pipeline",
    py_modules=["main"],
    install_requires=[
        # No external dependencies - uses only Python stdlib
    ],
    entry_points={
        "console_scripts": [
            "content-pipeline=main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
