'use strict';

// ifslib_init does not reset WASM global state between calls, so each render
// request requires a fresh instance. We cache the compiled module so that
// re-instantiation is cheap (no re-compilation overhead).
let wasmModule = null;

async function getWasmInstance(version) {
  if (!wasmModule) {
    const resp = await fetch('/ifslib.wasm?v=' + version);
    if (!resp.ok) throw new Error('Failed to load ifslib.wasm: ' + resp.status);
    const buf = await resp.arrayBuffer();
    wasmModule = await WebAssembly.compile(buf);
  }
  // Fresh instance every time — guarantees clean renderer state.
  const instance = await WebAssembly.instantiate(wasmModule, {});
  if (typeof instance.exports._initialize === 'function') {
    instance.exports._initialize();
  }
  return instance.exports;
}

function writeCString(wasm, str) {
  const bytes = new TextEncoder().encode(str + '\0');
  const ptr = wasm.malloc(bytes.length);
  if (!ptr) throw new Error('malloc returned null');
  new Uint8Array(wasm.memory.buffer).set(bytes, ptr);
  return ptr;
}

// Returns list of render sizes from 32 up to maxDim.
function progressiveSizes(width, height) {
  const maxDim = Math.max(width, height);
  const sizes = [];
  let s = 32;
  while (s < maxDim) {
    sizes.push(s);
    s *= 2;
  }
  sizes.push(maxDim);
  return sizes;
}

// Interleaved rendering: all pending requests advance one size-step at a time,
// so canvas 1 and canvas 2 both show a 32px preview before either reaches 64px.
//
// Each WASM instance is independent (own g_renderer), so we can render one frame
// from each instance per tick without interference.

// id -> { wasm, sizes, sizeIndex, width, height }
const pending = new Map();
let tickRunning = false;

self.onmessage = async function (e) {
  const { id, type, aifs, width, height, version } = e.data;

  if (type === 'cancel') {
    pending.delete(id);
    return;
  }

  try {
    const wasm = await getWasmInstance(version);
    const ptr = writeCString(wasm, aifs);
    const ok = wasm.ifslib_init(ptr);
    wasm.free(ptr);
    if (!ok) {
      self.postMessage({ id, type: 'error', message: 'ifslib_init failed' });
      return;
    }
    // Overwrite any stale entry for this id (e.g. re-render after cancel).
    pending.set(id, { wasm, sizes: progressiveSizes(width, height), sizeIndex: 0, width, height });
    if (!tickRunning) runTick();
  } catch (err) {
    self.postMessage({ id, type: 'error', message: String(err) });
  }
};

async function runTick() {
  tickRunning = true;
  while (pending.size > 0) {
    // Find the lowest size-step currently in progress across all pending requests.
    let minStep = Infinity;
    for (const req of pending.values()) minStep = Math.min(minStep, req.sizeIndex);

    // Render one frame for every request that is at the lowest step.
    for (const [id, req] of pending) {
      if (req.sizeIndex !== minStep) continue;
      const s = req.sizes[req.sizeIndex];
      const maxDim = Math.max(req.width, req.height);
      const rw = Math.max(1, Math.round(req.width  * s / maxDim));
      const rh = Math.max(1, Math.round(req.height * s / maxDim));
      const pixPtr = req.wasm.ifslib_render(rw, rh, 1.0, 1.0);
      if (!pixPtr) {
        self.postMessage({ id, type: 'error', message: 'ifslib_render failed at size ' + s });
        pending.delete(id);
        continue;
      }
      const pixels = new Uint8ClampedArray(
        req.wasm.memory.buffer.slice(pixPtr, pixPtr + rw * rh * 4)
      );
      self.postMessage({ id, type: 'frame', pixels, width: rw, height: rh }, [pixels.buffer]);
      req.sizeIndex++;
      if (req.sizeIndex >= req.sizes.length) {
        self.postMessage({ id, type: 'done' });
        pending.delete(id);
      }
    }

    // Yield to the event loop so new onmessage calls can add to pending.
    await new Promise(resolve => setTimeout(resolve, 0));
  }
  tickRunning = false;
}
