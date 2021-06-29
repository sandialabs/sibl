# unit test PTM

![ptm_ptg_workflow.png](fig/ptm_ptg_workflow.png)
> *PTM/PTG workflow*

## pixel sea (stacked layers)

![ptm-001-image.png](fig/ptm-001-image.png)
> *DICOM*

## masks (stacked layers)

![ptm-003-prediction.png](fig/ptm-003-prediction.png)
> *Deep Learning U-Net*

![thresholding_tib_fib.png](fig/thresholding_tib_fib.png)
> *Thresholding example, tibia and fibula.*

## halos (outer and inner curvature)

### Active Contour Model ("snakes") 
![snakes_baseline_smoothings_0.png](fig/snakes_baseline_smoothings_0.png)
![snakes_baseline_astro.png](fig/snakes_baseline_astro.png)

> [*Active Contour Model ("snakes")*](https://scikit-image.org/docs/dev/auto_examples/edges/plot_active_contours.html)

## Axial section template 

*via quadrant bisection and recursion*

![bilinear-five-patch.png](fig/bilinear-five-patch.png) 
> *Linear patches with curvature transition*

![biquadratic-five-patch.png](fig/biquadratic-five-patch.png)
> *Bisection and quadratic pathes with curvature transition*

![B(p=2)_1_2.png](fig/B(p=2)_1_2.png)
> *Bézier biquadratic basis used for boundary fitting*

![Livesu_2021_scaled_jacobian_valence.png](fig/Livesu_2021_scaled_jacobian_valence.png)
> [*Livesu 2021: Optimal Dual Schemes for Adaptive Grid Based Hexmeshing*](https://arxiv.org/pdf/2103.07745.pdf)

## Curvature Mapping

![bspline_surface_biquad2tri_animation_opt.gif](fig/bspline_surface_biquad2tri_animation_opt.gif)

![bspline_surface_cyl2sphere_animation_opt.gif](fig/bspline_surface_cyl2sphere_animation_opt.gif)

## Hex Mesh End Cap

![Corman_and_Crane_symmetric_moving_frames.png](fig/Corman_and_Crane_symmetric_moving_frames.png)
> [*Corman and Crane 2019: Symmetric Moving Frames*](https://dl.acm.org/doi/pdf/10.1145/3306346.3323029?casa_token=IqE4i_eSg1wAAAAA:7cSfPqjfz4-0LW9cvNRzmoQg_pjA8kslU2gVS-Tjo2vA1xl1504nky4ktFRqFWr-eQZVNMT2Dyds)

![MFEM](fig/mfem_llnl.png)
> [*MFEM LLNL*](https://computing.llnl.gov/projects/mfem-scalable-finite-element-discretization-library)

## Skeletonize, Stack, Mesh

`pixels -> trisurface`

![Livesu_2017_skeleton.png](fig/Livesu_2017_skeleton.png)

![Livesu_2017_skeleton_bifurcation.png](fig/Livesu_2017_skeleton_bifurcation.png)

![Livesu_2017_skeleton_mesh.png](fig/Livesu_2017_skeleton_mesh.png)

> [*Livesu 2017: Explicit Cylindrical Maps for General Tubular Shapes*](https://doi.org/10.1016/j.cad.2017.05.002)

## *Alternative*

![Livesu_2021_adaptive_grid_hex.png](fig/Livesu_2021_adaptive_grid_hex.png)
> [*Livesu 2021: Optimal Dual Schemes for Adaptive Grid Based Hexmeshing*](https://arxiv.org/pdf/2103.07745.pdf)
