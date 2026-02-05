from setuptools import setup, find_packages

setup(
    name="cardinalitykit",
    version="1.0.0",
    author="CardinalityKit",
    description="A comprehensive toolkit for cardinality estimation algorithms",
    long_description=open("cardinalitykit/README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.1.0",
        "tqdm>=4.50.0",
        "scipy>=1.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    keywords="cardinality estimation hyperloglog hyperreal probabilistic counting",
    project_urls={
        "Documentation": "https://github.com/cardinalitykit/cardinalitykit",
        "Source": "https://github.com/cardinalitykit/cardinalitykit",
        "Tracker": "https://github.com/cardinalitykit/cardinalitykit/issues",
    },
)