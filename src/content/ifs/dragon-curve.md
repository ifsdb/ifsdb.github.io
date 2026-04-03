---
name: "Dragon Curve"
description: "The Dragon Curve is a space-filling fractal arising from two rotational contraction mappings."
cardDescription: "Two rotational contractions at ±45° producing a non-self-intersecting curve that tiles the plane."
dimension: "≈ 1.5236"
transforms: 2
tags: [plane, tiling, curve]
aifs: |
  @
  $dim=2
  f1=[0.5,-0.5,0.5,0.5]
  f2=[1,0]*[-0.5,0.5,-0.5,-0.5]
  S=(f1|f2)*S
references:
  - text: "Gardner, M. (1967). \"Mathematical Games.\" Scientific American, 216(3), 124–125."
  - text: "Dragon curve — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Dragon_curve"
---

## Overview

The **Dragon Curve** (also called the Heighway Dragon, after NASA physicist
John Heighway who first studied it in the 1960s) is a self-similar fractal that can be
constructed by repeatedly folding a strip of paper in half and unfolding it so each fold
is at a right angle.

As an IFS, the Dragon Curve is the attractor of two affine contractions, each a rotation
by ±45° combined with a scaling by 1/√2. The resulting curve is continuous, non-self-intersecting,
and tiles the plane.

## Definition

The Dragon Curve is the attractor of two rotational contractions:

### Transformation 1 — Rotation by +45°, scale 1/√2

$$f_1(x,y) = \frac{1}{\sqrt{2}}\begin{pmatrix}\cos 45^\circ & -\sin 45^\circ\\ \sin 45^\circ & \cos 45^\circ\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} = \begin{pmatrix}0.5 & -0.5\\0.5 & 0.5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}$$

### Transformation 2 — Rotation by +135°, scale 1/√2, translate (1,0)

$$f_2(x,y) = \frac{1}{\sqrt{2}}\begin{pmatrix}\cos 135^\circ & -\sin 135^\circ\\ \sin 135^\circ & \cos 135^\circ\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}1\\0\end{pmatrix} = \begin{pmatrix}-0.5 & 0.5\\-0.5 & -0.5\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix} + \begin{pmatrix}1\\0\end{pmatrix}$$

## Properties

The Hausdorff dimension is:

$$d \approx 1.5236$$

- **Contractivity ratio:** 1/√2 for both mappings
- **Number of transformations:** 2
- **Tiling:** Four Dragon Curves together tile the plane
- **Boundary:** The curve is nowhere differentiable
- **Constructed by:** John Heighway, NASA (1960s); popularized by Martin Gardner
