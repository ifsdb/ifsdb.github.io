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

def get_all_shapes(mask, dil=1, min_area=30):
    d = ndimage.binary_dilation(mask, iterations=dil)
    labeled, n = ndimage.label(d)
    results = []
    for i in range(1, n+1):
        actual = mask & (labeled==i)
        area = int(actual.sum())
        if area < min_area:
            continue
        ys, xs = np.where(actual)
        pts = np.stack([xs,ys],axis=1).astype(float)
        results.append({
            'area': area,
            'cx': pts[:,0].mean(), 'cy': pts[:,1].mean(),
            'xmin': xs.min(), 'xmax': xs.max(),
            'ymin': ys.min(), 'ymax': ys.max(),
            'w': xs.max()-xs.min(), 'h': ys.max()-ys.min(),
        })
    return results

# -----------------------------------------------------------------------
# Focus on row 1 (BLUE → expansion):  analyze individual tile shapes
# -----------------------------------------------------------------------
print("=== ROW 1 (BLUE →): individual tile shapes in expansion (x>120) ===\n")
for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
    shapes = get_all_shapes(mask[130:260, 120:], dil=0, min_area=5)
    # translate y back
    for s in shapes:
        s['cy'] += 130; s['ymin'] += 130; s['ymax'] += 130
        s['cx'] += 120; s['xmin'] += 120; s['xmax'] += 120
    shapes.sort(key=lambda x: x['area'])
    print(f"  {name}:")
    for s in shapes:
        print(f"    area={s['area']:5d}  center=({s['cx']:6.1f},{s['cy']:5.1f})  size={s['w']}x{s['h']}")

print("\n=== SCALE CALIBRATION ===")
# Row 2 should be at scale 1.0 (YELLOW tiles match prototype)
# Row 1: check which tiles match prototype sizes
print("\nRow 1 tile areas vs prototypes:")
print(f"  RED prototype:    {271}")
print(f"  BLUE prototype:   {494}")
print(f"  YELLOW prototype: {884}")

# Expansion of row 1 areas:
for name, mask, proto in [('RED', red_mask, 271), ('BLUE', blue_mask, 494), ('YELLOW', yellow_mask, 884)]:
    shapes = get_all_shapes(mask[130:260, 120:], dil=0, min_area=5)
    areas = sorted([s['area'] for s in shapes if s['area'] > 20], reverse=True)
    print(f"\n  {name} (proto={proto}) in row-1 expansion:")
    for a in areas:
        print(f"    area={a}  scale_area={a/proto:.3f}  scale_lin={np.sqrt(a/proto):.3f}")

print("\n=== ROW 2 (YELLOW →): individual tile shapes in expansion (x>120) ===\n")
for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
    shapes = get_all_shapes(mask[260:, 120:], dil=0, min_area=5)
    for s in shapes:
        s['cy'] += 260; s['ymin'] += 260; s['ymax'] += 260
        s['cx'] += 120; s['xmin'] += 120; s['xmax'] += 120
    shapes.sort(key=lambda x: x['area'])
    print(f"  {name}:")
    for s in shapes:
        print(f"    area={s['area']:5d}  center=({s['cx']:6.1f},{s['cy']:5.1f})  size={s['w']}x{s['h']}")

print("\n=== EXPANSION BOUNDING BOXES ===")
for ri in range(3):
    y0 = ri*130; y1 = (ri+1)*130 if ri < 2 else H
    sub = arr[y0:y1, 120:]
    opaque = sub[:,:,3] > 100
    ys, xs = np.where(opaque)
    if ys.size:
        print(f"Row {ri}: opaque region spans x={xs.min()+120}-{xs.max()+120}, y={ys.min()+y0}-{ys.max()+y0}  -> bbox {xs.max()-xs.min()} x {ys.max()-ys.min()}")
