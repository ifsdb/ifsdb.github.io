from PIL import Image
import numpy as np
from scipy import ndimage

img = Image.open('C:/ifsdb.github.io/public/bronze-mean-rule.png')
arr = np.array(img)
R,G,B,A = arr[:,:,0].astype(float), arr[:,:,1].astype(float), arr[:,:,2].astype(float), arr[:,:,3].astype(float)

H, W = arr.shape[:2]
print(f"Image: {W}x{H}")

red_mask    = (A > 200) & (R > 180) & (G < 100) & (B < 150)
blue_mask   = (A > 200) & (R < 80)  & (G > 100) & (B > 150)
yellow_mask = (A > 200) & (R > 200) & (G > 180) & (B < 150)
print(f"Red: {red_mask.sum()}, Blue: {blue_mask.sum()}, Yellow: {yellow_mask.sum()}")

def get_components(mask, min_area=30):
    dilated = ndimage.binary_dilation(mask, iterations=2)
    labeled, n = ndimage.label(dilated)
    components = []
    for i in range(1, n+1):
        actual = mask & (labeled==i)
        area = int(actual.sum())
        if area < min_area:
            continue
        ys, xs = np.where(actual)
        components.append({
            'area': area,
            'cx': float(xs.mean()),
            'cy': float(ys.mean()),
            'xmin': int(xs.min()), 'xmax': int(xs.max()),
            'ymin': int(ys.min()), 'ymax': int(ys.max()),
        })
    return components

ROW_H = H / 3  # ~130px per row

for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
    comps = get_components(mask)
    print(f"\n{name} ({len(comps)} pieces):")
    for c in sorted(comps, key=lambda x: (int(x['cy']//ROW_H), x['cx'])):
        row = int(c['cy'] // ROW_H)
        w = c['xmax'] - c['xmin']
        h = c['ymax'] - c['ymin']
        print(f"  row{row} area={c['area']:5d}  center=({c['cx']:5.1f},{c['cy']:5.1f})  size={w}x{h}")

# ---------------------------------------------------------------
# Measure tile sizes from the SMALL prototypes on the LEFT side
# The arrow is around x=80 in each row, small tile is to the left
# ---------------------------------------------------------------
print("\n=== Prototype tile measurements (left side, x < 80) ===")
for name, mask in [('RED', red_mask), ('BLUE', blue_mask), ('YELLOW', yellow_mask)]:
    comps = get_components(mask, min_area=10)
    small = [c for c in comps if c['cx'] < 80]
    print(f"{name}: {len(small)} prototype(s)")
    for c in small:
        w = c['xmax'] - c['xmin']
        h = c['ymax'] - c['ymin']
        print(f"  area={c['area']}  size={w}x{h}  center=({c['cx']:.1f},{c['cy']:.1f})")
