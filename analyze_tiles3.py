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

# -----------------------------------------------------------------------
# Find convex-hull vertices for each prototype tile
# -----------------------------------------------------------------------
def hull_vertices(mask_2d, min_area=5):
    """
    Find connected components and return convex-hull vertices of each.
    """
    labeled, n = ndimage.label(mask_2d)
    results = []
    for i in range(1, n+1):
        m = labeled == i
        area = int(m.sum())
        if area < min_area:
            continue
        ys, xs = np.where(m)
        pts = np.stack([xs, ys], axis=1).astype(float)
        if len(pts) < 3:
            continue
        hull = spatial.ConvexHull(pts)
        verts = pts[hull.vertices]
        # order counter-clockwise from lowest-x, lowest-y
        cx, cy = pts.mean(0)
        angles = np.arctan2(verts[:,1]-cy, verts[:,0]-cx)
        order = np.argsort(angles)
        verts = verts[order]
        results.append({'area': area, 'hull': verts, 'cx': cx, 'cy': cy})
    return results

print("=== PROTOTYPE SHAPES (left side, x < 85) ===\n")
protos = {}
for ri in range(3):
    y0, y1 = ri*130, (ri+1)*130 if ri < 2 else H
    for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
        sub_mask = mask[y0:y1, :85].copy()
        comps = hull_vertices(sub_mask, min_area=50)
        if not comps:
            continue
        c = max(comps, key=lambda x: x['area'])
        v = c['hull'].copy()
        # translate back to full image coordinates
        v[:,1] += y0
        print(f"Row {ri} {name} prototype:  area={c['area']}  cx={c['cx']:.1f} cy={c['cy']+y0:.1f}")
        print(f"  hull vertices (x, y):")
        for vx, vy in v:
            print(f"    ({vx:.1f}, {vy+0:.1f})")
        # edge lengths
        n_v = v.shape[0]
        edges = []
        for j in range(n_v):
            dx = v[(j+1)%n_v,0]-v[j,0]; dy = v[(j+1)%n_v,1]-v[j,1]
            edges.append(np.hypot(dx,dy))
        print(f"  edge lengths: {[f'{e:.2f}' for e in edges]}")
        print(f"  bounding box: {int(v[:,0].max()-v[:,0].min())+1} x {int(v[:,1].max()-v[:,1].min())+1}")
        protos[f"r{ri}_{name}"] = {'hull': v, 'area': c['area'], 'edges': edges}
        print()

# -----------------------------------------------------------------------
# Count tile copies in each substitution (NO dilation)
# -----------------------------------------------------------------------
print("\n=== SUBSTITUTION TILE COUNTS (no dilation) ===\n")
for ri in range(3):
    y0, y1 = ri*130, (ri+1)*130 if ri < 2 else H
    src = ['RED','BLUE','YELLOW'][ri]
    print(f"Row {ri}  ({src} →)")
    for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
        sub_mask = mask[y0:y1, 120:].copy()
        labeled, n = ndimage.label(sub_mask)
        # count components with area > 20
        large = sum(1 for i in range(1, n+1) if (labeled==i).sum() > 20)
        all_areas = sorted([(labeled==i).sum() for i in range(1, n+1) if (labeled==i).sum() > 10],
                          reverse=True)
        print(f"  {name}: {large} pieces  areas={[int(a) for a in all_areas[:15]]}")
    print()

# -----------------------------------------------------------------------
# Geometric analysis: tile sizes to determine nature of shapes
# -----------------------------------------------------------------------
print("\n=== GEOMETRIC ANALYSIS ===\n")
# The row display scales might differ; calibrate by examining matching tiles
# Row1 YELLOW in expanded region should match row2 YELLOW prototype
# Check areas:
for ri in range(3):
    y0, y1 = ri*130, (ri+1)*130 if ri < 2 else H
    for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
        sub_mask = mask[y0:y1, :85].copy()
        labeled, n = ndimage.label(sub_mask)
        areas = [(labeled==i).sum() for i in range(1, n+1) if (labeled==i).sum() > 40]
        if areas:
            print(f"Prototype row{ri} {name}: area={max(areas)}")
