# primal/dual quadrilateral transitions

* *See also: [quadtree](quadtree.md)*

## Six Unique Strongly Balanced Transitions

Created with [dual_quad.py](../src/ptg/dual_quad.py) and [plot_dual_quad.py](plot_dual_quad.py):

| Template Key | Primal | Dual |
|:---:|:---:|:---:|
| `key_0000` *L1* | ![primal_quad_0000](fig/primal_quad_0000.png) | ![dual_quad_0000](fig/dual_quad_0000.png) 
| `key_0001` *convex* | ![primal_quad_0001](fig/primal_quad_0001.png) | ![dual_quad_0001](fig/dual_quad_0001.png) 
| `key_0011` *wave* | ![primal_quad_0011](fig/primal_quad_0011.png) | ![dual_quad_0011](fig/dual_quad_0011.png) |
| `key_0110` *diagonal* | ![primal_quad_0110](fig/primal_quad_0110.png) | ![dual_quad_0110](fig/dual_quad_0110.png) 
| `key_0111` *concave* | ![primal_quad_0111](fig/primal_quad_0111.png) | ![dual_quad_0111](fig/dual_quad_0111.png) 
| `key_1111` *L2* | ![primal_quad_1111](fig/primal_quad_1111.png) | ![dual_quad_1111](fig/dual_quad_1111.png) | 

## One Unique Weakly Balanced Transition

| Template | Primal | Dual |
|:---:|:---:|:---:|
| `key_0112` *weak* | ![primal_quad_0112](fig/primal_quad_0112.png) | ![dual_quad_0112](fig/dual_quad_0112.png) 

## Hash Table

* The hash table is composed
  * 16 strongly balanced templates,
    * Six templates are unique,
    * Ten templates are non-unique, and
  * Four weakly balanced template,
    * One template is unique,
    * Three templates are non-unique.


| `key_0000` | `key_0001` | `key_0010` | `key_0011` | `key_0100` | `key_0101` | `key_0110` | `key_0111` | 
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| ![primal_quad_0000](fig/primal_quad_0000.png) | ![primal_quad_0001](fig/primal_quad_0001.png) | ![primal_quad_0010](fig/primal_quad_0010.png) | ![primal_quad_0011](fig/primal_quad_0011.png) | ![primal_quad_0100](fig/primal_quad_0100.png) | ![primal_quad_0101](fig/primal_quad_0101.png) | ![primal_quad_0110](fig/primal_quad_0110.png) | ![primal_quad_0111](fig/primal_quad_0111.png) |
| ![dual_quad_0000](fig/dual_quad_0000.png) | ![dual_quad_0001](fig/dual_quad_0001.png) | ![dual_quad_0010](fig/dual_quad_0010.png) | ![dual_quad_0011](fig/dual_quad_0011.png) | ![dual_quad_0100](fig/dual_quad_0100.png) | ![dual_quad_0101](fig/dual_quad_0101.png) | ![dual_quad_0110](fig/dual_quad_0110.png) | ![dual_quad_0111](fig/dual_quad_0111.png) |


| `key_1000` | `key_1001` | `key_1010` | `key_1011` | `key_1100` | `key_1101` | `key_1110` | `key_1111` | 
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| ![primal_quad_1000](fig/primal_quad_1000.png) | ![primal_quad_1001](fig/primal_quad_1001.png) | ![primal_quad_1010](fig/primal_quad_1010.png) | ![primal_quad_1011](fig/primal_quad_1011.png) | ![primal_quad_1100](fig/primal_quad_1100.png) | ![primal_quad_1101](fig/primal_quad_1101.png) | ![primal_quad_1110](fig/primal_quad_1110.png) | ![primal_quad_1111](fig/primal_quad_1111.png) |
| ![dual_quad_1000](fig/dual_quad_1000.png) | ![dual_quad_1001](fig/dual_quad_1001.png) | ![dual_quad_1010](fig/dual_quad_1010.png) | ![dual_quad_1011](fig/dual_quad_1011.png) | ![dual_quad_1100](fig/dual_quad_1100.png) | ![dual_quad_1101](fig/dual_quad_1101.png) | ![dual_quad_1110](fig/dual_quad_1110.png) | ![dual_quad_1111](fig/dual_quad_1111.png) |


| `key_0112` | `key_1021` | `key_1201` | `key_2110` |
|:------:|:------:|:------:|:------:|
| ![primal_quad_0112](fig/primal_quad_0112.png) | ![primal_quad_1021](fig/primal_quad_1021.png) | ![primal_quad_1201](fig/primal_quad_1201.png) | ![primal_quad_2110](fig/primal_quad_2110.png) | 
| ![dual_quad_0112](fig/dual_quad_0112.png) | ![dual_quad_1021](fig/dual_quad_1021.png) | ![dual_quad_1201](fig/dual_quad_1201.png) | ![dual_quad_2110](fig/dual_quad_2110.png) |

## Assembly

| `key_0001_r0_p0` | `key_0001_r0_p1` | `key_0001_r1_p0` | `key_0001_r1_p1` |
|:------:|:------:|:------:|:------:|
| ![plot_dual_quad_0001_r0_p0](fig/plot_dual_quad_0001_r0_p0.png) | ![plot_dual_quad_0001_r0_p1](fig/plot_dual_quad_0001_r0_p1.png) | ![plot_dual_quad_0001_r1_p0](fig/plot_dual_quad_0001_r1_p0.png) | ![plot_dual_quad_0001_r1_p1](fig/plot_dual_quad_0001_r1_p1.png) | 


| primal mesh | `key_0001_r0_p1` | `key_0001_r1_p0` | `key_0001_r1_p1` |
|:------:|:------:|:------:|:------:|
| ![plot_quadtree_nested_0001a](fig/plot_quadtree_nested_0001a.png) | ![plot_quadtree_nested_0001b](fig/plot_quadtree_nested_0001b.png) | ![plot_quadtree_nested_0001c](fig/plot_quadtree_nested_0001c.png) | ![plot_quadtree_nested_0001d](fig/plot_quadtree_nested_0001d.png) | 


![plot_quadtree_concentric_convex](fig/plot_quadtree_concentric_convex.png)
> *Illustration of three concentric levels using the convex transition, Template_0001. The assembled dual mesh is (partly, sufficient to demonstrate symmetric) shown in blue.*