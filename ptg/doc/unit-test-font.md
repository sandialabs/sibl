# unit test - font

Demonstration of the Pixel To Geometry (PTG) workflow through an example of binary classification.

## Introduction

* Digital creation of modern fonts are often created from cubic Bezier curves.
* Here we use the creation of two letters ("e" and "a") to test our PTG workflow.
* This honors the "simple-to-complex" philosophy of software development, wherein components are proven viable through simple-to-understand and quick-to-run unit tests, prior to their integration into the software system.


## Objective

## Methods

* We restrict our study to two letters, "e" and "a".
  * Restriction to two known states and a test for the states composes the framework of binary classification.
  * 
  Here we use the creation of two letters ("e" and "a") to test our PTG workflow by demonstration of the following steps:
  * Create human-recognizable objects from our Bezier geometry factory,
  * Create a library composed of two [templates](definitions.md#template), which is then suitable to be used in a binary classification problem, with metrics, e.g., sensitivity and specificity, to adjudicate the quality of the decode algorithm.
  * Create an **encode** algorithm:
    * 


from [Design With FontForge](https://drive.google.com/file/d/1lT1O3lM3liIpdv74NJHczz7yXLsEY8vA/view?usp=sharing) [@FontForge2017]

![letter-e](fig/e.png)

> Figure.  The letter "e", composed of Bezier curves. @FontForge2017 from page 45.

![letter-a](fig/a.png)
> Figure.  The letter "a", composed of Bezier curves. @FontForge2017 from page 46.

![letter-g](fig/g.png)
> Figure.  The letter "g", composed of Bezier curves. @FontForge20177 from page 47.


## Results

To come.

## Discussion

To come.

## Conclusion

To come.

## References

To come.
