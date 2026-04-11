# IFS Encyclopedia — Copilot Instructions

## Project Overview

Static website for an **Iterated Function System (IFS) Encyclopedia** built with **Astro v6**.
Deployed to GitHub Pages at `https://ifsdb.github.io`.

Dev server: `npx astro dev` (binds to `127.0.0.1` — see note below).

---

## Stack

| Layer | Technology |
|---|---|
| Framework | Astro v6.1.1 (static output) |
| Math rendering | remark-math + rehype-katex (server-side LaTeX) |
| Fractal rendering | `ifslib.wasm` via Web Worker |
| Styles | Plain CSS (`src/styles/global.css`) |
| Content | Astro Content Collections (Markdown) |
| Sitemap | `@astrojs/sitemap` (auto-generates `/sitemap-index.xml`) |

---

## Project Structure

```
astro.config.mjs          # Site config, math plugins, Vite defines
src/
  content.config.ts       # Content Collections schema (Astro v6 — must be here, NOT src/content/config.ts)
  content/
    ifs/                  # One .mdx file per IFS entry (MDX superset of Markdown)
  components/
    IFSCanvas.astro       # Fractal canvas component — uses Web Worker
    Header.astro          # Site navigation
    Footer.astro
    FormulaBlock.astro
  layouts/
    BaseLayout.astro      # Wraps every page
    IFSEntryLayout.astro  # Layout for /ifs/[slug] pages
  pages/
    index.astro
    about.astro
    ifs/
      index.astro         # Catalog with tag filter + sort
      [slug].astro        # Dynamic page per IFS entry
    tools/
      index.astro
      ifstile.astro
    search.astro          # Full-text client-side search
public/
  ifslib.wasm             # WASM fractal renderer (do not modify)
  ifslib-worker.js        # Web Worker that owns the WASM instance
  favicon.svg
scratch/                  # Fully gitignored — use for all temporary/scratch files
```

---

## IFSEntryLayout props

`IFSEntryLayout` accepts:
- `title`, `description`, `name`, `dimension` — as before
- `slug?: string` — optional; when provided, renders an "Edit this page on GitHub" link pointing to `src/content/ifs/<slug>.mdx`

---

## IFSCanvas behaviour

- Clicking the canvas opens `https://app.ifstile.com?aifs=<base64>` in a new tab.
- Hovering shows an "Open in IFStile ↗" badge (CSS `.ifs-open-hint` inside `.ifs-canvas-frame`).
- The canvas is wrapped in `.ifs-canvas-frame > canvas` (the outer `.ifs-canvas-wrapper` is still present).

---

## Entry page features

Every `/ifs/[slug]` page additionally renders:
1. **Breadcrumb** — `← Catalog` link above the heading (`.breadcrumb` in `IFSEntryLayout`).
2. **AIFS program block** — collapsible `<details class="aifs-details">` with a `Copy` button.
3. **Similar entries** — up to 3 cards filtered by shared tags (`.similar-entries`).
4. **Edit on GitHub** — link at the bottom of the page (only when `slug` prop is provided).

---

## Theme toggle

- A ◑ button in the header toggles dark/light mode.
- State is stored in `localStorage` as `ifs-theme` (`'dark'` | `'light'`).
- A `is:inline` script in `<head>` reads `localStorage` and sets `document.documentElement.dataset.theme` synchronously to prevent flash.
- CSS uses `[data-theme="dark"]` and `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { … } }` — system preference is respected when no manual override is set.

---

## IFStile Example Programs

The official IFStile repository contains 40+ canonical AIFS examples at:
**https://github.com/mekhontsev/ifstile/tree/main/Examples**

Key files for reference when creating new entries:

| File | Description |
|---|---|
| `x^2-2x+2_Twin_Dragon.aifs` | Twin Dragon, Heighway Dragon, Lévy C Curve, and variants |
| `x^2-3x+3_Koch_Snowflake.aifs` | Koch Snowflake (algebraic form) |
| `x^2-5x+7_Gosper_Island.aifs` | Gosper Island — 7 maps, hexagonal 2D tile |
| `x^4+x^2-1_Golden.aifs` | Golden Trapezoid GIFS (4D companion matrix) |
| `x^4-2x^3-x^2+2x+1_Robinson*.aifs` | Robinson Triangle GIFS |
| `Ammann_A3.aifs`, `Ammannn_Beenker.aifs` | Quasicrystal tilings |
| `Jerusalem cross.aifs` | Jerusalem Cross fractal |
| `[3D]_*.aifs` | Various 3D fractal examples |

These files use **template/finder blocks** (blocks with `$vector`/`$semigroup` for the IFStile search engine). The **canonical attractor block** to extract is the first `@:ParentID` block with concrete (non-template) h0…hN definitions. Strip the template wrapper and use only `$dim`, matrix/rotation definitions, and the attractor equation `A=g^-1*(h0|...|hN)*A`.

For comprehensive AIFS language examples including all operators, array operations, block functions, and JS interop, see the unit test file:
**https://github.com/mekhontsev/ifstile/blob/main/SrcTests/aifs_simple.cpp**

For tiling data (substitution rules, inflation factors, Hausdorff dimensions, bibliographic references), see the **Tilings Encyclopedia**:
**https://tilings.math.uni-bielefeld.de/**

For a large catalog of self-similar IFS tiles classified by Perron number (quadratic, cubic, metallic), construction method, attractor shape, and topological properties, see **Stewart Hinsley's Self-Similar Tiles**:
**http://www.stewart.hinsley.me.uk/Fractals/IFS/Tiles/Tiles.php**

For classic IFS examples with geometric descriptions, standard matrix form, L-systems, similarity dimensions, and variants, see **Larry Riddle's Classic IFS collection** (Agnes Scott College):
**https://larryriddle.agnesscott.org/ifs/ifs.htm**

---

## Adding a New IFS Entry

Create `src/content/ifs/<slug>.mdx`. The slug is the filename without `.mdx` and becomes the URL at `/ifs/<slug>`. All entries use **MDX** (`.mdx`), which is a superset of Markdown — plain Markdown body works unchanged, but you can also embed JSX components when needed (e.g. multiple `<IFSCanvas>` elements).

### Required frontmatter fields

```yaml
---
name: "Human-readable name"
description: "One-sentence description (used in <meta> and search index)."
cardDescription: "Short text shown on the catalog card (optional, falls back to description)."
dimension: "≈ 1.585"          # optional, Hausdorff dimension as a display string
transforms: 3                  # number of affine transformations (positive integer)
tags: [plane, self-similar]    # array of lowercase strings; used for filtering
aifs: |                        # AIFS program — see format below
  @
  $dim=2
  f1=[0,0]*[0.5,0,0,0.5]
  f2=[1,0]*[0.5,0,0,0.5]
  f3=[0.5,0.866]*[0.5,0,0,0.5]
  S=(f1|f2|f3)*S
references:                    # optional
  - text: "Author (year). Title."
  - text: "Wikipedia article"
    url: "https://en.wikipedia.org/wiki/..."
---
```

