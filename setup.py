import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xyfigure",
    version="0.0.3",
    author="Chad B. Hovey",
    author_email="chovey@sandia.gov",
    description="A library for xy plotting and processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandialabs/sibl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
