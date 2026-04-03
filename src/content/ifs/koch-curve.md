---
name: "Koch Curve"
description: "The Koch curve is a fractal defined by replacing the middle third of each line segment with two sides of an equilateral triangle, repeated infinitely."
cardDescription: "Four affine maps producing a snowflake-like curve with infinite perimeter and finite area."
dimension: "≈ 1.261"
transforms: 4
tags: [plane, self-similar, curve, classic]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.333,0,0,0.333]
  f2=[0.333,0]*[0.167,-0.289,0.289,0.167]
  f3=[0.5,0.289]*[0.167,0.289,-0.289,0.167]
  f4=[0.667,0]*[0.333,0,0,0.333]
  S=(f1|f2|f3|f4)*S
references:
  - text: "Koch, H. von (1904). Sur une courbe continue sans tangente. Arkiv för Matematik."
  - text: "Koch snowflake — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Koch_snowflake"
---

## Overview

The **Koch curve** was introduced by Swedish mathematician Helge von Koch in 1904 as an example of a
continuous curve that is nowhere differentiable. The familiar **Koch snowflake** is obtained by
applying the construction to all three sides of an equilateral triangle.

## Construction

Starting from a unit line segment, at each step replace the middle third with two sides of an
equilateral triangle (pointing outward), removing the base:

$$\text{segment} \;\longrightarrow\; \text{four segments of length } \tfrac{1}{3}$$

After $n$ steps the curve has $4^n$ segments each of length $(\frac{1}{3})^n$,
so the total length grows as $(\frac{4}{3})^n \to \infty$.

## Definition

The four IFS maps all scale by $\frac{1}{3}$. Maps 2 and 3 additionally rotate by $\pm 60°$:

$$f_1(x,y) = \frac{1}{3}\begin{pmatrix}x \\ y\end{pmatrix}$$

$$f_2(x,y) = \frac{1}{3}\begin{pmatrix}\cos 60° & -\sin 60° \\ \sin 60° & \cos 60°\end{pmatrix}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}1/3 \\ 0\end{pmatrix}$$

$$f_3(x,y) = \frac{1}{3}\begin{pmatrix}\cos(-60°) & -\sin(-60°) \\ \sin(-60°) & \cos(-60°)\end{pmatrix}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}1/2 \\ \sqrt{3}/6\end{pmatrix}$$

$$f_4(x,y) = \frac{1}{3}\begin{pmatrix}x \\ y\end{pmatrix} + \begin{pmatrix}2/3 \\ 0\end{pmatrix}$$

## Properties

- **Fractal dimension:** $\frac{\log 4}{\log 3} \approx 1.261$
- **Perimeter:** Infinite
- **Number of transforms:** 4, all contraction ratio $\frac{1}{3}$
- **Self-similarity:** Each quarter of the curve is a scaled, rotated copy of the whole
