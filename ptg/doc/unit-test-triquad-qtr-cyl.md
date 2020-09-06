# unit test triquadratic quarter cylinder

## Objective

* Construct an approximation of a quarter cylinder from triquadratic Bezier controls

## Methods

<img src="fig/triquad-001.png" alt="triquad-001" width="300"/>

Figure: Surface ordering of contronl points for bilinear face.

<img src="fig/triquad-002.png" alt="triquad-002" width="300"/>

Figure: Slice build up in x-direction, each slice is parameterized in (y, z) for a given x.  

Order | Index 
---|:---:
Major | x
Middle | y
Minor | z

<img src="fig/triquad-003.png" alt="triquad-003" width="300"/>

Figure: Control point amplification in second and third slice (first slice remains unchanged from prior figure);  x0 face shown in blue, x1 face shown in orange.  

<img src="fig/triquad-004.png" alt="triquad-004" width="500"/>

Figure: Excerpt of B-spline control points used by Hughes (see [References](#references) below). Used as inspiration for present Bezier control points. 

### Triquadratic Bezier

* Number of control nets: 1
* Number of control points per net: 27
* Triquadratic Bezier solid
* [points](../data/bezier/triquad-qtr-cyl-control-points.csv)
* [nets](../data/bezier/triquad-qtr-cyl-control-nets.csv)
* [configuration](../data/bezier/triquad-qtr-cyl-config.json)

## Results

<img src="fig/triquad-005.png" alt="triquad-005" width="300"/>

Figure: Control points.

<img src="fig/triquad-006.png" alt="triquad-006" width="300"/>

Figure: Control nets (only one net is required and thus shown).

<img src="fig/triquad-007.png" alt="triquad-007" width="300"/>

Figure: Bezier points (blue) with control points (red).

<img src="fig/triquad-008.png" alt="triquad-008" width="300"/>

Figure: Triangulated surface of six faces on Bezier solid, with Bezier solid points (blue).

<img src="fig/triquad-009.png" alt="triquad-009" width="300"/>

Figure: Bezier solid with control points (red).

<img src="fig/triquad-010.png" alt="triquad-010" width="300"/>

Figure: Bezier solid (top view) with control points (red triangles).

## References

* [Hughes 2005](https://drive.google.com/file/d/0B-0Xwqeen8ddNTNfaHVZal92Mnc/view?usp=sharing) page 4156 and Appendix.
