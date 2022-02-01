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

If all of the tests pass, then the environment has been configured correctly.  Following are details of what to expect:

```bash
> pytest -v  # will run the tests in a verbose manner and produce output as follows
===================================== test session starts =====================================
platform darwin -- Python 3.9.7, pytest-6.2.5, py-1.9.0, pluggy-0.12.0 -- /Users/chovey/opt/miniconda3/envs/siblenv/bin/python
cachedir: .pytest_cache
rootdir: /Users/chovey/sibl
plugins: cov-2.10.1
collected 214 items

cli/process/tpav/test_three_points_angular_velocity.py::ThreePointsAngularVelocityTest::test_t0 PASSED [  0%]
cli/process/tpav/test_three_points_angular_velocity.py::ThreePointsAngularVelocityTest::test_t0_insufficient_rank_omega_parallel XFAIL [  0%]
cli/process/tpav/test_three_points_angular_velocity.py::ThreePointsAngularVelocityTest::test_t0_insufficient_rank_omega_perpendicular XFAIL [  1%]
cli/process/tpav/test_three_points_angular_velocity.py::ThreePointsAngularVelocityTest::test_t0_t1 PASSED [  1%]
cli/tests/test_functional_architecture.py::test_Csv PASSED                              [  2%]
cli/tests/test_functional_architecture.py::test_csv_data PASSED                         [  2%]
cli/tests/test_functional_architecture.py::test_Figure PASSED                           [  3%]
cli/tests/calculator/test_calculator.py::MyTestCase::test_add PASSED                    [  3%]
cli/tests/calculator/test_calculator.py::MyTestCase::test_divide PASSED                 [  4%]
cli/tests/calculator/test_calculator.py::MyTestCase::test_multiply PASSED               [  4%]
cli/tests/calculator/test_calculator.py::MyTestCase::test_subtract PASSED               [  5%]

...  # abbreviated

geo/tests/test_xybind.py::test_unit_square_contains PASSED                              [ 98%]
geo/tests/test_xybind.py::test_unit_squares_inType PASSED                               [ 99%]
geo/tests/test_xybind.py::test_qt_node_counts PASSED                                    [ 99%]
geo/tests/test_xybind.py::test_unit_circle_quad_mesh PASSED                             [100%]

========================= 195 passed, 3 skipped, 16 xfailed in 6.14s ==========================
```


```bash
> ./quality.sh                                        (siblenv)
===================================== test session starts =====================================
platform darwin -- Python 3.9.7, pytest-6.2.5, py-1.9.0, pluggy-0.12.0
rootdir: /Users/chovey/sibl
plugins: cov-2.10.1
collected 214 items

cli/process/tpav/test_three_points_angular_velocity.py .xx.                             [  1%]
cli/tests/test_functional_architecture.py ...                                           [  3%]
cli/tests/calculator/test_calculator.py ....                                            [  5%]
cli/tests/correlation/test_correlation.py ..................                            [ 13%]
cli/tests/differentiation/test_differentiation.py ....                                  [ 15%]

...  # abbreviated

geo/src/ptg/point.py                       23      0   100%
geo/src/ptg/polygon.py                     34      1    97%   39
geo/src/ptg/quadtree.py                   212      9    96%   284-288, 702-708, 711-717, 720-726
geo/src/ptg/reader.py                      44     20    55%   45, 56, 66-71, 79, 96-98, 108-119
geo/src/ptg/regularize_radial.py            7      0   100%
geo/src/ptg/view_bernstein_surface.py      89      6    93%   173-178, 206
geo/src/ptg/view_bezier.py                241     13    95%   524, 529-532, 537-554, 558
geo/src/ptg/view_bspline.py               321     27    92%   210-211, 479-482, 493-508, 670, 673, 676, 752, 757-765, 770-789, 793
---------------------------------------------------------------------
TOTAL                                    1902    198    90%


========================= 195 passed, 3 skipped, 16 xfailed in 8.77s ==========================
```

```bash
> ./style.sh                                          (siblenv)
Skipping .ipynb files as Jupyter dependencies are not installed.
You can fix this by running ``pip install black[jupyter]``
All done! ✨ 🍰 ✨
118 files would be left unchanged.
```

[Index](README.md)

Next: [Lesson 01](lesson_01.md)

