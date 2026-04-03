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
    ifs/                  # One .md file per IFS entry
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
- `slug?: string` — optional; when provided, renders an "Edit this page on GitHub" link pointing to `src/content/ifs/<slug>.md`

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

## Adding a New IFS Entry

Create `src/content/ifs/<slug>.md`. The slug is the filename without `.md` and becomes the URL at `/ifs/<slug>`.

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

### AIFS format (critical)

The `aifs` field is an IFStile DSL program. Key rules:
- Must start with `@` on its own line.
- `$dim=2` declares a 2D IFS.
- Each transform: `f<n>=[tx,ty]*[a,b,c,d]` where `[tx,ty]` is translation and `[a,b,c,d]` is the 2×2 matrix in row-major order.
- **The attractor line is mandatory**: `S=(f1|f2|...)*S` — without it `ifslib_init` returns 0 and nothing renders.
- The `aifs` YAML field uses a literal block scalar (`|`) to preserve newlines.

### Markdown body

Write freely in Markdown. Math is supported via LaTeX:
- Inline: `$f(x) = ax + b$`
- Block: `$$\begin{pmatrix}...\end{pmatrix}$$`

Use single `\` inside YAML (e.g. `\\frac`) and single `\` in Markdown body (rehype-katex handles both).

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
- **Content store cache**: After changing `src/content.config.ts` schema, delete `.astro/` to clear the stale data store if entries fail to load.
- **AIFS must have `S=(...)*S`**: The most common error — `ifslib_init` silently returns 0 if the attractor line is missing.
- **WASM has zero imports**: Instantiate with `WebAssembly.instantiate(buf, {})` — no WASI stubs needed.
- **Worker queue**: `ifslib` uses a single global `g_renderer`; never send concurrent render requests — the worker serializes them via a promise queue.
- **Astro v6 content config location**: Must be `src/content.config.ts`, not `src/content/config.ts`.
