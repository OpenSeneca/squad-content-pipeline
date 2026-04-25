from setuptools import setup, find_packages

setup(
    name="content-pipeline",
    version="1.1.0",
    description="CLI tool to extract tweet drafts and blog angles from agent learnings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Archimedes (OpenSeneca Squad)",
    url="https://github.com/OpenSeneca/content-pipeline",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'content-digest=content_pipeline.main:main',
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
