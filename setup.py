from setuptools import setup, find_packages

setup(
    name="delta-optimizer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Automatic AI training optimization with Δ† theory - just plug and play",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/delta-optimizer",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)