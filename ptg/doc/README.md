# doc

## Introduction

Pixel To Geometry (PTG) is the process of using stacked 2D image data, composed of pixels, to reconstruct a 3D solid.  PTG describes a **decoding** process of a physical system that was original **encoded** into a series of 2D medical images.  

## Questions

* H0: Segmentation based on threshold pixel intensity (quantisation) is sufficient to classify bone versus non-bone in the IRCAD data set based on ground truth F1-score.

## Road map

* Encode/Decode [unit test font](unit-test-font.md)
* Encode/Decode [unit test](unit-test.md)
* Encode/Decode [unit test femur](unit-test-femur.md)
* Encode/Decode femur, patella, tibia, fibula
* Encode/Decode human skeleton

## Design

* Object-oriented programming (OOP) as a default, functional programming (FP) where appropriate.
* [PEP 8](https://www.python.org/dev/peps/pep-0008/) via [Black](https://github.com/psf/black)

## References

* [Brain oriented programming](https://tobeva.com/articles/brain-oriented-programming/) limit classes to seven attributes.
* [Black](https://youtu.be/esZLCuWs_2Y) by Łukasz Langa - Life Is Better Painted Black, or: How to Stop Worrying and Embrace Auto-Formatting
* [Definitions](definitions.md)
