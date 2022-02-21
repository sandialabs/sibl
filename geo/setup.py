import setuptools
from distutils.util import convert_path

package_name = "ptg"

# version from .py file
setup_dict = {}
ver_path = convert_path("src/" + package_name + "/__version__.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), setup_dict)

with open("../README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="SIBL xyfigure, PTG extension",
    entry_points={
        "console_scripts": [
            "cli-hello=ptg.command_line:say_hello",
            "version=ptg.command_line:version",
            "pydual=ptg.main:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Chad B. Hovey",
    maintainer_email="chovey@sandia.gov",
    # name="ptg",
    name=package_name,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    url="https://github.com/sandialabs/sibl",
    # version="0.0.3",
    version=setup_dict["__version__"],
)


"""
References:
entry_points, console_scripts, setup.py
https://docs.astropy.org/en/latest/development/scripts.html
https://stackoverflow.com/questions/774824/explain-python-entry-points
"""
