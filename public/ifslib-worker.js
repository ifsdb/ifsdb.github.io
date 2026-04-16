'use strict';

// Each render request requires a fresh WASM instance because ifslib uses
// a single global renderer per instance. We cache the compiled module so
// that re-instantiation is cheap (no re-compilation overhead).
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

function readCString(wasm, ptr) {
  if (!ptr) return '';
  const mem = new Uint8Array(wasm.memory.buffer);
  let end = ptr;
  while (mem[end] !== 0) end++;
  return new TextDecoder().decode(mem.subarray(ptr, end));
}

function getLastOutput(wasm) {
  if (typeof wasm.get_last_output !== 'function') return '';
  return readCString(wasm, wasm.get_last_output());
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
  const { id, type, aifs, block, root, camera, width, height, version, priority, startSizeIndex } = e.data;

  if (type === 'cancel') {
    pending.delete(id);
    return;
  }

  if (type === 'priority') {
    const req = pending.get(id);
    if (req) req.priority = priority;
    return;
  }

  try {
    const wasm = await getWasmInstance(version);
    const ptr = writeCString(wasm, aifs);
    const ok = wasm.init(ptr);
    wasm.free(ptr);
    if (!ok) {
      const output = getLastOutput(wasm);
      self.postMessage({ id, type: 'error', message: 'init failed' + (output ? ': ' + output : '') });
      return;
    }
    // Select block: resolve name → index via get_block_idx, then set_block(idx).
    // Pass -1 to set_block for default (first non-hidden) block.
    let blkIdx = -1;
    if (block) {
      const blkPtr = writeCString(wasm, block);
      blkIdx = wasm.get_block_idx(blkPtr);
      wasm.free(blkPtr);
    }
    const selOk = wasm.set_block(blkIdx);
    if (!selOk) {
      const output = getLastOutput(wasm);
      self.postMessage({ id, type: 'error', message: 'set_block failed' + (output ? ': ' + output : '') });
      return;
    }
    // Override root variable if specified.
    if (root) {
      const rootPtr = writeCString(wasm, root);
      const rootOk = wasm.set_root(rootPtr);
      wasm.free(rootPtr);
      if (!rootOk) {
        const output = getLastOutput(wasm);
        self.postMessage({ id, type: 'error', message: 'set_root failed' + (output ? ': ' + output : '') });
        return;
      }
    }
    // Apply camera override if provided (requires ifslib with set_camera export).
    if (camera && Array.isArray(camera) && (camera.length === 4 || camera.length === 10)) {
      if (typeof wasm.set_camera === 'function') {
        const camPtr = wasm.malloc(camera.length * 8);
        const dv = new DataView(wasm.memory.buffer);
        for (let i = 0; i < camera.length; i++) dv.setFloat64(camPtr + i * 8, camera[i], true);
        const camOk = wasm.set_camera(camPtr, camera.length);
        wasm.free(camPtr);
        if (!camOk) {
          const output = getLastOutput(wasm);
          self.postMessage({ id, type: 'error', message: 'set_camera failed' + (output ? ': ' + output : '') });
          return;
        }
      }
      // If set_camera is not exported by this ifslib build, silently skip — renders with auto-fit camera.
    }
    // Overwrite any stale entry for this id (e.g. re-render after cancel).
    const sizes = progressiveSizes(width, height);
    const resumeAt = Math.min(startSizeIndex ?? 0, sizes.length - 1);
    pending.set(id, { wasm, sizes, sizeIndex: resumeAt, width, height, priority: priority ?? false });
    if (!tickRunning) runTick();
  } catch (err) {
    self.postMessage({ id, type: 'error', message: String(err) });
  }
};

async function runTick() {
  tickRunning = true;
  while (pending.size > 0) {
    // Priority canvases (visible on screen) advance first.
    // If any priority canvas is pending, non-priority canvases wait.
    const hasPriority = [...pending.values()].some(r => r.priority);

    // Pick exactly ONE canvas to render this tick: priority first, then lowest sizeIndex.
    // Yielding after every single render lets cancel/new-request messages be processed
    // between frames — so a slow final-step render doesn't block new canvases.
    let chosenId = null;
    let chosenReq = null;
    let chosenStep = Infinity;
    for (const [id, req] of pending) {
      if (hasPriority && !req.priority) continue;
      if (req.sizeIndex < chosenStep) {
        chosenStep = req.sizeIndex;
        chosenId = id;
        chosenReq = req;
      }
    }

    if (chosenReq) {
      const req = chosenReq;
      const id = chosenId;
      const s = req.sizes[req.sizeIndex];
      const maxDim = Math.max(req.width, req.height);
      const rw = Math.max(1, Math.round(req.width  * s / maxDim));
      const rh = Math.max(1, Math.round(req.height * s / maxDim));
      const isFinal = req.sizeIndex === req.sizes.length - 1;
      const quality = isFinal ? 2.0 : 1.0;
      const pixPtr = req.wasm.render(rw, rh, quality, 1.0);
      if (!pixPtr) {
        const output = getLastOutput(req.wasm);
        self.postMessage({ id, type: 'error', message: 'render failed at size ' + s + (output ? ': ' + output : '') });
        pending.delete(id);
      } else {
        const pixels = new Uint8ClampedArray(
          req.wasm.memory.buffer.slice(pixPtr, pixPtr + rw * rh * 4)
        );
        self.postMessage({ id, type: 'frame', pixels, width: rw, height: rh, sizeIndex: req.sizeIndex }, [pixels.buffer]);
        req.sizeIndex++;
        if (req.sizeIndex >= req.sizes.length) {
          self.postMessage({ id, type: 'done' });
          pending.delete(id);
        }
      }
    }

    // Yield after every single render so cancel/new messages are processed immediately.
    await new Promise(resolve => setTimeout(resolve, 0));
  }
  tickRunning = false;
}
