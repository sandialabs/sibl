# quadtree

## Numbering Convention

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

Created with [plot_quadtree.py](plot_quadtree.py):

* `L0` square domain $$(x, y) \in ([1, 3] \otimes  [-1, 1])$$
* Single point at `(2.6, 0.6)` to trigger refinement.

| | | | 
|:---:|:---:|:---:|
![plot_quadtree_L0](fig/plot_quadtree_L0.png) | ![plot_quadtree_L0](fig/plot_quadtree_L1.png) | ![plot_quadtree_L0](fig/plot_quadtree_L2.png) |
![plot_quadtree_L0](fig/plot_quadtree_L3.png) | ![plot_quadtree_L0](fig/plot_quadtree_L4.png) | ![plot_quadtree_L0](fig/plot_quadtree_L5.png) |

## Rebalancing

Created with [plot_quadtree.py](plot_quadtree.py):

| before | after |
|:---:|:---:|
| ![rebalance_pre](fig/rebalance_pre.png) | ![rebalance_post](fig/rebalance_post.png) |
| ![plot_quadtree_npts_9](fig/plot_quadtree_npts_9.png) | |
| ![plot_quadtree_npts_5](fig/plot_quadtree_npts_5.png) | |
| ![plot_quadtree_npts_3](fig/plot_quadtree_npts_3.png) | |
