from PIL import Image
import numpy as np
from scipy import ndimage, spatial

img = Image.open('C:/ifsdb.github.io/public/bronze-mean-rule.png')
arr = np.array(img)
R,G,B,A = [arr[:,:,i].astype(float) for i in range(4)]
H, W = arr.shape[:2]

red_mask    = (A > 200) & (R > 180) & (G < 100) & (B < 150)
blue_mask   = (A > 200) & (R < 80)  & (G > 100) & (B > 150)
yellow_mask = (A > 200) & (R > 200) & (G > 180) & (B < 150)

# Black outline pixels: opaque, R~G~B~0
outline = (A > 200) & (R < 40) & (G < 40) & (B < 40)
print(f"Black outline pixels: {outline.sum()}")

# Create color map: 1=red, 2=blue, 3=yellow, 0=background/outline
colormap = np.zeros((H,W), dtype=np.uint8)
colormap[red_mask] = 1
colormap[blue_mask] = 2
colormap[yellow_mask] = 3

# -----------------------------------------------------------------------
# APPROACH: flood-fill from black boundaries to find individual tiles
# The black borders separate tiles — use watershed-style separation
# -----------------------------------------------------------------------
# Build a "barrier" image where barriers = outline pixels
# Use distance-based approach: label connected colored regions BLOCKED by outlines

# Method: label connected components with the outline acting as separator
# i.e., two same-color pixels only in same component if path avoids outline+background

def tiles_with_barriers(mask, barrier, min_area=40):
    """Label connected regions of mask that are separated by barrier pixels"""
    # Remove barrier pixels from the mask
    clean = mask & ~barrier
    labeled, n = ndimage.label(clean)
    results = []
    for i in range(1, n+1):
        m = labeled == i
        area = int(m.sum())
        if area < min_area:
            continue
        ys, xs = np.where(m)
        pts = np.stack([xs,ys],axis=1).astype(float)
        results.append({
            'area': area,
            'cx': pts[:,0].mean(), 'cy': pts[:,1].mean(),
            'xmin': int(xs.min()), 'xmax': int(xs.max()),
            'ymin': int(ys.min()), 'ymax': int(ys.max()),
            'w': int(xs.max()-xs.min()), 'h': int(ys.max()-ys.min()),
        })
    return results

print("\n=== EXPANSION TILE COUNTS (using black outline as separator) ===\n")
ROW_BOUNDS = [(0,130,0,'RED'), (130,260,1,'BLUE'), (260,H,2,'YELLOW')]
tile_counts = {}
for y0,y1,ri,rname in ROW_BOUNDS:
    print(f"Row {ri} ({rname} →):")
    for name, mask in [('RED',red_mask),('BLUE',blue_mask),('YELLOW',yellow_mask)]:
        sub_mask    = mask[y0:y1, 120:].copy()
        sub_barrier = outline[y0:y1, 120:].copy()
        comps = tiles_with_barriers(sub_mask, sub_barrier, min_area=30)
        # translate back
        for c in comps:
            c['cx'] += 120; c['cy'] += y0
            c['xmin'] += 120; c['xmax'] += 120
            c['ymin'] += y0; c['ymax'] += y0
        n = len(comps)
        print(f"  {name}: {n} tiles")
        for c in sorted(comps, key=lambda x: (x['cy'], x['cx'])):
            print(f"    area={c['area']:5d}  center=({c['cx']:5.1f},{c['cy']:5.1f})  size={c['w']}x{c['h']}")
        tile_counts[f"r{ri}_{name}"] = n
    print()

print("\n=== SUBSTITUTION MATRIX ===")
print("M[tile_type][source_tile] = count")
types = ['RED','BLUE','YELLOW']
for ri, (y0,y1,_,rname) in enumerate(ROW_BOUNDS):
    for name in types:
        k = f"r{ri}_{name}"
        cnt = tile_counts.get(k, 0)
        print(f"  {rname} → {name}: {cnt}")

# Also compute the substitution matrix eigenvalues
print("\n=== SUBSTITUTION MATRIX EIGENVALUES ===")
# M[i,j] = number of tiles of type i in substitution of tile j
# Row 0 = RED source, Row 1 = BLUE source, Row 2 = YELLOW source
# Tile types: 0=RED, 1=BLUE, 2=YELLOW
M = np.zeros((3,3), dtype=float)
for ri, (y0,y1,src_idx,rname) in enumerate(ROW_BOUNDS):
    for ti, name in enumerate(types):
        k = f"r{ri}_{name}"
        M[ti, ri] = tile_counts.get(k, 0)
print("M ="); print(M)
eigvals = np.linalg.eigvals(M)
eigvals_sorted = sorted(eigvals.real, reverse=True)
print(f"Eigenvalues (real parts): {[f'{e:.4f}' for e in eigvals_sorted]}")
print(f"Largest eigenvalue (inflation factor squared?): {max(eigvals_sorted):.4f}")
print(f"sqrt(largest): {np.sqrt(abs(max(eigvals_sorted))):.4f}")
print(f"Bronze mean β = (3+sqrt(13))/2 = {(3+np.sqrt(13))/2:.4f}")
