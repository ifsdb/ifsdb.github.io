---
name: "Sierpiński Triangle"
description: "The Sierpiński Triangle is a self-similar fractal defined by three contraction mappings."
cardDescription: "Three contractions scaling by 1/2, producing a self-similar triangle with zero area."
dimension: "log(3)/log(2) ≈ 1.585"
transforms: 3
tags: [plane, self-similar, classic]
aifs: |
  @
  $dim=2
  f1=[0.5,0,0,0.5]
  f2=[0.5,0]*[0.5,0,0,0.5]
  f3=[0.25,0.5]*[0.5,0,0,0.5]
  S=(f1|f2|f3)*S
references:
  - text: "Sierpiński, W. (1915). \"Sur une courbe dont tout point est un point de ramification.\" Comptes Rendus, 160, 302–305."
  - text: "Sierpiński triangle — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle"
---

## Overview

The **Sierpiński Triangle** (also called the Sierpiński gasket) is one of
the most recognizable fractals in mathematics. Named after Polish mathematician
[Wacław Sierpiński](https://en.wikipedia.org/wiki/Wac%C5%82aw_Sierpi%C5%84ski),
who described it in 1915, it is constructed by recursively removing the central
triangle from an equilateral triangle.

As an IFS, the Sierpiński Triangle is the attractor of three affine contractions,
each scaling by 1/2 toward one of the three vertices of an equilateral triangle.

## Definition

The Sierpiński Triangle is the attractor of three affine maps (each a scaling by 1/2):

### Transformation 1 — Bottom-left vertex

$$f_1(x,y) = \begin{pmatrix}0.5 & 0\\0 & 0.5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}$$

### Transformation 2 — Bottom-right vertex

$$f_2(x,y) = \begin{pmatrix}0.5 & 0\\0 & 0.5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0.5\\0\end{pmatrix}$$

### Transformation 3 — Top vertex

$$f_3(x,y) = \begin{pmatrix}0.5 & 0\\0 & 0.5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0.25\\0.5\end{pmatrix}$$

## Properties

The Hausdorff dimension is:

$$d = \frac{\log 3}{\log 2} \approx 1.585$$

- **Self-similarity:** Each of the three sub-triangles is an exact scaled copy of the whole
- **Number of transformations:** 3, each with contractivity ratio 1/2
- **Area:** Zero (the attractor has Lebesgue measure zero)
- **Boundary:** Every point of the attractor is a boundary point
