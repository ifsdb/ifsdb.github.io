"""
Parse the bronze-mean patch PDF to extract polygon path data.
The PDF page is 2573x2600 points. All tile shapes are filled polygons.
We look for color-setting commands followed by path commands.
"""
import re, zlib

path = "C:/ifsdb.github.io/public/bronze-mean-patch.pdf"
with open(path, 'rb') as f:
    data = f.read()

# --- Find all obj ... endobj blocks ---
obj_blocks = {}
for m in re.finditer(rb'(\d+) 0 obj\b', data):
    obj_num = int(m.group(1))
    start = m.start()
    end_m = re.search(rb'endobj', data[start:])
    if end_m:
        obj_blocks[obj_num] = data[start:start+end_m.end()]

print(f"Found objects: {sorted(obj_blocks.keys())}")

# --- Decompress each stream ---
def try_decompress(raw):
    try:
        return zlib.decompress(raw)
    except:
        pass
    try:
        return zlib.decompress(raw, -zlib.MAX_WBITS)
    except:
        pass
    return None

for obj_num, block in sorted(obj_blocks.items()):
    sm = re.search(rb'stream\r?\n', block)
    em = re.search(rb'\r?\nendstream', block)
    if sm and em:
        raw_stream = block[sm.end():em.start()]
        if b'FlateDecode' in block:
            dec = try_decompress(raw_stream)
            if dec:
                print(f"\n=== Object {obj_num} stream ({len(raw_stream)} -> {len(dec)} bytes) ===")
                # Show first portion
                txt = dec.decode('latin-1', errors='replace')
                print(txt[:3000])
                print(f"... [{len(txt)} total chars]")
                # Save full decoded content
                with open(f"C:/ifsdb.github.io/pdf_stream_{obj_num}.txt", 'w', encoding='utf-8') as f:
                    f.write(txt)
                print(f"Saved to pdf_stream_{obj_num}.txt")
