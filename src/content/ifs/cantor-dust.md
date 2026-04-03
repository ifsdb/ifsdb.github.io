---
name: "Cantor Dust"
description: "Cantor dust is the two-dimensional analogue of the Cantor set, constructed by taking the Cartesian product of two Cantor sets."
cardDescription: "Four corner maps each scaling by 1/3. The 2D product of two Cantor sets — an uncountable set of isolated points with zero area."
dimension: "≈ 1.261"
transforms: 4
tags: [plane, self-similar, classic]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.333,0,0,0.333]
  f2=[0.667,0]*[0.333,0,0,0.333]
  f3=[0,0.667]*[0.333,0,0,0.333]
  f4=[0.667,0.667]*[0.333,0,0,0.333]
  S=(f1|f2|f3|f4)*S
references:
  - text: "Cantor, G. (1883). Über unendliche, lineare Punktmannichfaltigkeiten. Math. Annalen."
  - text: "Cantor set — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Cantor_set"
---

## Overview

**Cantor dust** is the two-dimensional generalisation of the classical Cantor set.
It is constructed as the Cartesian product $C \times C$ of the Cantor set with itself —
equivalently, by taking a unit square and at each iteration removing the central cross
$(\frac{1}{3}, \frac{2}{3}) \times [0,1]$ together with $[0,1] \times (\frac{1}{3}, \frac{2}{3})$.

The result is a totally disconnected perfect set: every point is a limit point, yet
no two points are connected.

## Construction

At step $n$ retain only the $4^n$ squares of side length $3^{-n}$ located in the four
corners of the $3^n \times 3^n$ grid. In the limit a self-similar dust remains.

Each of the four IFS maps scales by $\frac{1}{3}$ and translates to a corner of $[0,1]^2$:

$$f_k(x, y) = \frac{1}{3}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}t_x^{(k)} \\ t_y^{(k)}\end{pmatrix}$$

with translations $(0,0)$, $(\frac{2}{3}, 0)$, $(0, \frac{2}{3})$, $(\frac{2}{3}, \frac{2}{3})$.

## Properties

- **Fractal dimension:** $\frac{\log 4}{\log 3} \approx 1.261$
- **Lebesgue measure:** 0 (the dust has zero area)
- **Topological dimension:** 0 (totally disconnected)
- **Cardinality:** Uncountably infinite
- **Self-similarity:** Each quadrant of the dust is an exact $\frac{1}{3}$-scaled copy of the whole

## Relation to the Cantor Set

The 1D Cantor set $C \subset [0,1]$ is the attractor of the two maps
$g_1(x) = \frac{x}{3}$ and $g_2(x) = \frac{x}{3} + \frac{2}{3}$.
Cantor dust is $C \times C$, and the four 2D maps are exactly all combinations of $g_1, g_2$
applied independently to each coordinate.

Its Hausdorff dimension equals $2 \times \dim_H(C) = 2 \times \frac{\log 2}{\log 3} = \frac{\log 4}{\log 3}$.
