# Quad Tree

* Given a 2D body, immerse it in a 2D square domain.
* Subdivide the domain into four quadrants (SW, NW, SE, NE), which define four level zero (L0) subdomains.
* Set the maximum number of subdivision levels, e.g, three successive subdivisions of L0 into L1 and then L1 into L2 and finally L2 into L3 has `nbi_max = 3`.
* For the singeton domain of side length of L0 (equivalently for each of the four subdomain quadrants SW, NW, SE, NE of side length L)), the following side lengths are related as
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
@phdthesis{shimada1993physically,
  title={Physically-based mesh generation: automated triangulation of surfaces and volumes via bubble packing},
  author={Shimada, Kenji},
  year={1993},
  school={Massachusetts Institute of Technology}
}
```
