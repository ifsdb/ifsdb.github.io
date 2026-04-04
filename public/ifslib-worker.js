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

// Returns list of render sizes from ~1/8 up to maxDim, then exact target.
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

// Single sequential queue — WASM g_renderer is global state, only one render at a time.
let queue = Promise.resolve();

self.onmessage = function (e) {
  const msg = e.data;
  queue = queue
    .then(() => handleRequest(msg))
    .catch(err => {
      self.postMessage({ id: msg.id, type: 'error', message: String(err) });
    });
};

async function handleRequest({ id, aifs, width, height, version }) {
  const wasm = await getWasmInstance(version);

  const ptr = writeCString(wasm, aifs);
  const ok = wasm.ifslib_init(ptr);
  wasm.free(ptr);

  if (!ok) {
    self.postMessage({ id, type: 'error', message: 'ifslib_init failed' });
    return;
  }

  const maxDim = Math.max(width, height);
  for (const s of progressiveSizes(width, height)) {
    const rw = Math.max(1, Math.round(width * s / maxDim));
    const rh = Math.max(1, Math.round(height * s / maxDim));

    const pixPtr = wasm.ifslib_render(rw, rh, 1.0, 1.0);
    if (!pixPtr) {
      self.postMessage({ id, type: 'error', message: 'ifslib_render failed at size ' + s });
      return;
    }

    // slice() copies the data before the next WASM call can overwrite it
    const pixels = new Uint8ClampedArray(
      wasm.memory.buffer.slice(pixPtr, pixPtr + rw * rh * 4)
    );
    // Transfer the buffer to avoid copying on the message boundary
    self.postMessage({ id, type: 'frame', pixels, width: rw, height: rh }, [pixels.buffer]);
  }

  self.postMessage({ id, type: 'done' });
}
