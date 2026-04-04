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
**Mandatory**: without an attractor equation `ifslib_init` returns 0 and nothing renders.

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

- **`IFSCanvas.astro`** — Astro component. Accepts `id`, `aifs`, `width`, `height`, `label` props. Embeds AIFS as `data-aifs` on the `<canvas>`. The `<script>` block creates a shared `Worker('/ifslib-worker.js')` and posts render requests to it.

- **`public/ifslib-worker.js`** — Web Worker. Owns the singleton WASM instance. Serializes all requests via a promise queue (required because `ifslib` has a single global renderer). For each request renders progressively at sizes `[32, 64, 128, ..., maxDim]`, posting each frame as a transferable `Uint8ClampedArray`.

- **`public/ifslib.wasm`** — Built from [github.com/mekhontsev/ifstile](https://github.com/mekhontsev/ifstile) (`SrcLib/ifslib.cpp`). Pure WASI reactor (no imports). Exports:
  - `_initialize()` — must be called once after instantiation
  - `ifslib_init(ptr: i32) → i32` — pass null-terminated AIFS string; returns 1 on success, 0 on failure
  - `ifslib_render(w: i32, h: i32, quality: f32, thickness: f32) → i32` — returns pointer to RGBA pixel buffer
  - `malloc(n: i32) → i32`, `free(ptr: i32)`
  - `memory` — the linear memory

### Render flow

1. `IFSCanvas.astro` script calls `getWorker().postMessage({ id, aifs, width, height, version })`.
2. Worker calls `ifslib_init(aifs)`, then loops over `progressiveSizes(width, height)`.
3. Each step posts `{ type: 'frame', pixels: Uint8ClampedArray, width: rw, height: rh }`.
4. Main thread draws via `createImageBitmap` + `ctx.drawImage` scaled to canvas size.
5. Worker posts `{ type: 'done' }` when all frames are sent.

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
- **Content store cache**: After changing `src/content.config.ts` schema, delete `.astro/` to clear the stale data store if entries fail to load. Also delete `.astro/` if a newly-created `.mdx` entry renders with `InvalidContentEntryDataError` (all required fields missing) — this means the cache stored an empty/stale entry for the new file. Symptom: build succeeds but dev-server render fails with schema validation errors for `name`, `description`, `transforms`, `aifs`.
- **MDX `export const` in content collections**: Use `export const` (not plain `const`) for variables that are referenced in JSX expressions within MDX content entries (`src/content/ifs/*.mdx`). Plain `const` is NOT accessible inside the compiled `_createMdxContent` function. Also: never delete an `.md` file and add an `.mdx` file with the same slug while the dev server is running — clear `.astro/` cache to avoid a duplicate-ID error.
- **AIFS must have `S=(...)*S`**: The most common error — `ifslib_init` silently returns 0 if the attractor line is missing.
- **WASM has zero imports**: Instantiate with `WebAssembly.instantiate(buf, {})` — no WASI stubs needed.
- **Worker queue**: `ifslib` uses a single global `g_renderer`; never send concurrent render requests — the worker serializes them via a promise queue.
- **Astro v6 content config location**: Must be `src/content.config.ts`, not `src/content/config.ts`.
- **`$` inside LaTeX math in Markdown**: Never write `\$companion(...)` or `\$exchange()` inside `$...$` or `$$...$$` — remark-math breaks. Always move AIFS function names outside math delimiters into inline code: e.g. write `the matrix $s$ (defined as \`$companion([...])\` in AIFS)` instead of `$s = \$companion([...])$`.
