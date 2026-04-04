import { readFileSync } from 'fs';
const buf = readFileSync('public/ifslib.wasm');
const mod = await WebAssembly.compile(buf);
const exports_ = WebAssembly.Module.exports(mod);
console.log('Exports:', exports_.map(e=>e.kind+':'+e.name).join(', '));

const inst = await WebAssembly.instantiate(mod, {});
const ex = inst.exports;
ex._initialize();

function writeStr(wasm, s) {
  const b = Buffer.from(s + '\x00', 'utf8');
  const ptr = wasm.malloc(b.length);
  new Uint8Array(wasm.memory.buffer).set(b, ptr);
  return ptr;
}

const aifs1 = '@\n$dim=2\nf1=[0.5,0,0,0.5]\nf2=[0.5,0]*[0.5,0,0,0.5]\nf3=[0.25,0.5]*[0.5,0,0,0.5]\nS=(f1|f2|f3)*S';
let p = writeStr(ex, aifs1);
let ok = ex.ifslib_init(p);
ex.free(p);
console.log('Sierpinski init:', ok);
const px1 = ex.ifslib_render(16, 16, 1.0, 1.0);
const d1 = new Uint8Array(ex.memory.buffer.slice(px1, px1 + 16*16*4));
console.log('Sierpinski sum:', d1.reduce((a,b)=>a+b,0));

const aifs2 = '@\n$dim=2\nf1=[0,0,0,0.16]\nf2=[0,1.6]*[0.85,0.04,-0.04,0.85]\nf3=[0,1.6]*[0.2,-0.26,0.23,0.22]\nf4=[0,0.44]*[-0.15,0.28,0.26,0.24]\nS=(f1|f2|f3|f4)*S';
p = writeStr(ex, aifs2);
ok = ex.ifslib_init(p);
ex.free(p);
console.log('Barnsley init:', ok);
const px2 = ex.ifslib_render(16, 16, 1.0, 1.0);
const d2 = new Uint8Array(ex.memory.buffer.slice(px2, px2 + 16*16*4));
console.log('Barnsley sum:', d2.reduce((a,b)=>a+b,0));
console.log('Same output?', d1.every((v,i)=>v===d2[i]));
