# Step 0: Getting Started with CinoLib

## Overview

The **goal** of this document is to record the steps required to get [CinoLib](https://github.com/mlivesu/cinolib), created by Livesu and contributors, installed and running as a **local user workflow** to produce a hexahedral mesh from a surface representation.

The specific example will be the duck model shown in the figure below (originally created in, and reproduced from [Livesu 2021b](references.md#livesu-2021b)).

![duck](fig/Livesu_2021_dual_fig_1.png)
> *Figure 0.1:  Reproduction from Fig. 1 of [Livesu 2021b](references.md#livesu-2021b).*

Next:  [Step 1](step_01.md)


[References](references.md)

Notes:

* 2022-01-17, Livesu committed major update that removes cinolib dependency on Qt. 
  * `cmake` is used as the build system.
  * GLFW and ImGui handle the GUI.

