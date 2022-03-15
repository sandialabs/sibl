# Chronology

## 2022-01-18-0221

This is a nice coincidence. Just yesterday [2022-01-17] I committed a major update to cinolib which completely removes the dependency from Qt. In the current version cmake is used as a building system, and the GUI is in the hands of GLFW and ImGui. It should work just out of the box, give it a try and let me know if you have any issue with the new version.

BTW: the comment you have at the end of https://github.com/sandialabs/sibl/blob/master/geo/doc/cinolib.md about figure 5 is correct. It was a typo and has been corrected in the TOG version of the paper. The arxiv version is actually old, I suggest you take a look at this one http://pers.ge.imati.cnr.it/livesu/papers/LPC21/LPC21.pdf, there are a few more experiments and novel insight on the previous techniques.

Last year we made two TOG papers on grid-based hexmeshing. Part of the code necessary to build the example you mention is still outside of cinolib, and can be found in this repository: https://github.com/cg3hci/Gen-Adapt-Ref-for-Hexmeshing. Specifically, this repository contains the code necessary to create an adaptive grid with hanging nodes and to enforce balancing and pairing, whereas the schemes to suppress hanging nodes are already inside the library. Eventually everything will be refactored and the whole hexmeshing pipeline will be moved inside cinolib. This is work in progress.

> I would memorialize these steps in a “Getting Started” markdown report, and submit it to your GitHub repository so that others around the world could learn the steps too.

That could be useful, thanks! Even though things may change over time as I mentioned above. The ultimate goal  is to be able to execute the whole pipeline with a single cinolib call, and then expose it to the public :)

BTW, at this link there is an online demo based on our code that you can use to produce hexmeshes http://90.147.146.248/

> Also, I would be very interested in trying to wrap your C++ library for Python users!

This could be really interesting as well. Let's talk about it :)

## 2022-01-17

* Livesu committed major update that removes cinolib dependency on Qt. 
  * `cmake` is used as the build system.
  * GLFW and ImGui handle the GUI.

