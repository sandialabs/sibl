# Lesson 04b: Mesh Smoothing

## Goal

Given the mesh developed in the previous less, using Laplacian iterations to smooth the mesh.

## Steps

```bash
> conda activate siblenv
> cd ~/sibl/geo/doc/dual/lesson_04
> python lesson_04b.py
```

## Results

* Animation of smoothing

![lesson_04b_iter__opt](fig/lesson_04b_iter__opt.gif)

Linear Scale | Log Scale
--|--
![lesson_04b_convergence](fig/lesson_04b_convergence.png) | ![lesson_04b_convergence_log](fig/lesson_04b_convergence_log.png)

* Convergence tolerance: `0.1`
* Number of iterations: `18`