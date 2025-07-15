#!/usr/bin/env python3
"""
Script d'installation pour le Classificateur d'Humour de Commits
"""

from setuptools import setup, find_packages
import os

# Lecture du README
with open("README_PORTABLE.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="commit-humor-classifier",
    version="1.0.0",
    author="Assistant IA",
    author_email="assistant@ia.com",
    description="Classificateur d'humour pour messages de commit basé sur EuroBERT-210m",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/commit-humor-classifier",
    py_modules=["commit_humor_classifier"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch>=1.9.0",
        "transformers>=4.20.0",
        "accelerate>=0.20.0",
        "huggingface_hub>=0.16.0",
    ],
    entry_points={
        "console_scripts": [
            "commit-humor=commit_humor_classifier:main",
        ],
    },
    include_package_data=True,
    keywords="humor classification commit git eurobert transformers nlp",
    project_urls={
        "Bug Reports": "https://github.com/username/commit-humor-classifier/issues",
        "Source": "https://github.com/username/commit-humor-classifier",
    },
)