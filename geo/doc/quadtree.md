# quadtree

## Numbering convention

* *x* is the dominant (first) axis
* *y* is the subordinant (second) axis
* Level 0: blue (0 bisections: 2^0 = 1 quad per side length)
  * Level 1: orange (1 bisection: 2^1 = 2 quads per side length)
    * Level 2: green (2 bisections: 2^2 = 4 quads per side length)
      * Level 3: red (3 bisections: 2^3 = 8 quads per side length)

Created with [plot_quadtree_convention.py](plot_quadtree_convention.py):

![plot_quadtree_convention](fig/plot_quadtree_convention.png)

Created with [fig_quadtree.tex](fig_quadtree.tex):

![fig_quadtree](fig/fig_quadtree.png)

## Refinement Example

* `L0` square domain $$(x, y) \in ([1, 3] \otimes  [-1, 1])$$
* Single point at `(2.6, 0.6)` to trigger refinement.


| `level_max` | quadtree |
|:---:|:---:|
| `0` | ![plot_quadtree_L0](fig/plot_quadtree_L0.png) |
| `1` | ![plot_quadtree_L0](fig/plot_quadtree_L1.png) |
| `2` | ![plot_quadtree_L0](fig/plot_quadtree_L2.png) |
| `3` | ![plot_quadtree_L0](fig/plot_quadtree_L3.png) |
| `4` | ![plot_quadtree_L0](fig/plot_quadtree_L4.png) |
| `5` | ![plot_quadtree_L0](fig/plot_quadtree_L5.png) |
| `6` | ![plot_quadtree_L0](fig/plot_quadtree_L6.png) |
