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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
