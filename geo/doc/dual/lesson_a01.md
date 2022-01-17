# Compile C++ for binding with Python

## Goals

Memorialize the the directions for C++ compilation of macOS, Linus, and Windows.

## Steps

### macOS

```bash
> conda activate siblenv
> cd ~/sibl/geo/src/dual
> 
```

### Linux

*To come.*

### Windows

```bash
> cd ~/sibl/geo/src/dual
> g++ -O3 -Wall -shared -std=c++11 -fPIC -fvisibility=hidden -IC:/Users/acsokol/Miniconda3/Include -IC:/Users/acsokol/Miniconda3/lib/site-packages/pybind11/include  main.cpp -o xybind.pyd -LC:/Users/acsokol/Miniconda3 -lpython39
```

#### Details

Split it up into a few different parts:

* First set of compiler flags are pretty standard, the two items that have required messing with were as follows:
  * The `visibility` flag which seems to be a newer pybind11 thing. 
  * The other is `Werror`, which I had to remove. It says to treat warnings as errors which we do not want.

```bash
> g++ -O3 -Wall -Werror -shared -std=c++11 -fPIC -fvisibility=hidden
```

#### Include Locations

These were the locations returned by the python include line, `$(python -m pybind11 --includes)`, that just runs nicely in Linux/macOS.  I loaded python and typed in the command to get the correct responses.

* `-IC:/Users/acsokol/Miniconda3/Include`
* `-IC:/Users/acsokol/Miniconda3/lib/site-packages/pybind11/include`
 
The list of cpp files to compile (later will include other cpp files) `main.cpp`.

This line gets filled in by `python-config` which didn't work either on windows, `xybind$(python3-config --extension-suffix)`.  The `pyd` seems to be a windows dll equivalent?? `xybind` name has to also appear in the `PYBIND11_MODULE(xybind, m)` line in the cpp file.
 
* `-o xybind.pyd`

This was the hangup for a long time, telling it where the `python39.dll` file was located and getting the correct syntax to link it. The capital `L` tells the compiler what folder to look in and the lower case `l` tells it the file with some assumed platform dependent extension.

* `-LC:/Users/acsokol/Miniconda3 -lpython39`
