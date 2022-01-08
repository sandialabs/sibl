# Lesson 00: Verify the configuration

The **goal** of this lesson is to verify that the local `siblenv` environment has been [configured](../../../config/README.md) and is ready for use.

From the command line, activate the `siblenv` environment, then start python.

```bash
> cd ~/sibl
> conda activate siblenv
> pytest -v
> bash quality.sh
> bash style.sh
```

If all of the tests pass, then the environment has been configured correctly.

[ [Index](README.md) ]
[ Next: [Lesson 01](lesson_01.md) ]

