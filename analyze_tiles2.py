from PIL import Image
import numpy as np
from scipy import ndimage

img = Image.open('C:/ifsdb.github.io/public/bronze-mean-rule.png')
arr = np.array(img)
R,G,B,A = [arr[:,:,i].astype(float) for i in range(4)]
H, W = arr.shape[:2]

# --- Color masks ---
red_mask    = (A > 200) & (R > 180) & (G < 100) & (B < 150)
blue_mask   = (A > 200) & (R < 80)  & (G > 100) & (B > 150)
yellow_mask = (A > 200) & (R > 200) & (G > 180) & (B < 150)

# Row boundaries (3 rows)
row_bounds = [(0,130), (130,260), (260,H)]

# Expanded region: right side only
EX_START = 120

def components_in(mask, y0, y1, x0=0, x1=None, dil=1, min_area=20):
    if x1 is None: x1 = W
    sub = mask[y0:y1, x0:x1].copy()
    if dil > 0:
        sub = ndimage.binary_dilation(sub, iterations=dil)
    labeled, n = ndimage.label(sub)
    comps = []
    for i in range(1, n+1):
        m_dil = labeled==i
        m_act = mask[y0:y1, x0:x1] & m_dil
        area = int(m_act.sum())
        if area < min_area:
            continue
        ys, xs = np.where(m_act)
        comps.append({
            'area': area,
            'cx': float(xs.mean()) + x0,
            'cy': float(ys.mean()) + y0,
            'w': int(xs.max()-xs.min()),
            'h': int(ys.max()-ys.min()),
        })
    return comps

print("=== LEFT SIDE PROTOTYPES (x < 80) ===")
names = ['RED', 'BLUE', 'YELLOW']
masks = [red_mask, blue_mask, yellow_mask]
proto = {}
for ri, (y0,y1) in enumerate(row_bounds):
    for name, mask in zip(names, masks):
        comps = components_in(mask, y0, y1, x0=0, x1=80, dil=1, min_area=10)
        if comps:
            c = max(comps, key=lambda x: x['area'])
            proto[f"{name}_r{ri}"] = c
            print(f"  row{ri} {name}: area={c['area']} bbox={c['w']}x{c['h']}  center=({c['cx']:.1f},{c['cy']:.1f})")

print("\n=== SUBSTITUTION RULE (x > 120) ===")
for ri, (y0,y1) in enumerate(row_bounds):
    print(f"\nRow {ri} ({'RED->','BLUE->','YELLOW->'}[ri])")
    for name, mask in zip(names, masks):
        comps = components_in(mask, y0, y1, x0=EX_START, dil=0, min_area=15)
        print(f"  {name}: {len(comps)} pieces")
        for c in sorted(comps, key=lambda x: (x['cy'], x['cx'])):
            print(f"    area={c['area']:5d}  center=({c['cx']:6.1f},{c['cy']:6.1f})  size={c['w']}x{c['h']}")

print("\n=== RATIO ANALYSIS ===")
# The bronze mean β: inflated tile is β times larger
# Find ratios of expanded tile to prototype
# Use the big bounding-box of all expanded tiles
for ri, (y0,y1) in enumerate(row_bounds):
    row_names = ['RED_rule', 'BLUE_rule', 'YELLOW_rule']
    src_name = names[ri]
    exp_mask = None
    for name, mask in zip(names, masks):
        comps = components_in(mask, y0, y1, x0=EX_START, dil=0, min_area=15)
        if comps:
            all_cx = [c['cx'] for c in comps]
            all_cy = [c['cy'] for c in comps]
    # find full expanded region bbox by looking at any opaque non-background pixel
    sub = arr[y0:y1, EX_START:W]
    opaque = sub[:,:,3] > 100
    if opaque.sum() > 0:
        ys, xs = np.where(opaque)
        w_exp = xs.max() - xs.min()
        h_exp = ys.max() - ys.min()
        pk = f"{src_name}_r{ri}"
        if pk in proto:
            p = proto[pk]
            print(f"  Row{ri} {src_name}: prototype {p['w']}x{p['h']}, expanded bbox ~{w_exp}x{h_exp}, scale_x={w_exp/p['w']:.3f}, scale_y={h_exp/p['h']:.3f}")
