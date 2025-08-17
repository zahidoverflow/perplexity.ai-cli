#!/usr/bin/env python3
"""
Setup script for perplexity-cli
Optimized for pipx installation
"""

from setuptools import setup
import os

def read_file(filename):
    """Read a file and return its contents."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def read_requirements():
    """Read requirements from requirements.txt."""
    requirements = []
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    except FileNotFoundError:
        # Fallback requirements
        requirements = ["websocket-client>=1.6.0", "requests>=2.28.0"]
    return requirements

# Read version from the main module
def get_version():
    """Extract version from the main module."""
    try:
        with open("perplexity_cli.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except:
        return "2.1.0"

setup(
    name="perplexity-cli",
    version=get_version(),
    author="zahidoverflow",
    author_email="imzooel@gmail.com",
    description="A command-line interface for Perplexity AI with web search capabilities",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/zahidoverflow/perplexity-cli",
    project_urls={
        "Homepage": "https://github.com/zahidoverflow/perplexity-cli",
        "Repository": "https://github.com/zahidoverflow/perplexity-cli",
        "Bug Reports": "https://github.com/zahidoverflow/perplexity-cli/issues",
        "Documentation": "https://github.com/zahidoverflow/perplexity-cli#readme",
        "Changelog": "https://github.com/zahidoverflow/perplexity-cli/blob/main/CHANGELOG.md",
    },
    py_modules=["perplexity_cli"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Utilities",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "perplexity-cli=perplexity_cli:main",
            "pplx=perplexity_cli:main",  # Short alias
        ],
    },
    keywords=[
        "perplexity", "ai", "cli", "chatbot", "assistant", "search",
        "command-line", "pipx", "artificial-intelligence", "web-search"
    ],
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)
