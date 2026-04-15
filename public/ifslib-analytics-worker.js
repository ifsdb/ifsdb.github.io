'use strict';

// Analytics worker — runs information() queries and boundary dimension computation on demand.
// One fresh WASM instance per request (stateless, no queue needed).
// Main thread can terminate() this worker at any time without cleanup issues.

let wasmModule = null;

async function getWasm(version) {
  if (!wasmModule) {
    const resp = await fetch('/ifslib.wasm?v=' + version);
    if (!resp.ok) throw new Error('Failed to load ifslib.wasm: ' + resp.status);
    wasmModule = await WebAssembly.compile(await resp.arrayBuffer());
  }
  // Fresh instance — avoids any shared state between requests.
  const inst = await WebAssembly.instantiate(wasmModule, {});
  inst.exports._initialize();
  return inst.exports;
}

function writeCStr(w, s) {
  const b = new TextEncoder().encode(s + '\0');
  const p = w.malloc(b.length);
  new Uint8Array(w.memory.buffer).set(b, p);
  return p;
}

function readCStr(w, p) {
  if (!p) return '';
  const m = new Uint8Array(w.memory.buffer);
  let e = p; while (m[e]) e++;
  return new TextDecoder().decode(m.subarray(p, e));
}

function getOutput(w) { return readCStr(w, w.get_last_output()); }

// Attempts to compute dim(∂A) with the given max_inters budget.
// Returns { dim } on success, { incomplete: true } if budget was exceeded,
// or { error: string } on failure (non-exact IFS, OSC violated, etc.).
// dim === 0  means 0-dimensional boundary (tiles touch at isolated points).
// dim === -1 means tiles are completely disjoint (no contacts at all).
function tryCalcBoundaryDim(w, maxInters) {
  const settingsPtr = w.malloc(20);
  const iresPtr     = w.malloc(20);
  {
    const dv = new DataView(w.memory.buffer);
    dv.setUint32  (settingsPtr +  0, maxInters,   true); // max_inters
    dv.setUint32  (settingsPtr +  4, 0xFFFFFFFF,  true); // max_depth (no limit)
    dv.setUint32  (settingsPtr +  8, 63,          true); // max_bits
    dv.setFloat32 (settingsPtr + 12, 0.0,         true); // prec (exact rational)
    dv.setUint8   (settingsPtr + 16, 0);                 // mode_ori
    dv.setUint8   (settingsPtr + 17, 1);                 // stop_on_overlap
    dv.setUint8   (settingsPtr + 18, 1);                 // stop_on_incomplete
    dv.setUint8   (settingsPtr + 19, 0);                 // padding
  }

  const ok = w.calc_neighbor_graph(iresPtr, settingsPtr);
  w.free(settingsPtr);

  if (!ok) {
    const msg = getOutput(w);
    w.free(iresPtr);
    return { error: msg || 'calc_neighbor_graph failed' };
  }

  const dv = new DataView(w.memory.buffer);
  const bits      = dv.getUint32(iresPtr +  8, true); // m_bits
  const oscDepth  = dv.getUint32(iresPtr + 12, true); // m_over_depth
  const completed = dv.getUint8 (iresPtr + 16);       // m_completed
  w.free(iresPtr);

  if (bits === 0)      return { error: 'non-exact IFS (sin/cos or decimal literals)' };
  if (oscDepth > 0)    return { error: 'OSC violated at depth ' + oscDepth };
  if (!completed)      return { incomplete: true };

  const dim = w.calc_boundary_dim();
  if (isNaN(dim))      return { error: 'calc_boundary_dim failed: ' + getOutput(w) };
  return { dim };
}

self.onmessage = async function ({ data }) {
  const { id, aifs, block, root, request, version } = data;
  try {
    const w = await getWasm(version);

    const aifsPtr = writeCStr(w, aifs);
    const initOk = w.init(aifsPtr);
    w.free(aifsPtr);
    if (!initOk) {
      self.postMessage({ id, type: 'error', request, message: 'init failed: ' + getOutput(w) });
      return;
    }

    const bPtr = block ? writeCStr(w, block) : 0;
    const selOk = w.set_block(bPtr);
    if (bPtr) w.free(bPtr);
    if (!selOk) {
      self.postMessage({ id, type: 'error', request, message: 'set_block failed: ' + getOutput(w) });
      return;
    }
    if (root) {
      const rPtr = writeCStr(w, root);
      const rootOk = w.set_root(rPtr);
      w.free(rPtr);
      if (!rootOk) {
        self.postMessage({ id, type: 'error', request, message: 'set_root failed: ' + getOutput(w) });
        return;
      }
    }

    if (request === 'BoundaryDim') {
      // Tiered budget: retry with larger max_inters if computation is incomplete.
      for (const budget of [8000, 50000, 200000]) {
        const r = tryCalcBoundaryDim(w, budget);
        if (r.error) {
          self.postMessage({ id, type: 'error', request, message: r.error });
          return;
        }
        if (!r.incomplete) {
          self.postMessage({ id, type: 'result', request, data: r.dim });
          return;
        }
      }
      self.postMessage({ id, type: 'error', request, message: 'budget exceeded (maxInters=200000)' });
      return;
    }

    const infPtr = writeCStr(w, request);
    w.information(infPtr);
    w.free(infPtr);
    self.postMessage({ id, type: 'result', request, data: getOutput(w) });
  } catch (err) {
    self.postMessage({ id, type: 'error', request, message: String(err) });
  }
};
