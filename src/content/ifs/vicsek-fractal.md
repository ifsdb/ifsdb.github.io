---
name: "Vicsek Fractal"
description: "The Vicsek fractal is a self-similar plane fractal built from five copies of itself arranged in a cross pattern, one at each corner and one at the centre."
cardDescription: "Five maps in a cross arrangement — four corners plus centre. Related to critical percolation clusters."
dimension: "≈ 1.465"
transforms: 5
tags: [plane, self-similar, classic]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.333,0,0,0.333]
  f2=[0.667,0]*[0.333,0,0,0.333]
  f3=[0.333,0.333]*[0.333,0,0,0.333]
  f4=[0,0.667]*[0.333,0,0,0.333]
  f5=[0.667,0.667]*[0.333,0,0,0.333]
  S=(f1|f2|f3|f4|f5)*S
references:
  - text: "Vicsek, T. (1983). Fractal models for diffusion controlled aggregation. J. Phys. A: Math. Gen."
  - text: "Vicsek fractal — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Vicsek_fractal"
---

## Overview

The **Vicsek fractal** (also called the *box fractal*) was introduced by Tamás Vicsek in 1983
in the context of diffusion-limited aggregation. Starting from a 3×3 grid, keep the four corner
squares and the central square, then recurse. The resulting pattern resembles a cross at every scale.

## Construction

At each step, subdivide the square into a 3×3 grid and keep only the five marked cells:

```
X . X
. X .
X . X
```

Repeat for each retained sub-square. The attractor is the intersection of all iterations.

## Definition

Five affine maps, each scaling by $\frac{1}{3}$ and translating to one of the five retained positions:

$$f_k(x, y) = \frac{1}{3}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}t_x^{(k)} \\ t_y^{(k)}\end{pmatrix}$$

with translations $(0,0)$, $(\frac{2}{3}, 0)$, $(\frac{1}{3}, \frac{1}{3})$, $(0, \frac{2}{3})$, $(\frac{2}{3}, \frac{2}{3})$.

## Properties

- **Fractal dimension:** $\frac{\log 5}{\log 3} \approx 1.465$
- **Lebesgue measure:** 0
- **Number of transforms:** 5, all contraction ratio $\frac{1}{3}$
- **Lattice symmetry:** The fractal has the same 4-fold symmetry as the square lattice
