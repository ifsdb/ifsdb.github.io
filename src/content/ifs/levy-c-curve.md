---
name: "Lévy C Curve"
description: "The Lévy C curve is a self-similar fractal defined by two affine maps that each scale by 1/√2 and rotate by ±45°."
cardDescription: "Two maps, each a 45° rotation scaled by 1/√2. The attractor tiles the plane and resembles the letter C at each scale."
dimension: "2"
transforms: 2
tags: [plane, curve, self-similar, tiling]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.5,-0.5,0.5,0.5]
  f2=[0.5,0.5]*[0.5,0.5,-0.5,0.5]
  S=(f1|f2)*S
references:
  - text: "Lévy, P. (1938). Les courbes planes ou gauches et les surfaces composées de parties semblables au tout. J. École Polytechnique."
  - text: "Lévy C curve — Wikipedia"
    url: "https://en.wikipedia.org/wiki/L%C3%A9vy_C_curve"
---

## Overview

The **Lévy C curve** (also called the Lévy dragon) was studied by French mathematician Paul Lévy
in 1938. It is a self-similar curve with the remarkable property that multiple copies of itself
tile the plane without overlap. Its name comes from its resemblance to the letter *C* at every
level of magnification.

## Definition

Two affine maps, each a rotation by ±45° combined with a scale factor of $\frac{1}{\sqrt{2}}$:

$$f_1(x, y) = \frac{1}{\sqrt{2}} R_{+45°} \begin{pmatrix}x \\ y\end{pmatrix} = \begin{pmatrix}\frac{x-y}{2} \\ \frac{x+y}{2}\end{pmatrix}$$

$$f_2(x, y) = \frac{1}{\sqrt{2}} R_{-45°} \begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}\frac{1}{2} \\ \frac{1}{2}\end{pmatrix} = \begin{pmatrix}\frac{x+y}{2} + \frac{1}{2} \\ \frac{-x+y}{2} + \frac{1}{2}\end{pmatrix}$$

Both maps have contraction ratio $r = \frac{1}{\sqrt{2}}$.

## Properties

- **Fractal dimension:** $\frac{\log 2}{\log \sqrt{2}} = 2$ (the attractor has positive area)
- **Tiling:** Four copies of the curve tile a square
- **Number of transforms:** 2
- **Self-similarity:** Each half of the curve is a scaled rotated copy of the whole