### AIFS language — full reference

The `aifs` field is an IFStile/ifslib program. The full language is documented in [Mekhontsev (2019), Appendix E](https://epub.ub.uni-greifswald.de/frontdoor/index/index/docId/2479). Both `ifslib.wasm` and `app.ifstile.com` support the complete language.

#### File structure
```
@@import other.aifs    # optional: include another file (relative path)

@ID:ParentID           # block start: ID and ParentID are optional unique strings
# comment              # lines starting with # are comments
$dim=2                 # dimension of rational space (required)
...                    # variable definitions and attractor equations
```
- **`#` starts a comment** — everything from `#` to end of line is ignored. End-of-line comments (`x=1 # note`) are valid. The `#` character has no special meaning inside string values or matrix literals.
- A file can contain any number of blocks separated by `@ID:ParentID` lines.
- Each block is a GIFS that may define multiple attractor sets.
- A block **inherits** all definitions from its parent block and can override them.
- `ID` can be empty (`@`) for anonymous blocks. `ParentID` can be empty (no parent).

**Rendering selection:**
- **`ifslib`** renders the **first visible block** and within it the **first visible attractor set** — unless `$root` overrides this.
- **IFStile** has UI to browse and select any block and any set within it.
- Use `$root=S` inside a block to tell `ifslib` which set to render from that block.

#### Variable types
| Prefix | Meaning |
|---|---|
| (none) | Ordinary variable — computed once |
| `$name` | Built-in special variable (e.g. `$dim`, `$subspace`) |
| `&name` | Substitution macro — re-evaluated at each use site |

#### Operators
| Syntax | Meaning |
|---|---|
| `f1*f2` | Composition: x → f1(f2(x)) |
| `S1\|S2` | Union of sets (or operators): S1 ∪ S2 |
| `f^n` | n-fold composition f∘f∘...∘f |
| `f^-1` | Inverse map f⁻¹ |
| `+`, `-`, `*`, `/`, `^` | Arithmetic on scalars and matrices |
| `%` | Modulo: `a%b` — result has sign of `b` (Python-style); `b=0` returns `a` |
| `$i` | Identity map |
| `$e` | Empty set ∅ |

Operator precedence note: `2*[1,0]` = 2(x+[1,0]) = 2x+[2,0] but `[1,0]*2` = 2x+[1,0].
In general `[t]*M` applies M then adds t (standard affine form **f(x) = M·x + t**).

#### Vectors and matrices
- `[a1, a2, ..., an]` — n-element vector; auto-converted to a translation or matrix by context.
- For `$dim=2`: a 2-vector is a translation, a 4-vector is a 2×2 matrix (row-major).
- For `$dim=n`: an n-vector is a translation, n²-vector is an n×n matrix.
- Element access: if `v=[a1,..,an]` then `v[0]=a1`, `v[n-1]=an`.

#### Affine map form
The standard form for a 2D map is:
```
f=[tx,ty]*[a,b,c,d]   # translation [tx,ty] after matrix [[a,b],[c,d]]
                       # i.e. f(x) = [[a,b],[c,d]]·x + [tx,ty]
```
Pure translation: `[tx,ty]` — shifts x by [tx,ty].
Pure scaling: `[0.5,0,0,0.5]` — scales by 0.5 (no translation).

#### Special matrix constructors and built-in constants
| Syntax | Meaning |
|---|---|
| `$companion([a0,a1,...,an-1])` | Companion matrix for the monic polynomial a₀+a₁x+...+aₙ₋₁xⁿ⁻¹+xⁿ |
| `$exchange()` | Anti-diagonal identity matrix (exchange matrix χₙ) |
| `$charpoly(M)` | Characteristic polynomial coefficients of matrix M as a vector `[a0,...,an-1]` (monic, ascending) |
| `$numden(val, eps?)` | Rational approximation of val: returns `[numerator, denominator]`. Returns `[0,0]` if no rational found within tolerance |
| `$pi` | The constant π |

Example: `s=$companion([1,-1,1,-1])` defines the companion matrix for the cyclotomic polynomial x⁴−x³+x²−x+1 (used for pentagonal/golden-ratio IFS).

#### Special variables
| Variable | Meaning |
|---|---|
| `$dim=n` | Dimension of the rational space (required in every block) |
| `$n=name` | Human-readable name for the block, displayed in IFStile's block list. No effect on rendering. |
| `$subspace=[M, i1, i2, ...]` | Projection from the n-dimensional rational space to the rendering subspace. `M` is a matrix identifier; each index selects one **real Jordan cell** of `M`. A real eigenvalue → 1D cell (contributes 1 rendering dimension); a complex conjugate pair → 2D cell (contributes 2 rendering dimensions). The total rendering dimension equals the sum of the selected cells' dimensions. Indices are 0-based positions in the sequence of eigenvalues with Im(λ) ≥ 0, ordered by **decreasing modulus** (ties broken by decreasing real part). |
| `$root=name` | Selects which attractor set is shown first in this block. `ifslib` always renders this set; IFStile uses it as the initial selection when the user switches to the block. Not needed if the desired set is already the first one defined in the block. |
| `$camera=...` | Sets the view for a block. **2D**: `$camera=[cx, cy, r, angle]` — center `(cx,cy)`, screen radius `r`, rotation angle (degrees). **3D**: `$camera=[[loc],[target],[up],fov]` — camera position, look-at point, up vector, field of view in degrees. Example 3D: `$camera=[[-0.1,0.55,-3],[0.5,-0.5,0.62],[0.17,0.74,0.15],30]`. Supported by both `ifslib` and IFStile. |
| `$a=c` | Marks the block as **checked** in IFStile's UI. UI-only — has no effect on `ifslib`. |
| `$a=h` | Marks the block as **hidden**. Both `ifslib` and IFStile skip hidden blocks; `ifslib` searches for the first non-hidden block to render. Hidden blocks are still usable as parent blocks (via `@ID:ParentID`) by non-hidden blocks. |

Example: `$subspace=[s,0]` projects onto the eigenplane of eigenvalue index 0 of matrix `s`. Used together with `$companion` for algebraic IFS whose attractor lives in a 2D eigenspace of a higher-dimensional rational space.

`$subspace` is also meaningful for native 2D IFS (`$dim=2`). When the IFS is defined using eigenvectors of a matrix `s` as a natural coordinate basis (e.g. Gosper Island uses the Eisenstein integer basis of `s=$companion([1,-1])`, which corresponds to 60° lattice axes), specifying `$subspace=[s,0]` tells ifslib to render in the eigenvector basis of `s` rather than the standard `(1,0),(0,1)` basis. This rotates and scales the rendered image to align with the algebraic structure of the IFS — the attractor is displayed in its "natural" orientation.

#### Mathematical functions (scalars)
`sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `exp`, `log`, `floor`, `ceil`, `arg`.

`if` — conditional:
- `if(cond)` → 1 if cond > 0, else 0
- `if(cond, val1, val2)` → val1 if cond > 0, else val2
- `if(cond1, val1, cond2, val2, default)` → multi-branch: first positive condition wins

#### Array operations
| Syntax | Meaning |
|---|---|
| `a[-1]` | Negative index: last element (`a[-2]` = second-to-last, etc.) |
| `a()` | Array size (number of elements) |
| `a[start:end:step]` | Python-style slicing; step optional (default 1); negative step reverses |
| `a[]` | Flatten one nesting level |
| `a[idxArr]` | Fancy indexing: select multiple elements by index array |
| `[e0,e1,...](idx)` | Lazy indexing: evaluates only element at `idx`, others are not computed |

Auto-generation syntax — a single array can contain any number of generator segments interleaved with static elements:
```
[static..., $, termCond, genExpr, static..., $, termCond, genExpr, static...]
```
- Static elements before, between, and after generator segments are appended as-is.
- `$` — marks start of a generator segment; `$` is shorthand for `$(0)` — a reference to the **current array being built**
- `$()` = `$(0)()` = current length of the array being built (equals current index during generation)
- `$[-1]` = `$(0)[-1]` = last element of the current array (i.e. the previously appended element)
- `$(1)`, `$(2)`, … — references to enclosing (parent, grandparent, …) arrays; useful when building nested arrays
- `termCond` — generate while `termCond > 0`; `N-$()` generates until total count reaches N
- `genExpr` — expression for each generated element
- `tail...` — zero or more static elements appended after generation stops
- Example: `[0, 1, $, 7-$(), $[-1]+$[-2]]` → 7 Fibonacci values `[0,1,1,2,3,5,8]`

#### Block functions
A block (`@name`) can be used as a reusable function:
```
@funcName
param1 = defaultVal    # parameter with default value
param2 = defaultVal
ret = expr             # return value

@
result = funcName(arg1, arg2)    # call by position
result = funcName()              # call with all defaults
result = $new(funcName, param2, val2)  # call with named overrides
field  = result.param1           # field access on block instance
```
- The **last variable defined** in the block is the return value. Naming it `ret` is a readable convention — the name has no special meaning to the interpreter.
- Block inheritance (`@child:parent`) — child overrides parent variables; any block can be a parent.
- `@:ParentID` — child with no ID (anonymous), inherits from parent.

#### JavaScript interop
AIFS files can embed ES module JavaScript before the first `@@` separator:
```
export function funcName(arg) { return arg + 1; }
export const constArr = [11, 12];
@@

@
$init = funcName        # call JS function once at init (can assign AIFS variables)
result = funcName(3)    # call JS function from AIFS
val    = constArr[1]    # access JS constant
```
- JS functions callable from AIFS must be `export`ed.
- `console.log(...)` is available inside JS functions.
- `$init = jsFunc` calls `jsFunc` once during block initialization; the function can set `this.varName = value` to inject AIFS variables.

#### Ordinary IFS attractor equation
```
S=(f1|f2|f3)*S    # S is the unique compact attractor of the IFS {f1,f2,f3}
```
**Mandatory**: without an attractor equation `ifs_select` returns 0 and nothing renders.

#### GIFS (Generalized IFS — multiple attractors)
When the self-similar system defines multiple interleaved attractors, each gets its own equation. The attractor variables appear on both sides:
```
@
$dim=4
$subspace=[s,0]
s=$companion([1,-1,1,-1])    # companion matrix for cyclotomic polynomial
r=$exchange()
g=s-s^4                      # expansion matrix
A1=g^-1*(h1*A1|h2*A1|h3*A2) # A1 and A2 are the two Robinson triangle types
A2=g^-1*(h4*A1|h5*A2)
```
Here `h*A` denotes the image of attractor set A under map h.

`g` must be an **expansion** (spectral radius > 1 after projection) to guarantee that the attractor exists. If `g` is a contraction, existence depends on the GIFS dependency graph.

#### Templates (for IFStile Finder/search, not needed for rendering)
| Syntax | Meaning |
|---|---|
| `$real(a,b)` / `$integer(a,b)` | Distribution `T`: uniform on [a,b] (real or integer) |
| `$number(T)` | Distribution `T` for a scalar: passed to `$semigroup`, `$vector`, etc. |
| `$semigroup([g1,...,gm], T)` | Random element of the semigroup generated by g1…gm, with element distribution T |
| `$vector(L, T)` | Random vector of length L with component distribution T |

`T` can be a `$real(a,b)` or `$integer(a,b)` uniform distribution, or a number (log-variance of a normal distribution on ℝ, i.e. σ = e^(T/2)), or omitted (IFStile uses its Finder “log variance” parameter as default).

#### Example — simple 2D IFS (Sierpiński triangle)
```
@
$dim=2
f1=[0.5,0,0,0.5]
f2=[0.5,0]*[0.5,0,0,0.5]
f3=[0.25,0.5]*[0.5,0,0,0.5]
S=(f1|f2|f3)*S
```

#### Example — algebraic IFS via companion matrix (Rauzy fractal)
```
@
$dim=3
$subspace=[g,0]
g=$companion([-1,1,1])   # companion for x³+x²+x-1 (tribonacci)
A=(g^-1|g^-2*[0,1,0]|g^-3*[0,1,1])*A
```

The `aifs` YAML field uses a literal block scalar (`|`) to preserve newlines.

### Markdown body

Write freely in Markdown. Math is supported via LaTeX:
- Inline: `$f(x) = ax + b$`
- Block: `$$\begin{pmatrix}...\end{pmatrix}$$`

Use single `\` inside YAML (e.g. `\\frac`) and single `\` in Markdown body (rehype-katex handles both).

**Consecutive block equations**: Always separate adjacent `$$...$$` blocks with a blank line. Without the blank line, remark-math merges them into a single render block, making them hard to read.

**`$$` must be on its own line**: remark-math only recognises a block math delimiter when `$$` appears alone on a line. Never write `$$\begin{aligned}` or `\end{aligned}$$` — always put the opening and closing `$$` on separate lines:
```
$$
\begin{aligned}
...
\end{aligned}
$$
```
Inline `$$` at the start or end of a content line causes remark-math to miss the closing delimiter, turning all subsequent text red (raw LaTeX source rendered as plain text).

### Multiple canvases (MDX JSX)

To show more than one fractal canvas in an entry (e.g. a GIFS with multiple attractors):

```mdx
import IFSCanvas from '../../components/IFSCanvas.astro';

export const aifsA1 = `@
$dim=4
...
$root=A1
A1=...
A2=...`;

export const aifsA2 = `@
$dim=4
...
$root=A2
A1=...
A2=...`;

<div class="canvas-row">
  <figure>
    <IFSCanvas id="slug-a1" aifs={aifsA1} width={380} height={380} label="A1 label" />
    <figcaption>$A_1$ — description</figcaption>
  </figure>
  <figure>
    <IFSCanvas id="slug-a2" aifs={aifsA2} width={380} height={380} label="A2 label" />
    <figcaption>$A_2$ — description</figcaption>
  </figure>
</div>
```

CSS for `.canvas-row` / `.canvas-row figure` / `.canvas-row figcaption` is in `src/styles/global.css`.
Use `export const` (not plain `const`) — plain `const` is inaccessible inside the compiled MDX content function.

---

## Content Collections Schema

Defined in `src/content.config.ts` (Astro v6 format — **not** `src/content/config.ts`):

```ts
{
  name: z.string(),
  description: z.string(),
  cardDescription: z.string().optional(),
  dimension: z.string().optional(),
  transforms: z.number().int().positive(),
  tags: z.array(z.string()).default([]),
  aifs: z.string(),
  references: z.array(z.object({
    text: z.string(),
    url: z.string().url().optional(),
  })).optional(),
}
```

Always use `entry.data.tags ?? []` when reading tags — never assume the array is defined even with `.default([])` due to caching behavior.

---

## Fractal Rendering Pipeline

### Components

- **`IFSCanvas.astro`** — Astro component. Accepts `id`, `aifs`, `width`, `height`, `label` props. Embeds AIFS as `data-aifs` on the `<canvas>`. The `<script>` block is deduplicated by Astro across all instances on a page — all canvases share one worker and one set of module-level state variables.

- **`public/ifslib-worker.js`** — Web Worker. Compiles `ifslib.wasm` once (cached as `wasmModule`), but instantiates a **fresh WASM instance per render request** (required because `ifslib` has a single global renderer in each instance — concurrent renders need separate instances). Renders progressively at sizes `[32, 64, 128, ..., maxDim]` using round-robin interleaving across all pending canvases.

- **`public/ifslib.wasm`** — Pure WASI reactor. Exports:
  - `_initialize()` — must be called once after instantiation
  - `init(ptr) → 0|1` — parse AIFS source (C string ptr)
  - `ifs_select(block_ptr, root_ptr) → 0|1` — select block and root attractor (empty → first non-hidden / default)
  - `set_camera(params_ptr, num_params) → 0|1` — override the camera/viewport for subsequent `render()` calls. Must be called after `ifs_select()`. Two layouts selected by `num_params`:
    - **2D** (`num_params=4`): `[cx, cy, r, angle_deg]` — viewport center, inscribed-circle radius, rotation angle in degrees.
    - **3D** (`num_params=10`): `[loc.x, loc.y, loc.z, ref.x, ref.y, ref.z, up.x, up.y, up.z, fov_deg]` — camera location, look-at point, up vector, field of view in degrees.
    - **Reset** (`num_params=0`): resets to automatic camera (fit to attractor on next `render()` call). `params_ptr` is ignored.
    - Returns 0 if no block is selected or `num_params` is not 0, 4, or 10. `params_ptr` points to a `double[]` array in WASM memory. When not called, `$camera` from the AIFS block is used.
  - `render(w, h, quality, thickness) → pixelPtr` — render to RGBA pixel buffer (`width * height * 4` bytes). `quality >= 1`; quality=2 is usually sufficient for good results, computation time grows exponentially with quality. `thickness >= 1` in pixels, use 1 as default. Returns NULL on failure. Pixel data is valid until the next `render` call and must not be freed by the caller.
  - `information(what_ptr) → 0|1` — compute analytics for the currently selected block; output goes to `get_last_output()`. Values for `what`:
    - `"Measure"` — Hausdorff dimension, centroid `C`, principal moments `I`, eigenvectors `Q` (aspect ratio can be derived from `I`). All attractor sets are printed, including dim=0 fixed points (which have `I=0` and no `inv` field).
    - `"Dimension"` — numerical Hausdorff dimension estimate with polynomial equation
    - `"Evaluation"` — evaluated map matrices (useful for verifying companion matrix expansions)
    - `"Components"` — variable-to-graph-component mapping. Output: one line per variable, `varName: componentNumber`. Variables named `/^i\d+$/` in a boundary AIFS (output of `custom_ifs`) are intersection pieces; all others are original attractor variables.
    - `"Subspaces"` — affine subspaces for every attractor set. Output format per variable: `varName: n m` on a header line, followed by a data block with the concrete points. `n` = number of points spanning each affine subspace (affine dimension = `n − 1`); `m` = number of subspaces in the union that contains the set. The data block has `n × m` rows total, grouped in sets of `n` rows per subspace, each row being one point (space-separated coordinates).
      - `n=1, m=1` → 0D (single point), 1 row
      - `n=2, m=1` → 1D (line segment), 2 rows
      - `n=3, m=1` → 2D (plane / polygon), 3 rows
      - `n=4, m=1` → 3D (3D region), 4 rows

      **Polyhedral boundary detection**: after `custom_ifs(0, 2)`, load the boundary AIFS and call `information("Subspaces")`. If all `i*` variables have `n ≤ ambient_dim` (where `ambient_dim` = first number of the attractor `A` minus 1), the boundary pieces are linear — i.e. the boundary is polyhedral (straight edges in 2D, flat faces in 3D).

      **Important**: `n ≤ ambient_dim` means the piece is *contained in a hyperplane*, but does **not** mean it is straight. A piece with `n = ambient_dim` is a curve that spans the full ambient space (e.g. an infinite-sided polygon has `n = 3` in 2D). Only `n < ambient_dim` (piece fits in a lower-dimensional affine subspace, i.e. a line in 2D) guarantees straight edges. Use `information("Dimension")` together with Subspaces for a complete picture: `Subspaces` tells you the affine dimension of the containing subspace; `Dimension` tells you the Hausdorff dimension of the piece itself. A polyhedral piece has both `n ≤ ambient_dim` AND integer Hausdorff dimension equal to `n-1`; a curved (infinite-sided polygon) boundary has `n = ambient_dim` but `Dimension = 1` (integer).

      Both `bitmask=0` and `bitmask=1` are now correct for this check. A previous bug in `bitmask=1` that produced incorrect `n=4` pieces for menger-sponge has been fixed.
    - `"Projection"` — projected IFS as graphviz digraph + map definitions
    - `"Balls"` — approximate bounding ball (center + radius); guaranteed to be at most 3/2 times the minimum enclosing ball radius, not the exact minimum
    - `"Diameters"` — geometric diameter, diameter endpoints, center of mass, squared radius (slow)
    - `"NormalMaps"` — normal map indices
    - `"AST"` — abstract syntax tree of parsed maps

    **Slow operations:** `Dimension`, `Diameters`, `Subspaces` can be slow. All others are fast.

    `information("Dimension")` works in the **rendering Euclidean space**, which is determined by `$subspace` (or `$dim` if no subspace). This means it correctly handles **any ambient dimension**: 2D tiles (boundary dim ∈ (1,2)), 3D fractals (boundary dim ∈ (2,3)), GIFS with multiple attractor types, and algebraic IFS projected via `$subspace` from a higher `$dim`. The dimension is always relative to the actual rendered space, not the rational space.

    **Output format** — one section per group of components sharing the same dimension (multiple component IDs can share the same substitution matrix and thus the same dimension):
    ```
    Component IDs: 4, 5
    dim ~= 1.523627086202492
    dim = 2*log(x)/log(p)
    p = p0 = 2
    x^3-x^2-2=0
    x~=1.695620769559862
    Component IDs: 1, 2, 3
    dim ~= 0
    dim = 2*log(x)/log(p)
    p = p0
    1=0
    x~=1
    ```
    When `p` is a product of complex roots, additional lines appear between `p =` and the polynomial:
    ```
    p = p0 = |product of used roots|
    p0 ~= 5.828...
    used roots of z^4-...:
             2.414...
             2.414...
    x^2-4*x-4=0
    ```
    To extract the polynomial: scan forward from the `dim ~=` line, stop at the next `Component IDs:` line, and pick the first line matching `/^x[^~]/`. The polynomial can be up to ~10 lines after `dim ~=` when complex roots are listed.

    **Parsing note:** the `Component IDs:` line lists all component numbers that share the same dimension block (comma-separated). When filtering for i\* components, a block is relevant if **any** of its listed IDs is an i\* component.

  - `calc_neighbor_graph(ires_ptr, settings_ptr) → 0|1` — computes the neighbor intersection graph. Must be called after `ifs_select()` and before `custom_ifs()`. Precision/budget parameters live here (not in `custom_ifs`).

    **`integer_ims::settings` input struct (20 bytes, align 4):**
    | Offset | Type | Field | Default | Meaning |
    |---|---|---|---|---|
    | 0 | uint32 | `max_inters` | 4000 | max elements in search tree |
    | 4 | uint32 | `max_depth` | `0xFFFFFFFF` | max tree depth; no limit |
    | 8 | uint32 | `max_bits` | 63 | rational precision bits; >63 = big-rational (slow) |
    | 12 | float32 | `prec` | 0.0 | 0.0 = exact rational; ~0.3 = float/infinite graphs |
    | 16 | uint8 | `mode_ori` | 0 | 1 = orientation-finding mode (ignores translates) |
    | 17 | uint8 | `stop_on_overlap` | 1 | stop vertex on first overlap found |
    | 18 | uint8 | `stop_on_incomplete` | 1 | abort if any vertex cannot be fully processed; ensures `m_completed=0` when budget exceeded |
    | 19 | uint8 | (padding) | 0 | |

    **`inter_result` output struct (20 bytes, align 4):**
    | Offset | Type | Field | Meaning |
    |---|---|---|---|
    | 0 | uint32 | `m_gcx` | intersections checked |
    | 4 | uint32 | `m_depth` | tree depth reached |
    | 8 | uint32 | `m_bits` | rational precision bits used; **0** = non-exact IFS (sin/cos/decimals) |
    | 12 | uint32 | `m_over_depth` | **0** = OSC holds; **>0** = OSC violated at this depth |
    | 16 | uint8 | `m_completed` | 1 = fully computed; 0 = cut short by budget — try larger `max_inters` |
    | 17 | uint8 | `m_overflowed` | 1 = rational overflow occurred |
    | 18 | uint8 | `m_mode` | arithmetic mode: 0=rational, 1=big_rational, 2=real |
    | 19 | uint8 | (padding) | |

    **Tiered `max_inters`:** some IFS need large budgets: try 8000 → 50000 → 200000. Danzer needs ~50 000, Quaquaversal needs ~200 000.

    **Do NOT use `prec > 0` (float mode).** Float mode results are unreliable for non-rational IFS. Always use `prec=0`. (When float search is intentionally desired, `0.3` is a reasonable value.)

    **Detecting non-exact IFS:** IFS defined with `sin`, `cos`, or decimal literals like `0.5` will return `m_bits=0`. Decimal literals are intentional float-mode signals — do NOT auto-convert to fractions.

  - `custom_ifs(bitmask, lim) → 0|1` — generates AIFS output from the neighbor graph computed by `calc_neighbor_graph()`. Must be called after `calc_neighbor_graph()`. Output goes to `get_last_output()` as a ready-to-use AIFS program (no comment header). **`bitmask=0`** is a special mode: boundary for every attractor. Individual bits: 0=intersections between neighbors, 1=connections between neighbors, 2=neighbourhoods, 3=neighbourhood graph, 4=relators (group encoding of neighbor graph), 5=alternative boundary. `lim=2` for boundary (pieces of the boundary are pairwise intersections of neighbors).

    **Variable name prefixes in the output AIFS** (names are `<prefix><1-based index>`, e.g. `i1`, `k3`):
    | Prefix | Example | Content |
    |---|---|---|
    | `q` | `q1` | extra pre-evaluated references from eval context |
    | `k` | `k1` | IFS contraction maps from the index map |
    | `e` | `e1` | identity-map label for each contraction map (emitted when neighbors/intersections are requested) |
    | `v` | `v1` | implicit attractor sets for graph vertices with no direct user reference |
    | `m` | `m1` | neighbor conjugacy maps $r^{-1} \cdot ? \cdot f$ for each pairwise neighborhood |
    | `id_` | `id_1` | group relators (bitmask bit 4) |
    | `i` | `i1` | **pairwise boundary/intersection sets** (bitmask bit 0, lim=2) — individual pieces of ∂A, one per neighbor pair |
    | `u` | `u1` | pairwise connection unions (bitmask bit 1, lim=2) |
    | `j` | `j1` | higher-order intersection sets (bitmask bit 0, lim≥3) |
    | `w` | `w1` | higher-order connection unions (bitmask bit 1, lim≥3) |
    | `<Name>_n<N>` | `A_n1` | **full boundary of attractor `<Name>`** — defined as `i1\|i2\|...\|iN` (union of all pairwise pieces). The subscript `_n1` counts neighbor-union levels. This IS the complete ∂A, but reading its dimension from `information("Dimension")` is redundant since it equals the max dim of its `i*` constituents. |

    When parsing `information("Measure")` output for boundary dimension: variables matching `/^i\d+$/` are the individual ∂A pieces; all others (`k`, `e`, `v`, `<Name>_n<N>`, original attractor names) are to be ignored when filtering components.
  - `get_last_output() → charPtr` — console output accumulated since last call (errors and `information` results). Returned pointer is valid until the next ifslib call and must not be freed by the caller.
  - `malloc`, `free`, `memory`

### Boundary dimension pipeline

The combination of `calc_neighbor_graph` + `custom_ifs` → `information("Components")` → `information("Dimension")` computes the Hausdorff dimension of the boundary ∂A of an IFS attractor A.

**Step 1 — compute neighbor graph and boundary IFS:**
```js
// Write integer_ims::settings (20 bytes)
function writeSettings(wasm, maxInters, maxDepth, maxBits, prec) {
  const ptr = wasm.malloc(20);
  const v = new DataView(wasm.memory.buffer);
  v.setUint32  (ptr +  0, maxInters, true);
  v.setUint32  (ptr +  4, maxDepth,  true);  // 0xFFFFFFFF = no limit
  v.setUint32  (ptr +  8, maxBits,   true);
  v.setFloat32 (ptr + 12, prec,      true);  // 0.0 = exact rational
  v.setUint8   (ptr + 16, 0);  // mode_ori
  v.setUint8   (ptr + 17, 1);  // stop_on_overlap (default)
  v.setUint8   (ptr + 18, 1);  // stop_on_incomplete (default) — ensures m_completed=0 when budget exceeded
  v.setUint8   (ptr + 19, 0);  // padding
  return ptr;
}

// Read inter_result (20 bytes)
function readInterResult(wasm, ptr) {
  const v = new DataView(wasm.memory.buffer);
  return {
    checked:   v.getUint32(ptr +  0, true),  // m_gcx
    depth:     v.getUint32(ptr +  4, true),  // m_depth
    bits:      v.getUint32(ptr +  8, true),  // m_bits (0 = non-exact IFS)
    oscDepth:  v.getUint32(ptr + 12, true),  // m_over_depth (0 = OSC holds)
    completed: v.getUint8 (ptr + 16),        // m_completed
    overflow:  v.getUint8 (ptr + 17),        // m_overflowed
    mode:      v.getUint8 (ptr + 18),        // 0=rational,1=big_rational,2=real
  };
}

const iresPtr = wasm.malloc(20);
const settingsPtr = writeSettings(wasm, 4000, 0xFFFFFFFF, 63, 0.0);
const ok = wasm.calc_neighbor_graph(iresPtr, settingsPtr);
wasm.free(settingsPtr);
const ires = readInterResult(wasm, iresPtr);
wasm.free(iresPtr);

if (!ok || !ires.completed) { /* retry with larger maxInters */ }

// Generate boundary AIFS (bitmask=0: boundary for every attractor)
wasm.custom_ifs(0, 2);
const boundaryAifs = readCString(wasm, wasm.get_last_output());
```
The boundary AIFS is a GIFS whose attractor variables are the pieces of ∂A. No comment header — output is clean AIFS directly.

**Step 2 — identify attractor vs intersection components:**
Load the boundary AIFS into a fresh instance. Call `information("Components")`. Its output is lines of form `varName: componentNumber`. Variables named `/^i\d+$/` (e.g. `i1`, `i17`, `i103`) are the individual pairwise boundary pieces — these are the ones whose dimension gives dim(∂A). The variable `A_n1` (pattern `<Name>_n<N>`) is the **full** boundary ∂A = union of all `i*` — so its dimension equals the max dim of the `i*` pieces, but it gets its own component number and should also be skipped when filtering (reading the `i*` components directly is more precise). All other names (`A`, `B`, `S`, `k1`, `e1`, `v1`) must also be skipped: `A`/`B`/`S` are the original attractors inherited from parent block `@UN0`, and `k*`/`e*`/`v*` are auxiliary map variables; none of these are boundary pieces.

**Important:** the boundary AIFS block inherits the original attractor variables (`A`, `B`, `S`, …) from its parent block `@UN0`. These inherited attractors appear in `information("Components")` output with their own (non-boundary) component numbers and show up in `information("Dimension")` with the attractor's own fractal dimension (e.g. dim≈1.26 for Koch curve's `A`). If you don't filter them out, you will mistakenly read the attractor's dimension instead of the boundary dimension. **The rule is simple: only `i*` variable component numbers are boundary components. All others must be skipped.**

```js
// Parse Components output → Set of component numbers that are NOT boundary (i.e. non-i* variables)
function findAttractorComps(output) {
  const comps = new Set();
  for (const line of output.split('\n')) {
    const m = line.match(/^(\w+):\s*(\d+)$/);
    if (m && !/^i\d+$/.test(m[1])) comps.add(parseInt(m[2]));
  }
  return comps;
}
```

**Step 3 — read dimension, skipping non-boundary components:**
Call `information("Dimension")`. Iterate components; skip any whose number is in `attractorComps` (i.e. skip all components that don't belong to `i*` variables). Among the **remaining** (intersection-piece only) components:
- If all have integer dimension → **polyhedral boundary**: dim=1 means straight-edge pieces (2D tiling), dim=2 means flat-face pieces (3D tiling).
- If all have dim ≈ 0 → **point contacts only** (tiles touch at isolated points; also applies to curves like Koch curve where the "tiles" only touch at endpoints). OSC still holds.
- If any have fractional dimension → that is dim(∂A). Use the highest fractional-dim component.

**Note on polynomials — finding the minimal polynomial:**

`information("Dimension")` outputs the **characteristic polynomial** of the substitution matrix for the boundary component. This polynomial may be **reducible** and contain spurious factors. The spurious factors arise from symmetry subspaces of the substitution matrix: if the IFS has a discrete symmetry (rotation, reflection), the boundary substitution matrix block-diagonalises and its characteristic polynomial is a product of factors from each invariant subspace.

**General rule:** A monic integer factor $f(x)$ of $q(x)$ is spurious if and only if **all** its complex roots have modulus strictly less than $\lambda$ (the dominant real root of $q(x)$). The minimal polynomial is the unique remaining factor after dividing out all spurious ones — equivalently, it is the factor whose dominant root equals $\lambda$.

The degree of a spurious factor equals the dimension of the corresponding symmetry subspace. For $n$-fold symmetry the symmetry contribution has degree $\phi(n)$ (Euler totient): 4-fold gives degree 2, 3-fold gives degree 3 (since $\phi(3)=2$ for $\mathbb{Z}[i]$ but degree 3 for the tribonacci case), etc. In practice search all integer divisors up to half the degree of $q(x)$.

**Recipe to extract the minimal polynomial of dim(∂A):**

1. From the `dim ~= D` line, extract the reported polynomial `q(x)`. Find `λ` numerically (its largest positive real root).
2. **First check the known spurious factors table below** — if the IFS is listed there, apply the known factorization directly without search.
3. Otherwise: try all integer divisors of `q(x)` of degree 1, 2, 3, … up to `floor(deg(q)/2)` via polynomial long division.
4. A factor is **spurious** if all its complex roots have modulus < `λ`. Divide `q(x)` by all spurious factors. The remain is the minimal polynomial.

**Why spurious factors have smaller modulus:** the dimension formula is `dim = 2·log(λ)/log(p)` where `p = |g|²` (expansion norm squared) and `λ` is the spectral radius of the boundary substitution. Any symmetry eigenvalue `μ` satisfies `|μ| < λ` (otherwise it would set a higher dimension), so spurious factors always have roots of strictly smaller modulus.

**General algebraic structure of spurious eigenvalues:** spurious eigenvalues always lie exactly on the circle $|\mu| = \sqrt{p}$, giving $\dim = 2\log\sqrt{p}/\log p = 1$ — a whole-dimension value. Their minimal polynomial over $\mathbb{Q}$ can sometimes be identified analytically:
- For IFS in $\mathbb{Z}[i]$ (Gaussian integers, expansion $g$), the spurious factor is the minimal polynomial of $g$ itself or of $-\bar{g}$ depending on the symmetry direction. E.g. twin-dragon: $g = 1+i$, MinPoly$(g) = x^2-2x+2$. Levy-c-curve: $\mu = -1+i = -\bar{g}$, MinPoly$(\mu) = x^2+2x+2$.
- For IFS with permutation symmetry (e.g. Rauzy, whose 3-letter alphabet has a $C_3$ symmetry), the spurious factor is the minimal polynomial of a primitive root of unity twisted by $\sqrt{p}$: the roots of $x^3+x^2+x-1$ lie on $|z|=\sqrt{\tau}$ and correspond to the non-trivial characters of $C_3$.
- In general: if the IFS has $n$-fold symmetry with expansion $|g|^2=p$, the spurious factor is (a factor of) the minimal polynomial over $\mathbb{Q}$ of $\sqrt{p}\cdot\zeta$, where $\zeta = e^{2\pi i/n}$.

**Known spurious factors and their source:**

| IFS | Characteristic poly degree | Spurious factor | Spurious roots | Source |
|---|---|---|---|---|
| twin-dragon | 5 | x²−2x+2 | 1±i, modulus √2 | 4-fold rotation symmetry of the boundary |
| levy-c-curve | 11 | x²+2x+2 | −1±i, modulus √2 | reflection symmetry of the boundary |

| rauzy-fractal | 7 | x³+x²+x−1 | complex pair, modulus √τ | 3-fold rotational symmetry of the Rauzy fractal |

Both spurious quadratic factors have p=2, `|μ|=√2=p^(1/2)`, giving `2·log(√2)/log(2)=1`. They encode geometric symmetry, not fractal complexity.

**JS snippet for integer factor search (searches all degrees up to floor(n/2)):**
```js
function polyDiv(num, den) {
  const r = [...num]; const q = [];
  for (let i = 0; i <= num.length - den.length; i++) {
    const c = r[i] / den[0]; q.push(c);
    for (let j = 0; j < den.length; j++) r[i+j] -= c*den[j];
  }
  return [q, r.slice(r.length - (den.length-1))];
}
// Find dominant root of poly p (largest positive real root)
function dominantRoot(p) {
  let lo=1, hi=100;
  const ev = x => p.reduce((s,c)=>s*x+c,0);
  if (ev(hi) < 0) return null;
  while (hi-lo > 1e-12) { const m=(lo+hi)/2; ev(m)<0 ? lo=m : hi=m; }
  return (lo+hi)/2;
}
const lambda = dominantRoot(coeffs);
// Try all integer divisors of degree d, for d = 1..floor(n/2)
const maxD = Math.floor((coeffs.length-1)/2);
function search(d, prefix, remaining) {
  if (prefix.length === d+1) {
    const den = [1, ...prefix];
    const [q, rem] = polyDiv(remaining, den);
    if (!rem.every(x=>Math.abs(x)<1e-6)) return;
    if (!q.every(x=>Math.abs(x-Math.round(x))<1e-6)) return;
    // Check if all roots of den have modulus < lambda (spurious)
    // For quadratic: roots of x^2+bx+c have |r|^2 = c (if complex) or check individually
    console.log('Factor degree', d, ':', den, '→ quotient', q.map(x=>Math.round(x)));
  } else {
    for (let k=-10; k<=10; k++) search(d, [...prefix,k], remaining);
  }
}
for (let d=1; d<=Math.min(maxD,4); d++) search(d, [], coeffs);
```

**Interpreting `inter_result` before processing:**
| Condition | Meaning |
|---|---|
| `bits=0, checked=0` | IFS has non-exact coefficients — `custom_ifs` inapplicable |
| `bits>0, checked=0, completed=1` | Rational ran, only point contacts (dim(∂A) = 0) |
| `checked>0, oscDepth=0` | OSC holds, boundary dimension valid |
| `checked>0, oscDepth>0` | OSC violated — result meaningless |
| `completed=0` | Computation cut short — retry with larger `max_inters` |

**Known boundary dimensions for encyclopedia entries** (rational IFS):

| Entry | dim(∂A) | Polynomial |
|---|---|---|
| cap | 1.3684 | x²−4x+1=0 |
| gosper-island | 1.1292 | x−3=0 |
| heighway-dragon | 1.5236 | x³−x²−2=0 |
| jerusalem-cross | 1.0000 | polyhedral (straight edges) |
| koch-snowflake | 1.2619 | x−4=0 |
| levy-c-curve | 1.9340 | x⁹−3x⁸+3x⁷−3x⁶+2x⁵+4x⁴−8x³+8x²−16x+8=0 (degree-11 characteristic poly factors as (x²+2x+2)×degree-9; x²+2x+2 has roots −1±i giving dim=1) |
| menger-sponge | 1.8928 | x−8=0 (3D, boundary ∈ (1,3)) |
| pentadendrite | 1.0421 | x−3=0 |
| pentigree | 1.1415 | x−3=0 |

| rauzy-fractal | 1.0934 | x⁷+x⁶+x⁵−3x⁴−3x³−3x²+x+1=0 = (x³+x²+x−1)(x⁴−2x−1) → minimal: x⁴−2x−1=0 |
| shield-tiling | 1.0527 | x−2=0 |
| sierpinski-carpet | 1.0000 | polyhedral (straight edges) |
| tame-twin-dragon | 1.2108 | x⁵−x⁴+x³−x²−4=0 |
| twin-dragon | 1.5236 | x⁵−3x⁴+4x³−4x²+4x−4=0 = (x³−x²−2)(x²−2x+2) → minimal: x³−x²−2=0 (same as heighway-dragon) |
| ammann-a3, ammann-beenker, ammann-beenker-dual, cells-tiling, chair-tiling, danzer-7-fold, golden-trapezoid, octagonal, pinwheel-tiling, quaquaversal-tiling, robinson-triangles, sphinx, square-family, viper | 1.0000 | polyhedral (straight edges) |
| labyrinth | 1.0000 (dim) | curved boundary (dim=1 but not straight — infinite-sided polygon; `information("Subspaces")` gives `n=ambientDim` confirming non-linear pieces) |
| octahedron-fractal | 1.0000 | polyhedral (3D straight faces) |
| sierpinski-tetrahedron | 0 | point contacts only |
| cantor-dust | 0 | point contacts only |
| koch-curve | 0 | point contacts only (curve, not a tile) |
| antoines-necklace, barnsley-fern, chinese-lamp, jerusalem-cube | n/a | non-exact IFS (`bits=0`) |
| sierpinski-triangle, vicsek-fractal | n/a | decimal literals in AIFS — author's choice to use float mode; rewrite as `1/2`, `1/3` to enable exact arithmetic |

### Main-thread state (`IFSCanvas.astro` script)

```
_worker   : Worker | null          — singleton worker, created on first use
_pending  : Map<id, HTMLCanvasElement> — canvases currently being rendered
_done     : Set<id>                — canvases that finished rendering (never re-rendered)
```

### Worker state (`ifslib-worker.js`)

```
wasmModule : WebAssembly.Module | null  — compiled module, cached after first fetch
pending    : Map<id, {wasm, sizes, sizeIndex, width, height}>  — active render jobs
```

### Render flow

1. Canvas enters viewport (IntersectionObserver, rootMargin 200px) → `renderCanvas(canvas)` called.
2. Guard: skip if `_done.has(id)` or `_pending.has(id)` (already rendering).
3. `_pending.set(id, canvas)` **immediately** (before any `await`) — makes cancel visible.
4. HiDPI scaling: read `getBoundingClientRect()` for true CSS size, set `canvas.width/height` to physical pixels, lock `canvas.style.width/height` to CSS size (prevents aspect ratio distortion from CSS `max-width: 100%`).
5. Post `{ id, aifs, width, height, version }` to worker.
6. Worker: `await getWasmInstance(version)` → fresh instance → `init` → `ifs_select('','')` → add to `pending` Map → `runTick()`.
7. `runTick()`: round-robin — finds the lowest `sizeIndex` across all pending, renders one frame per canvas at that step, posts `{ type: 'frame', pixels, width, height }`, yields via `setTimeout(0)`, loops until `pending` is empty.
8. Main thread `onmessage`: for `frame` — draw only if `_pending.has(id)` (guards against stale frames after cancel). For `done` — move from `_pending` to `_done` **only if `_pending.has(id)`** (prevents marking a cancelled canvas as done).

### Cancel flow (canvas leaves viewport)

1. `cancelCanvas(canvas)`: `_pending.delete(id)` → post `{ id, type: 'cancel' }` to worker.
2. Worker `onmessage cancel`: `pending.delete(id)` — job is dropped from the round-robin.
3. **Race (cancel arrives during `await getWasmInstance`)**: the `await` may complete after the cancel. This is safe — the stale render writes to `pending` and runs to completion, but all its `frame`/`done` messages are silently dropped on the main thread (canvas no longer in `_pending`). The canvas stays in neither `_pending` nor `_done`, so it re-renders correctly when it re-enters the viewport.
4. **Do NOT use a `cancelled` Set** to guard inside the worker — it causes a broken re-render race: a new render request can see its own id in `cancelled` (left by the prior cancel), skip itself, and the canvas stays blank permanently.

### Cache busting

`__IFSLIB_VERSION__` is injected by Vite at build time from `astro.config.mjs`:
```js
vite: { define: { __IFSLIB_VERSION__: JSON.stringify('1.0.0') } }
```
Bump this string when replacing `ifslib.wasm`.

---

## Pages

| Route | File | Description |
|---|---|---|
| `/` | `src/pages/index.astro` | Landing page |
| `/ifs` | `src/pages/ifs/index.astro` | Catalog — tag filter + sort |
| `/ifs/[slug]` | `src/pages/ifs/[slug].astro` | Individual IFS entry |
| `/search` | `src/pages/search.astro` | Client-side full-text search |
| `/tools` | `src/pages/tools/index.astro` | Tools index |
| `/tools/ifstile` | `src/pages/tools/ifstile.astro` | IFStile tool |
| `/about` | `src/pages/about.astro` | About page |

Header nav order: Home | Catalog | Search | Tools | About

---

## Known Quirks & Gotchas

- **Dev server host**: Astro/Vite on Windows may bind to `[::1]` instead of `127.0.0.1`. The config has `server: { host: '127.0.0.1' }` to fix this.
- **Content store cache**: After changing `src/content.config.ts` schema, delete `.astro/` to clear the stale data store if entries fail to load. Also delete `.astro/` if a newly-created `.mdx` entry renders with `InvalidContentEntryDataError` (all required fields missing) — this means the cache stored an empty/stale entry for the new file. Symptom: build succeeds but dev-server render fails with schema validation errors for `name`, `description`, `transforms`, `aifs`. **Rule: always delete `.astro/` and restart the dev server after adding any new `.mdx` file.** The build (`npx astro build`) is not affected by this cache and can be used to verify pages work correctly.
- **MDX `export const` in content collections**: Use `export const` (not plain `const`) for variables that are referenced in JSX expressions within MDX content entries (`src/content/ifs/*.mdx`). Plain `const` is NOT accessible inside the compiled `_createMdxContent` function. Also: never delete an `.md` file and add an `.mdx` file with the same slug while the dev server is running — clear `.astro/` cache to avoid a duplicate-ID error.
- **`#` is a comment in AIFS**: Everything from `#` to end of line is ignored — including inside AIFS blocks fetched from GitHub (e.g. `Quaquaversal.aifs` has `# a^4=1` etc.). Never mistake commented-out lines for actual definitions when reading raw `.aifs` files.
- **AIFS must have `S=(...)*S`**: The most common error — `init` succeeds but `ifs_select` fails with "No valid root reference found" if the attractor line is missing. Call `get_last_output()` after any failure to retrieve the error message.
- **WASM has zero imports**: Instantiate with `WebAssembly.instantiate(buf, {})` — no WASI stubs needed.
- **Fresh WASM instance per render**: `ifslib` has one global `g_renderer` per instance — the worker creates a new instance for every render request (module is compiled once and cached; re-instantiation is cheap).
- **Never use a `cancelled` Set in the worker**: It creates a broken re-render race where a new render request sees its own id in `cancelled` (left by a prior cancel), skips itself, and the canvas stays black permanently. Let stale renders complete — they are silently dropped on the main thread (canvas not in `_pending`).
- **Astro v6 content config location**: Must be `src/content.config.ts`, not `src/content/config.ts`.
- **`$` inside LaTeX math in Markdown**: Never write `\$companion(...)` or `\$exchange()` inside `$...$` or `$$...$$` — remark-math breaks. Always move AIFS function names outside math delimiters into inline code: e.g. write `the matrix $s$ (defined as \`$companion([...])\` in AIFS)` instead of `$s = \$companion([...])$`.
