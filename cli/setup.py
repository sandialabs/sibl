import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="SIBL xyfigure, a library for xy plotting and processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Chad B. Hovey",
    maintainer_email="chovey@sandia.gov",
    name="xyfigure",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    url="https://github.com/sandialabs/sibl",
    version="0.0.9",
)
