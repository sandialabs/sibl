# Definitions

## class

* A class if the code blueprint from which conrete objects are created.

## isomorphism

* An isomophism is a mapping between two sets *{A}* and *{B}* that is one-to-one.
* From *{A}* to *{B}* is called the *forward map*.
* From *{B}* to *{A}* is called the *inverse map*.
* The mapping from *{A}* to *{B}* is reversible, such that the inverse map from *{B}* to *{A}* recovers the original *{A}* that created *{B}* in the forward map.
* It is one of the morphisms of [category theory](https://en.wikipedia.org/wiki/Category_theory)
  * It is a homomorphism that admits and inverse.
  * It is a monomorphism as it is injective (one-to-one) and surjective (onto).

## object

  * An object is an instance of a class.

## slice

  * A slice is a two-dimensional subset taken from a three-dimensional structure.  
  * A slice is composed *m* rows and *n* colunms, the major and minor axes, respectively.  
  * At each (row, column) index (i, j), with i = [0, 1, 2, ... m) and j = [0, 1, 2, ... n), there is a class integer k = [0, ... number_of_classes).

## template

  * A template is the fundamental instance of a class.
  * The template contains sufficient default *convention*, freeing the implementor from specifying a *configuration*.
  * All client class implementations are an isomophism of a class template.
  * Words with concepts similar to *template* are *atlas*, *parent*, *primitive*, *progenitor*, and *prototype*.
