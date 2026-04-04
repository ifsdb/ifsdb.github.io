"""
Better PDF parser - handle 're' (rectangle) and proper path accumulation.
Find the YELLOW tile geometry.
"""
import re, math, collections

with open("C:/ifsdb.github.io/pdf_stream_6.txt", encoding='utf-8') as f:
    txt = f.read()

tokens = txt.split()
n = len(tokens)
i = 0

def try_float(s):
    try: return float(s)
    except: return None

# Look for what commands appear near the yellow color
# Find position of first '1 0.922 0.361 rg' or similar yellow color
# Find yellow color token position
yellow_cmd_pos = None
for j, tok in enumerate(tokens):
    if tok == 'rg':
        r = try_float(tokens[j-3]) if j >= 3 else None
        g_ = try_float(tokens[j-2]) if j >= 2 else None
        b = try_float(tokens[j-1]) if j >= 1 else None
        if r and r > 0.9 and g_ and g_ > 0.8 and b and b < 0.5:
            yellow_cmd_pos = j
            print(f"Yellow color at token {j}: {tokens[j-3:j+2]}")
            break

if yellow_cmd_pos:
    # Show next 100 tokens after yellow color
    snippet = tokens[yellow_cmd_pos:yellow_cmd_pos+100]
    print("\nTokens after yellow color command:")
    for k, tok in enumerate(snippet):
        print(f"  [{yellow_cmd_pos+k}] {tok}")

# ---------------------------------------------------------------
# Rewrite parser to handle 're' (rectangle) and 'h' (closepath)
# ---------------------------------------------------------------
print("\n=== REPARSING WITH 're' SUPPORT ===\n")

polygons_by_color = collections.defaultdict(list)
current_color = None
current_path = []
num_buf = []  # buffer for numeric args

def flush_nums(n_required):
    """Return last n_required numbers from buffer"""
    if len(num_buf) >= n_required:
        return [num_buf[-n_required+k] for k in range(n_required)]
    return None

i = 0
num_buf = []
while i < n:
    tok = tokens[i]
    f = try_float(tok)
    if f is not None:
        num_buf.append(f)
        i += 1
        continue
    
    # Commands
    if tok == 'rg':
        if len(num_buf) >= 3:
            r, g_, b = num_buf[-3], num_buf[-2], num_buf[-1]
            current_color = (round(r,3), round(g_,3), round(b,3))
            current_path = []
        num_buf = []
    
    elif tok == 'm':
        if len(num_buf) >= 2:
            x, y = num_buf[-2], num_buf[-1]
            current_path = [(x, y)]
        num_buf = []
    
    elif tok == 'l':
        if len(num_buf) >= 2 and current_path:
            x, y = num_buf[-2], num_buf[-1]
            current_path.append((x, y))
        num_buf = []
    
    elif tok == 're':
        # Rectangle: x y w h re
        if len(num_buf) >= 4:
            x, y, w, h = num_buf[-4], num_buf[-3], num_buf[-2], num_buf[-1]
            current_path = [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
        num_buf = []
    
    elif tok == 'h':
        # Close path (implicitly closes back to start; path already closed)
        num_buf = []
    
    elif tok in ('f', 'f*', 'F', 'B', 'b'):
        if current_path and len(current_path) >= 3 and current_color:
            polygons_by_color[current_color].append(list(current_path))
        elif current_path and len(current_path) >= 3:
            print(f"WARNING: path without color: {current_path[:2]}")
        current_path = []
        num_buf = []
    
    elif tok in ('q', 'Q', 'cm', 'cs', 'cs', 'gs', 'Do', 'W', 'n', 'S', 'w', 'J', 'j', 'M', 'd', 'ri', 'i', 'gs'):
        num_buf = []
    
    else:
        num_buf = []
    
    i += 1

print(f"Colors found:")
for color, polys in sorted(polygons_by_color.items(), key=lambda x: -len(x[1])):
    sizes = collections.Counter(len(p) for p in polys)
    r8,g8,b8 = int(color[0]*255), int(color[1]*255), int(color[2]*255)
    print(f"  RGB({r8},{g8},{b8})  {len(polys)} polygons  vertex-counts: {dict(sizes)}")

# Find yellow
colors_named = {}
for color in polygons_by_color:
    r8,g8,b8 = color[0]*255, color[1]*255, color[2]*255
    if r8 > 180 and g8 < 120 and b8 < 150 and r8 > g8:
        colors_named['red'] = color
    elif r8 < 50 and g8 > 100:
        colors_named['blue'] = color
    elif r8 > 200 and g8 > 180 and b8 < 150:
        colors_named['yellow'] = color

print(f"\nIdentified: {colors_named}")

def poly_area(poly):
    n = len(poly)
    area = 0
    for j in range(n):
        x1,y1 = poly[j]; x2,y2 = poly[(j+1)%n]
        area += x1*y2 - x2*y1
    return abs(area)/2

def edge_lens(poly):
    n = len(poly)
    return [math.hypot(poly[(j+1)%n][0]-poly[j][0], poly[(j+1)%n][1]-poly[j][1]) for j in range(n)]

# Show first few of each type
for name in ['red','blue','yellow']:
    if name not in colors_named: continue
    color = colors_named[name]
    polys = polygons_by_color[color]
    print(f"\n{name.upper()} — first 3 polygons:")
    for p in polys[:3]:
        el = edge_lens(p)
        area = poly_area(p)
        print(f"  vertices={p}")
        print(f"  edge_lengths={[f'{e:.4f}' for e in el]}")
        print(f"  area={area:.4f}")

# Compute exact side lengths
print("\n=== EXACT SIDE ANALYSIS ===\n")
for name in ['red','blue','yellow']:
    if name not in colors_named: continue
    color = colors_named[name]
    polys = polygons_by_color[color]
    all_el = []
    for p in polys:
        all_el.extend(edge_lens(p))
    distinct = sorted(set(round(e,3) for e in all_el if e > 0.1))
    print(f"{name.upper()} distinct edge lengths (rounded to 0.001): {distinct[:20]}")
    areas = [poly_area(p) for p in polys[:5]]
    print(f"  first 5 areas: {[f'{a:.4f}' for a in areas]}")
