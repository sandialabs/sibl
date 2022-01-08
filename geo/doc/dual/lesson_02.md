# Lesson 02: Run Lesson 01 from python script

Prerequisite: [Lesson 01](lesson_01.md)

It is often easier to interact with the `xybind` library through the use of a 
Python script, instead of using Python interactively.

The **goal** of this lesson is to move the interactive content from [Lesson 01](lesson_01.md) into a script and then obtain the same output as in the previous lesson.

The interactive steps from the procedural approach are wrapped into a python script as follows:

```python
# This is the concept of modifying lesson_01 to obtain lesson_02.py;
# it is not a runnable python script.  See `lesson_02.py` for the
# runnable python script.

import math
import matplotlib.pyplot as plt

import xybind as xyb

def main():
    # The procedural steps from the previous lesson are pasted here.


if __name__ == "__main__":
    main()
```

Then, run this python script, [`lesson_02.py`](lesson_02.py) from the command line:

```bash
> conda activate siblenv
> cd ~/sibl/geo/doc/dual
> python lesson_02.py
```

The same figure created in Lesson 01 should appear again for this lesson:

![circle_boundary](fig/circle_boundary.png)

[ [Index](README.md) ]
[ Next: [Lesson 03](lesson_03.md) ]

