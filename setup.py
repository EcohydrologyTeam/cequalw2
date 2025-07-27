from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cequalw2",
    version="1.0.0",
    author="Todd E. Steissberg, PhD, PE",
    author_email="",
    description="Python library for reading, writing, and visualizing CE-QUAL-W2 model data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ecohydrology/cequalw2-Claude",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Hydrology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
        "matplotlib>=3.0.0",
        "seaborn>=0.10.0",
        "h5py>=2.10.0",
        "pyyaml>=5.3",
        "holoviews>=1.13.0",
        "bokeh>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
    },
)