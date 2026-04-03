---
name: "Sierpiński Carpet"
description: "The Sierpiński Carpet is a plane fractal defined by subdividing a square into 9 equal parts and recursively removing the central square."
cardDescription: "Eight affine maps tiling a square minus its centre. A 2D analogue of the Cantor set and Sierpiński triangle."
dimension: "≈ 1.893"
transforms: 8
tags: [plane, self-similar, classic]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.333,0,0,0.333]
  f2=[0.333,0]*[0.333,0,0,0.333]
  f3=[0.667,0]*[0.333,0,0,0.333]
  f4=[0,0.333]*[0.333,0,0,0.333]
  f5=[0.667,0.333]*[0.333,0,0,0.333]
  f6=[0,0.667]*[0.333,0,0,0.333]
  f7=[0.333,0.667]*[0.333,0,0,0.333]
  f8=[0.667,0.667]*[0.333,0,0,0.333]
  S=(f1|f2|f3|f4|f5|f6|f7|f8)*S
references:
  - text: "Sierpiński, W. (1916). Sur une courbe cantorienne qui contient une image biunivoque et continue de toute courbe donnée. C. R. Acad. Sci. Paris."
  - text: "Sierpiński carpet — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Sierpi%C5%84ski_carpet"
---

## Overview

The **Sierpiński Carpet** is a self-similar plane fractal first described by Wacław Sierpiński in 1916.
It is constructed by repeatedly subdividing a square into a 3×3 grid of nine equal sub-squares
and removing the central one, then repeating the process for each remaining sub-square.

The carpet is a two-dimensional analogue of the Cantor set and can be seen as a "thickened" version
of the Sierpiński triangle.

## Construction

At each iteration, divide the current square into a 3×3 grid and delete the centre cell.
After $n$ steps, $8^n$ sub-squares of side length $3^{-n}$ remain.

The attractor is the limit $S = \lim_{n\to\infty} S_n$ and is defined exactly by the eight IFS maps.

## Definition

Each of the eight affine maps scales by $\frac{1}{3}$ and translates to one of the eight non-central positions:

$$f_k(x, y) = \frac{1}{3}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}t_x^{(k)} \\ t_y^{(k)}\end{pmatrix}$$

where $(t_x, t_y)$ ranges over $\{0, \frac{1}{3}, \frac{2}{3}\}^2$ excluding $(\frac{1}{3}, \frac{1}{3})$.

## Properties

- **Fractal dimension:** $\frac{\log 8}{\log 3} \approx 1.893$
- **Lebesgue measure:** 0 (the set has zero area)
- **Topological dimension:** 1 (the carpet is a universal curve — every compact, locally connected, one-dimensional metric space is homeomorphic to a subset of it)
- **Number of transforms:** 8, all contraction ratio $\frac{1}{3}$
