---
name: "Barnsley Fern"
description: "The Barnsley Fern is a fractal named after mathematician Michael Barnsley, defined by four affine transformations."
cardDescription: "Four affine maps producing a naturalistic fern shape. A classic example of biological structure from simple rules."
dimension: "≈ 1.6667"
transforms: 4
tags: [plane, probabilistic, naturalistic]
aifs: |
  @
  $dim=2
  f1=[0,0,0,0.16]
  f2=[0,1.6]*[0.85,0.04,-0.04,0.85]
  f3=[0,1.6]*[0.2,-0.26,0.23,0.22]
  f4=[0,0.44]*[-0.15,0.28,0.26,0.24]
  S=(f1|f2|f3|f4)*S
references:
  - text: "Barnsley, M. (1988). Fractals Everywhere. Academic Press."
  - text: "Barnsley fern — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Barnsley_fern"
---

## Overview

The **Barnsley Fern** is a fractal named after British mathematician
[Michael Barnsley](https://en.wikipedia.org/wiki/Michael_Barnsley).
It is a classic example of an IFS attractor that closely resembles a natural
black spleenwort fern (*Asplenium adiantum-nigrum*). The fern demonstrates how
biological shapes can emerge from simple mathematical rules.

Barnsley first described this IFS in his 1988 book *Fractals Everywhere*.
The four affine transformations are chosen so that one maps the entire fern to
its stem, one to the successively smaller leaflets, and two to the bottom left
and right fronds.

## Definition

The Barnsley Fern is defined by four affine transformations applied with given probabilities:

### Transformation 1 — Stem

$$f_1(x,y) = \begin{pmatrix}0 & 0\\0 & 0.16\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}, \quad p_1 = 0.01$$

### Transformation 2 — Successively smaller leaflets

$$f_2(x,y) = \begin{pmatrix}0.85 & 0.04\\-0.04 & 0.85\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0\\1.6\end{pmatrix}, \quad p_2 = 0.85$$

### Transformation 3 — Left frond

$$f_3(x,y) = \begin{pmatrix}0.2 & -0.26\\0.23 & 0.22\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0\\1.6\end{pmatrix}, \quad p_3 = 0.07$$

### Transformation 4 — Right frond

$$f_4(x,y) = \begin{pmatrix}-0.15 & 0.28\\0.26 & 0.24\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0\\0.44\end{pmatrix}, \quad p_4 = 0.07$$

## Properties

- **Fractal dimension:** ≈ 1.6667 (Hausdorff dimension)
- **Self-similarity:** Each frond is a scaled and rotated copy of the whole fern
- **Number of transformations:** 4
- **Random iteration:** The chaos game algorithm samples this attractor with probabilities p₁=0.01, p₂=0.85, p₃=0.07, p₄=0.07
