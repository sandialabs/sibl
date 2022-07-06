# Lesson 04c: Mesh Smoothing

## Goal

Quantify what effect mesh smoothing has on mesh quality.

## Methods

Compare the minimum scaled Jacobian quality metric for the mesh in the previous lesson
*before* and *after* smoothing.

## Steps

```bash
> conda activate siblenv
> cd ~/sibl/geo/doc/dual/lesson_04
> python lesson_04c.py
```

## Results

![lesson_04c_histogram](fig/lesson_04c_histogram.png)

## Context from Previous Lesson

* Animation of smoothing

![lesson_04b_iter__opt](fig/lesson_04b_iter__opt.gif)

Linear Scale | Log Scale
--|--
![lesson_04b_convergence](fig/lesson_04b_convergence.png) | ![lesson_04b_convergence_log](fig/lesson_04b_convergence_log.png)

* Convergence tolerance: `0.1`
* Number of iterations: `18`
