"""
Parse bronze-mean PDF stream to extract all tile polygons grouped by color.
Find unique tile shapes (the substitution prototiles).
"""
import re, math, collections

# Read the decoded stream
with open("C:/ifsdb.github.io/pdf_stream_6.txt", encoding='utf-8') as f:
    txt = f.read()

print(f"Stream length: {len(txt)} chars")

# Parse PDF drawing commands
# Commands: rg (set RGB fill), m (moveto), l (lineto), h (closepath), f* (eofill)
# Pattern: sequence of numbers followed by command

# Split into tokens
tokens = txt.split()
print(f"Total tokens: {len(tokens)}")

# State machine parser
polygons_by_color = collections.defaultdict(list)
current_color = None
current_path = []
i = 0
n = len(tokens)

def try_float(s):
    try: return float(s)
    except: return None

polygon_count = 0
color_changes = 0

while i < n:
    tok = tokens[i]
    
    # Color command: x y z rg
    if tok == 'rg':
        r = try_float(tokens[i-3]) if i >= 3 else None
        g_ = try_float(tokens[i-2]) if i >= 2 else None
        b = try_float(tokens[i-1]) if i >= 1 else None
        if r is not None:
            # Round to 3 decimal places to match
            current_color = (round(r,3), round(g_,3), round(b,3))
            color_changes += 1
        current_path = []
    
    # moveto: x y m
    elif tok == 'm':
        x = try_float(tokens[i-2]) if i >= 2 else None
        y = try_float(tokens[i-1]) if i >= 1 else None
        if x is not None:
            current_path = [(x, y)]
    
    # lineto: x y l
    elif tok == 'l':
        x = try_float(tokens[i-2]) if i >= 2 else None
        y = try_float(tokens[i-1]) if i >= 1 else None
        if x is not None and current_path:
            current_path.append((x, y))
    
    # fill (end of path)
    elif tok in ('f', 'f*', 'F', 'B', 'b'):
        if current_path and current_color:
            polygons_by_color[current_color].append(list(current_path))
            polygon_count += 1
        current_path = []
    
    i += 1

print(f"\nColor changes: {color_changes}")
print(f"Total polygons: {polygon_count}")
print(f"\nColors found:")
for color, polys in sorted(polygons_by_color.items(), key=lambda x: -len(x[1])):
    sizes = collections.Counter(len(p) for p in polys)
    r8,g8,b8 = int(color[0]*255), int(color[1]*255), int(color[2]*255)
    print(f"  RGB({r8},{g8},{b8})  {len(polys)} polygons  vertex-counts: {dict(sizes)}")

# Identify the 3 colors
# RED ≈ (225, 49, 91) → (0.882, 0.192, 0.357)
# BLUE ≈ (0, 141, 203) → (0.0, 0.553, 0.796)
# YELLOW ≈ (255, 236, 92) → (1.0, 0.925, 0.361)
colors_named = {}
for color in polygons_by_color:
    r8,g8,b8 = color[0]*255, color[1]*255, color[2]*255
    if r8 > 180 and g8 < 100:
        colors_named['red'] = color
    elif r8 < 50 and g8 > 100 and b8 > 150:
        colors_named['blue'] = color
    elif r8 > 200 and g8 > 180 and b8 < 150:
        colors_named['yellow'] = color

print(f"\nIdentified: {colors_named}")

# Analyze each color's polygon shapes
def edge_lengths(poly):
    n = len(poly)
    lengths = []
    for i in range(n):
        dx = poly[(i+1)%n][0] - poly[i][0]
        dy = poly[(i+1)%n][1] - poly[i][1]
        lengths.append(math.hypot(dx, dy))
    return sorted(lengths)

def poly_area(poly):
    n = len(poly)
    area = 0
    for i in range(n):
        x1,y1 = poly[i]
        x2,y2 = poly[(i+1)%n]
        area += x1*y2 - x2*y1
    return abs(area)/2

print("\n=== UNIQUE TILE SHAPES (by edge-length signature) ===\n")
for name, color in colors_named.items():
    polys = polygons_by_color[color]
    print(f"{name.upper()} ({len(polys)} tiles):")
    
    # Find unique shapes by rounded edge-length sig
    shape_sigs = collections.defaultdict(list)
    for p in polys:
        el = edge_lengths(p)
        sig = tuple(round(e, 0) for e in el)
        shape_sigs[sig].append(p)
    
    for sig, ps in sorted(shape_sigs.items(), key=lambda x: -len(x[1])):
        p0 = ps[0]
        area = poly_area(p0)
        exact_el = edge_lengths(p0)
        print(f"  Shape {sig}: {len(ps)} instances, area={area:.2f}")
        print(f"    vertices: {p0}")
        print(f"    edge_lengths: {[f'{e:.4f}' for e in exact_el]}")
    print()

# Summary statistics
print("\n=== RAW EDGE LENGTH STATISTICS ===\n")
all_edges = []
for name, color in colors_named.items():
    for p in polygons_by_color[color]:
        all_edges.extend(edge_lengths(p))

# Find clusters of edge lengths
all_edges_sorted = sorted(set(round(e, 1) for e in all_edges))
# Group close values
from itertools import groupby
groups = []
current_group = [all_edges_sorted[0]]
for e in all_edges_sorted[1:]:
    if e - current_group[-1] < 2:
        current_group.append(e)
    else:
        groups.append(current_group)
        current_group = [e]
groups.append(current_group)

print("Edge length groups:")
for g in groups:
    center = sum(g)/len(g)
    print(f"  ~{center:.1f} pts: {g[:5]}")

# Show a couple of YELLOW polygons
if 'yellow' in colors_named:
    ypoly = polygons_by_color[colors_named['yellow']]
    print(f"\nYELLOW sample polygon 0: {ypoly[0]}")
    print(f"YELLOW sample polygon 1: {ypoly[1] if len(ypoly)>1 else 'N/A'}")
