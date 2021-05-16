# unit test - femur

## Title

Geometry workflow to enable patient-specific analysis from medical image data.

## Introduction

## Motivation

* Femoral fracture, 18-yo male, high-speed motor vehicle crash, case rID = 48399.  [Case](https://radiopaedia.org/cases/48399/play?lang=us)
* Winquist 1980.  Classification of femoral shaft fractures [Case](https://radiopaedia.org/articles/winquist-classification-of-femoral-shaft-fractures-1?lang=us)

## Objective

Demonstrate the Pixel To Geometry (PTG) workflow through 3D reconstruction of the right, normal human femur, AM50. 

## Review

* numpy-stl on [pypi](https://pypi.org/project/numpy-stl/) and on [GitHub](https://github.com/WoLpH/numpy-stl).
* Remacle JF, Geuzaine C, Compere G, Marchandise E. High‐quality surface remeshing using harmonic maps. International Journal for Numerical Methods in Engineering. 2010 Jul 23;83(4):403-25. [link](https://www.gmsh.info/doc/preprints/gmsh_stl_preprint.pdf)
* Marchandise E, de Wiart CC, Vos WG, Geuzaine C, Remacle JF. High‐quality surface remeshing using harmonic maps—Part II: Surfaces with high genus and of large aspect ratio. International Journal for Numerical Methods in Engineering. 2011 Jun 17;86(11):1303-21. [link](https://gmsh.info/doc/preprints/gmsh_stl2_preprint.pdf)
* Geuzaine C, Remacle JF. Gmsh: A 3‐D finite element mesh generator with built‐in pre‐and post‐processing facilities. International journal for numerical methods in engineering. 2009 Sep 10;79(11):1309-31. [link](https://gmsh.info/doc/preprints/gmsh_paper_preprint.pdf)
* Martin T, Cohen E, Kirby RM. Volumetric parameterization and trivariate B-spline fitting using harmonic functions. Computer aided geometric design. 2009 Aug 1;26(6):648-64.  [link](https://people.eecs.berkeley.edu/~sequin/CS284/PAPERS/Bspline_Volume_Meshing.pdf)
* Gu X, Wang Y, Chan TF, Thompson PM, Yau ST. Genus zero surface conformal mapping and its application to brain surface mapping. IEEE transactions on medical imaging. 2004 Aug 2;23(8):949-58. [link](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.5.1392&rep=rep1&type=pdf)
* Chuang JH, Ahuja N, Lin CC, Tsai CH, Chen CH. A potential-based generalized cylinder representation. Computers & Graphics. 2004 Dec 1;28(6):907-18. [link](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.390.1416&rep=rep1&type=pdf)
* Zhang Y, Bajaj C, Sohn BS. 3D finite element meshing from imaging data. Computer methods in applied mechanics and engineering. 2005 Nov 15;194(48-49):5083-106. [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2748876/)
* Zhang, Computational Bio-Modeling Lab in Carnegie Mellon University (CMU-CBML) [GitHub](https://github.com/CMU-CBML).
* Yu Y, Wei X, Li A, Liu JG, He J, Zhang YJ. HexGen and Hex2Spline: Polycube-based Hexahedral Mesh Generation and Spline Modeling for Isogeometric Analysis Applications in LS-DYNA. arXiv preprint arXiv:2011.14213. 2020 Nov 28. [link](https://arxiv.org/pdf/2011.14213.pdf)  Submitted to Springer INdAM Series, 2020.
* Goncalves, Paulo.  [GMSH, MeshLab, Calculix - Frequency Analysis of Human Femur](https://youtu.be/4BbDXylSua0)

## Data States

* human subject
* DICOM
* volume segmentation of part (e.g., 3D femur)
* surface triangular mesh (skin) of a volume segmentation
* surface segmentation via centroidal Voronoi tessellation (CVT)
* polycube volume
* hex volume mesh (control mesh)
* spline volume mesh

## Functional Workflow: `Function: Input -> Output`

| scan | | |
|--|--|--|
| function | input | output |
| *scan* | human subject | `DICOM( array( int[0, 1] ) )`

| image process | | |
|--|--|--|
| function | input | output |
| `image_process` </br> `.denoise \|` </br> `.defleck \|` </br> `.deisland \|` | `DICOM` | `ImageStack( array(Image) )` </br> `Image( matrix(Intensity) )` </br> `Intensity( int[0, 256) )` | 
|  *segment* | `ImageStack` | `SegmentedStack( array(Mask) )` |
| *unknown* | `DICOM` | `Isosurface( STL )` |

| Primitive |
|--|
| `Point3D( tuple(float, float, float) )` |
| `Con3( tuple(int, int, int) )` | 
| `Con4( tuple(int, int, int, int) )` |
| `Con8( tuple(int0, int1, ..., int7) )` |
| `Con10( tuple(int0, int1, ..., int9) )` |
| `Mask( matrix( int[0, 1] ) )` |

| Curve | | |
|--|--|--|
| function | input | output |
| `skeletonize` | in | out |

| Surface | | |
|--|--|--|
| function | input | output |
|  `isosurface` </br> `.MarchingCubes \|` </br> `.SurfaceNets \| ` </br> `.DualContouring \|`| in | out |
|  `contour_spectrum` | `SegmentedStack` | `(outer: Isosurface, inner: Isosurface)` |
| `triangularize` | `SegmentedStack` | `STL( array(Point3D), array(Con3) )` 

| Volume | | |
|--|--|--|
| function | input | output |
| `tetrahedralize` </br> `.tet4 \|` </br> `.tet10 \|` | `SegmentedStack` | `Tet4Mesh( array(Point3D), array(Con4) )` </br> `Tet10Mesh( array(Point3D), array(Con10) )`
| `hexahedralize` </br> `.hex8 \|` | `SegmentedStack` | `Hex8Mesh( array(Point3D), array(Con8) )` |
| `voxelize` | `SegmentedStack` | EulerianDomain3D (aka "SugarCubes") |
| `BSplineTrivariate` | xx | xx |

## Data

* Bauer, Eric.  [Human femur](https://sketchfab.com/3d-models/human-femur-a9c1f1a88b104c3fbfe975fa10b31b31) available in three formats, Stereolithography (stl), Generated GLTF (gltf), Generated USDZ (usdz), 165 MB, 3.5M triangles, 1.7M vertices, materials 1, ["Human Femur"](https://skfb.ly/6ursH) by Eric Bauer is licensed under [Creative Commons Attribution](http://creativecommons.org/licenses/by/4.0/), 10 Nov 2019.  [Elon University](https://www.elon.edu/u/directory/profile/?user=ebauer).
* Soodmand 2018.  (Correspondence: ehsan.soodmand@gmail.com, Biomechanics and Implant Technology Research Laboratory, Department of Orthopaedics, University Medicine Rostock, Doberaner Strasse 142, 18057 Rostock, Germany, https://forbiomit.med.uni-rostock.de/en/about-us/staff)
  * Soodmand E, Kluess D, Varady PA, Cichon R, Schwarze M, Gehweiler D, Niemeyer F, Pahr D, Woiczinski M. Interlaboratory comparison of femur surface reconstruction from CT data compared to reference optical 3D scan. Biomedical engineering online. 2018 Dec;17(1):1-0.
  * [Link](https://biomedical-engineering-online.biomedcentral.com/articles/10.1186/s12938-018-0461-0)

## Methods

## Results

## Discussion

## Conclusion

## Appendix

## References

* Digital Morphology [Digimorph](http://www.digimorph.org/)
* [OsiriX DICOM Viewer](https://www.osirix-viewer.com/)
* [OsiriX Foundation](https://www.osirixfoundation.com/)
* [OsiriX Open Source](https://github.com/pixmeo/osirix)
* [Slicer](https://github.com/Slicer)
* SlicerMorph [GitHub](https://github.com/SlicerMorph/) and [website](https://slicermorph.github.io/)

### Unit Tests

The client driver file, [pixel_to_mesh_example.py](../examples/pixel_to_mesh_example.py), created the following pixel shapes:

* <img src="fig/qtr_cyl_ir3_or6_pixperlen1.png" alt="qtr_cyl_ir3_or6_pixperlen1" width="320"/>
* > [Figure](fig/qtr_cyl_ir3_or6_pixperlen1.png): Quarter cylinder, H=1 len, IR=3 len, OR=6 len, pix/len = 1.

* <img src="fig/qtr_cyl_ir3_or6_pixperlen2.png" alt="qtr_cyl_ir3_or6_pixperlen2" width="320"/>
* > [Figure](fig/qtr_cyl_ir3_or6_pixperlen2.png): Quarter cylinder, H=1 len, IR=3 len, OR=6 len, pix/len = 2.

* <img src="fig/qtr_cyl_ir3_or6_pixperlen3.png" alt="qtr_cyl_ir3_or6_pixperlen3" width="320"/>
* > [Figure](fig/qtr_cyl_ir3_or6_pixperlen3.png): Quarter cylinder, H=1 len, IR=3 len, OR=6 len, pix/len = 3.

* <img src="fig/cyl_ir3_or6_pixperlen1.png" alt="cyl_ir3_or6_pixperlen1" width="320"/>
* > [Figure](fig/cyl_ir3_or6_pixperlen1.png): Cylinder, H=1 len, ID=6 len, OD=12 len, pix/len = 1.

* <img src="fig/cyl_ir3_or6_pixperlen2.png" alt="cyl_ir3_or6_pixperlen2" width="320"/>
* > [Figure](fig/cyl_ir3_or6_pixperlen2.png): Cylinder, H=1 len, ID=6 len, OD=12 len, pix/len = 2.

* <img src="fig/cyl_ir3_or6_pixperlen3.png" alt="cyl_ir3_or6_pixperlen3" width="320"/>
* > [Figure](fig/cyl_ir3_or6_pixperlen3.png): Cylinder, H=1 len, ID=6 len, OD=12 len, pix/len = 3.
