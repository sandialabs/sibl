# Quad Tree

* Given a 2D body, immerse it in a 2D square domain.
* Subdivide the domain into four quadrants (`sw`, `nw`, `se`, `ne`), which define four level zero (L0) subdomains.
* Set the maximum number of subdivision levels, e.g, three successive subdivisions of L0 into L1 and then L1 into L2 and finally L2 into L3 has `nbi_max = 3`.  
  * *This is the **recursion stopping criterion** for this implementation.*  
  * Other stopping criteria include (a) maximum number of entities allowed in a quadrant, or (b) a minimum quadrant side length is reached.
* For the singleton domain of side length of L0 (equivalently for each of the four subdomain quadrants SW, NW, SE, NE of side length L)), the following side lengths are related as
  * `L1 = L0 / 2 = L0 / (2^1)` # The first subdivision, *etc.*
  * `L2 = L1 / 2 = L0 / (2^2)`
  * `L3 = L2 / 2 = L0 / (2^3)`
  * `Ln = ........ L0 / (2^n)`
* Example: given a domain of side length `L0 = 16 cm`
  * `L1 = 8 cm`
  * `L2 = 4 cm`
  * `L3 = 2 cm`
  * `L4 = 1 cm`
  * `L5 = 0.5 cm`
  * *etc.*

```python
def refine(domain: 2Dsquare, level: int = 1):
    # create four subdomains
    

    for s in subdomains:
        if self.body.fully_contains(s) or 
           self.body.fully_excludes(s):
           # no further refinement
           return
        else:
            # s contains the body boundary
            refine(s, level + 1)  # recursion
```

## References:

```bash
@article{liang2010guaranteed,
  title={Guaranteed-quality all-quadrilateral mesh generation with feature preservation},
  author={Liang, Xinghua and Ebeida, Mohamed S and Zhang, Yongjie},
  journal={Computer Methods in Applied Mechanics and Engineering},
  volume={199},
  number={29-32},
  pages={2072--2083},
  year={2010},
  publisher={Elsevier},
  note={\url{https://scholar.archive.org/work/low5zpwnnjbaznempizlbey2mi/access/wayback/http://www.imr.sandia.gov/papers/imr18/Liang.pdf}},
}

@article{rushdi2017all,
  title={All-quad meshing without cleanup},
  author={Rushdi, Ahmad A and Mitchell, Scott A and Mahmoud, Ahmed H and Bajaj, Chandrajit C and Ebeida, Mohamed S},
  journal={Computer-Aided Design},
  volume={85},
  pages={83--98},
  year={2017},
  publisher={Elsevier},
  note={\url{https://doi.org/10.1016/j.cad.2016.07.009},\url{https://www.sciencedirect.com/science/article/am/pii/S001044851630080X}},
}

@phdthesis{shimada1993physically,
  title={Physically-based mesh generation: automated triangulation of surfaces and volumes via bubble packing},
  author={Shimada, Kenji},
  year={1993},
  school={Massachusetts Institute of Technology},
  note={\url{https://dspace.mit.edu/bitstream/handle/1721.1/12332/29019892-MIT.pdf?sequence=2}}
}
```

* Hill, Christian. [christian](https://scipython.com/blog/quadtrees-2-implementation-in-python/) Quadtrees #2: Implementation in Python, 19 Apr 2020.
* Russell, Jeffery. [JRTECHS](https://jrtechs.net/data-science/implementing-a-quadtree-in-python) Implementing a Quadtree in Python, 10 Oct 2020.
