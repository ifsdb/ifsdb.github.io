---
name: "Pythagoras Tree"
description: "The Pythagoras tree is a fractal tree constructed by placing two scaled squares on the two legs of a right isosceles triangle on top of a base square, recursively."
cardDescription: "Two maps at ±45°, each scaling by 1/√2. A self-similar tree that perfectly tiles a bounded region of the plane."
dimension: "2"
transforms: 2
tags: [plane, self-similar, naturalistic, tiling]
aifs: |
  @
  $dim=2
  f1=[0,1]*[0.5,-0.5,0.5,0.5]
  f2=[0.5,1.5]*[0.5,0.5,-0.5,0.5]
  S=(f1|f2)*S
references:
  - text: "Pythagoras tree — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Pythagoras_tree_(fractal)"
  - text: "Mandelbrot, B. (1982). The Fractal Geometry of Nature. W. H. Freeman."
---

## Overview

The **Pythagoras tree** is a fractal named after the Pythagorean theorem.
Starting from a unit square (representing the trunk), an isosceles right triangle is placed
on the top edge, and two smaller squares are built on its two legs.
The process is repeated on each new square indefinitely.

In the symmetric variant both child squares are the same size: each has side $\frac{1}{\sqrt{2}}$
and is tilted by $\pm 45°$ relative to its parent.

## Definition

The two IFS maps both scale by $\frac{1}{\sqrt{2}}$:

$$f_1(x,y) = \frac{1}{\sqrt{2}} R_{+45°}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}0\\1\end{pmatrix} = \begin{pmatrix}\frac{x-y}{2}\\\frac{x+y}{2}+1\end{pmatrix}$$

$$f_2(x,y) = \frac{1}{\sqrt{2}} R_{-45°}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}\frac{1}{2}\\\frac{3}{2}\end{pmatrix} = \begin{pmatrix}\frac{x+y}{2}+\frac{1}{2}\\-\frac{x-y}{2}+\frac{3}{2}\end{pmatrix}$$

$f_1$ places the left child square, $f_2$ the right. Both use contraction ratio $r = \frac{1}{\sqrt{2}}$.

## Properties

- **Fractal dimension:** 2 — the attractor eventually fills a bounded planar region with positive area
- **Tiling:** The whole tree fits inside a $6 \times 4$ bounding box for the symmetric case
- **Self-similarity:** Each subtree beyond a branching point is a scaled, rotated copy of the whole tree
- **Number of transforms:** 2, both contraction ratio $\frac{1}{\sqrt{2}}$
- **Variants:** Asymmetric versions (different branch angles) produce visually distinct trees while maintaining the IFS structure
