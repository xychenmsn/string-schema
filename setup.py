"""
Setup script for Simple Schema package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simple-schema",
    version="1.0.0",
    author="Simple Schema Team",
    author_email="team@simple-schema.dev",
    description="A simple, LLM-friendly schema definition library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simple-schema/simple-schema",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "simple-schema=simple_schema.cli:main",
        ],
    },
    keywords="schema validation json llm ai data-extraction",
    project_urls={
        "Bug Reports": "https://github.com/simple-schema/simple-schema/issues",
        "Source": "https://github.com/simple-schema/simple-schema",
        "Documentation": "https://simple-schema.readthedocs.io/",
    },
)
