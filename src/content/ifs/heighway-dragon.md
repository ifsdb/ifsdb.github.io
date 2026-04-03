---
name: "Heighway Dragon"
description: "The Heighway dragon is a fractal curve obtained by repeatedly folding a strip of paper in half and unfolding it at right angles."
cardDescription: "Two maps each rotating by 45° or −135°, producing a dragon-shaped curve that tiles the plane in groups of four."
dimension: "2"
transforms: 2
tags: [plane, curve, tiling, classic]
aifs: |
  @
  $dim=2
  f1=[0,0]*[0.5,-0.5,0.5,0.5]
  f2=[1,0]*[-0.5,-0.5,0.5,-0.5]
  S=(f1|f2)*S
references:
  - text: "Heighway, J. (1966). Dragon curve. Recreational Mathematics Magazine."
  - text: "Davis, C., Knuth, D. E. (1970). Number representations and dragon curves. J. Recreational Mathematics."
  - text: "Dragon curve — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Dragon_curve"
---

## Overview

The **Heighway dragon curve** was first investigated by NASA physicist John Heighway and
later popularised by Martin Gardner and Donald Knuth. It is most famously associated with the
*paper folding sequence*: repeatedly fold a strip of paper in half in the same direction, then
unfold each crease to a right angle. After infinitely many folds, the result is the dragon curve.

## Definition

Two affine maps, both scaling by $\frac{1}{\sqrt{2}}$, with rotations of $+45°$ and $-135°$:

$$f_1(x,y) = \begin{pmatrix}\frac{x-y}{2} \\ \frac{x+y}{2}\end{pmatrix}$$

$$f_2(x,y) = \begin{pmatrix}-\frac{x+y}{2} + 1 \\ \frac{x-y}{2}\end{pmatrix}$$

Both maps share the common image point $f_1(1,0) = f_2(1,0) = (\frac{1}{2}, \frac{1}{2})$.

## Properties

- **Fractal dimension:** 2 (the attractor fills a region of the plane)
- **Tiling:** Four copies of the dragon tile the plane
- **Number of transforms:** 2, both contraction ratio $\frac{1}{\sqrt{2}}$
- **Paper folding:** The $n$-th iteration corresponds to $n$ folds of a paper strip

## Paper Folding Connection

The sequence of fold directions when unfolding (R = right, L = left) follows the recurrence:

$$a_{2^k(2m+1)} = \begin{cases} R & \text{if } k \text{ is even} \\ L & \text{if } k \text{ is odd} \end{cases}$$

This *regular paper folding sequence* encodes the entire structure of the dragon curve.
