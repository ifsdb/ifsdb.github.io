'use strict';

// Analytics worker — runs information() queries on demand.
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

    const infPtr = writeCStr(w, request);
    w.information(infPtr);
    w.free(infPtr);
    self.postMessage({ id, type: 'result', request, data: getOutput(w) });
  } catch (err) {
    self.postMessage({ id, type: 'error', request, message: String(err) });
  }
};
