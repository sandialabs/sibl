# Lesson 00: Verify the configuration

To use the *SIBL Mesh Engine*, a Python environment called `siblenv` must be installed and configured.

## Goal

Verify that the `siblenv` environment has been configured correctly and is ready for use.

## Steps

Complete the [configuration](../../../config/README.md).  Then, from the command line, run the following: 

```bash
> cd ~/sibl
> conda activate siblenv
> pytest -v
> bash quality.sh
> bash style.sh
```

If all of the tests pass, then the environment has been configured correctly.

[Index](README.md)

Next: [Lesson 01](lesson_01.md)

