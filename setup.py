from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csw",
    version="0.1.0",
    author="Cedric Sascha wagner",
    author_email="cedric.sascha.wagner@outlook.de",
    description="A flexible tree-like data structure for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/csw",  # Replace with actual repository URL if available
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
