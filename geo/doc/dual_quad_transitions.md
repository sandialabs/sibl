# primal/dual quadrilateral transitions

* *See also: [quadtree](quadtree.md)*

## Six Unique Strongly Balanced Transitions

Created with [dual_quad.py](../src/ptg/dual_quad.py) and [plot_dual_quad.py](plot_dual_quad.py):

| Template | Primal | Dual |
|:---:|:---:|:---:|
| `L0` Template_0000 | ![primal_quad_0000](fig/primal_quad_0000.png) | ![dual_quad_0000](fig/dual_quad_0000.png) 
| `Convex` Template_0001 | ![primal_quad_0001](fig/primal_quad_0001.png) | ![dual_quad_0001](fig/dual_quad_0001.png) 
| `Flat` Template_0011 | ![primal_quad_0011](fig/primal_quad_0011.png) | ![dual_quad_0011](fig/dual_quad_0011.png) |
| `Diagonal` Template_0110 | ![primal_quad_0110](fig/primal_quad_0110.png) | ![dual_quad_0110](fig/dual_quad_0110.png) 
| `Concave` Template_0111 | ![primal_quad_0111](fig/primal_quad_0111.png) | ![dual_quad_0111](fig/dual_quad_0111.png) 
| `L1` Template_1111 | ![primal_quad_1111](fig/primal_quad_1111.png) | ![dual_quad_1111](fig/dual_quad_1111.png) | 

## One Unique Weakly Balanced Transition

| Template | Primal | Dual |
|:---:|:---:|:---:|
| `L2` Template_0112 | ![primal_quad_0112](fig/primal_quad_0112.png) | ![dual_quad_0112](fig/dual_quad_0112.png) 

## Hash Table

* The hash table is composed
  * 16 stronly balanced templates,
    * Six templates are unique,
    * Ten templates are non-unique, and
  * Four weakly balanced template,
    * One template is unique,
    * Three templates are non-unique.


| `0000` | `0001` | `0010` | `0011` | `0100` | `0101` | `0110` | `0111` | 
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| ![primal_quad_0000](fig/primal_quad_0000.png) | ![primal_quad_0001](fig/primal_quad_0001.png) | ![primal_quad_0010](fig/primal_quad_0010.png) | ![primal_quad_0011](fig/primal_quad_0011.png) | ![primal_quad_0100](fig/primal_quad_0100.png) | ![primal_quad_0101](fig/primal_quad_0101.png) | ![primal_quad_0110](fig/primal_quad_0110.png) | ![primal_quad_0111](fig/primal_quad_0111.png) |
| ![dual_quad_0000](fig/dual_quad_0000.png) | ![dual_quad_0001](fig/dual_quad_0001.png) | ![dual_quad_0010](fig/dual_quad_0010.png) | ![dual_quad_0011](fig/dual_quad_0011.png) | ![dual_quad_0100](fig/dual_quad_0100.png) | ![dual_quad_0101](fig/dual_quad_0101.png) | ![dual_quad_0110](fig/dual_quad_0110.png) | ![dual_quad_0111](fig/dual_quad_0111.png) |


| `1000` | `1001` | `1010` | `1011` | `1100` | `1101` | `1110` | `1111` | 
|:------:|:------:|:------:|:------:|:------:|:------:|:------:|:------:|
| ![primal_quad_1000](fig/primal_quad_1000.png) | ![primal_quad_1001](fig/primal_quad_1001.png) | ![primal_quad_1010](fig/primal_quad_1010.png) | ![primal_quad_1011](fig/primal_quad_1011.png) | ![primal_quad_1100](fig/primal_quad_1100.png) | ![primal_quad_1101](fig/primal_quad_1101.png) | ![primal_quad_1110](fig/primal_quad_1110.png) | ![primal_quad_1111](fig/primal_quad_1111.png) |
| ![dual_quad_1000](fig/dual_quad_1000.png) | ![dual_quad_1001](fig/dual_quad_1001.png) | ![dual_quad_1010](fig/dual_quad_1010.png) | ![dual_quad_1011](fig/dual_quad_1011.png) | ![dual_quad_1100](fig/dual_quad_1100.png) | ![dual_quad_1101](fig/dual_quad_1101.png) | ![dual_quad_1110](fig/dual_quad_1110.png) | ![dual_quad_1111](fig/dual_quad_1111.png) |


| `0112` | `1021` | `1201` | `2110` |
|:------:|:------:|:------:|:------:|
| ![primal_quad_0112](fig/primal_quad_0112.png) | ![primal_quad_1021](fig/primal_quad_1021.png) | ![primal_quad_1201](fig/primal_quad_1201.png) | ![primal_quad_2110](fig/primal_quad_2110.png) | 
| ![dual_quad_0112](fig/dual_quad_0112.png) | ![dual_quad_1021](fig/dual_quad_1021.png) | ![dual_quad_1201](fig/dual_quad_1201.png) | ![dual_quad_2110](fig/dual_quad_2110.png) |
