import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
a = np.asarray(Image.open(S + 'ships-in-space.jpg').convert('RGB')).astype(np.float32) / 255.0
H, W, _ = a.shape
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
xn = x / W
yn = y / H

# 1. Pure neutral monochrome luminance from the ships-in-space artwork (R = G = B)
L = 0.28 * a[..., 0] + 0.59 * a[..., 1] + 0.13 * a[..., 2]

# Separate crisp hull highlights & dark ink lines while calming the space nebula haze
ship_L = np.clip((L - 0.10) / 0.80, 0.0, 1.0)
ship_L = np.power(ship_L, 1.38) * 0.82

# Extract dark ink creases ONLY inside lit ship hulls (using local average, never ringing isolated stars)
pad = np.pad(L, 2, mode='edge')
local_mean = (
    pad[0:H, 0:W] + pad[0:H, 2:W+2] + pad[0:H, 4:W+4] +
    pad[2:H+2, 0:W] + pad[2:H+2, 2:W+2] + pad[2:H+2, 4:W+4] +
    pad[4:H+4, 0:W] + pad[4:H+4, 2:W+2] + pad[4:H+4, 4:W+4]
) / 9.0
# Hull interiors have elevated local_mean; stars in dark space do not
on_hull = np.clip((local_mean - 0.24) / 0.14, 0.0, 1.0)
ink_crease = np.clip((local_mean - L - 0.025) / 0.18, 0.0, 1.0) * on_hull

# 2. Maven Creative / Form Bio sculptural monochrome lighting field
# Velvety obsidian #0c0c0c across the middle/left reading zone
base = np.full((H, W), 0.047, dtype=np.float32)

# Top-right diagonal silver-graphite atmospheric wash (echoing Form Bio's top-right #707070 grain)
d_tr = ((xn - 1.04) / 0.31) ** 2 + ((yn + 0.06) / 0.54) ** 2
light_tr = 0.34 * np.exp(-0.5 * d_tr)

# Subtle bottom-left corner graphite counter-wash, strictly clear of the middle text column
d_bl = ((xn + 0.05) / 0.21) ** 2 + ((yn - 1.05) / 0.33) ** 2
light_bl = 0.15 * np.exp(-0.5 * d_bl)

# Soft silver rim behind the lower-right fleet for silver-gelatin tonal separation
d_fleet = ((xn - 0.89) / 0.22) ** 2 + ((yn - 0.62) / 0.36) ** 2
light_fleet = 0.10 * np.exp(-0.5 * d_fleet)

field = base + light_tr + light_bl + light_fleet

# 3. Reveal the right-side fleet cleanly; keep both the reading column and sidebar pocket velvety dark
fx = np.clip((xn - 0.54) / 0.21, 0.0, 1.0)
fx = fx * fx * (3.0 - 2.0 * fx)

# Carve ship ink crevices through the silver wash, then lift lit hull plates into brushed silver
out_L = field * (1.0 - 0.62 * ink_crease * fx) + (ship_L * 0.84) * fx
out_L = np.clip(out_L, 0.040, 0.86)

# 4. Fine 1px analog monochrome film grain matching Form Bio's tonal noise profile:
# quiet velvety grain in #0c0c0c reading pocket (~3.8/255), richer silver grain in light sweeps (~15-20/255)
rng = np.random.default_rng(42)
noise = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
norm_v = np.clip((out_L - 0.047) / 0.45, 0.0, 1.0)
sigma = 0.015 + 0.056 * np.power(norm_v, 0.72)
out_L = np.clip(out_L + noise * sigma, 0.0, 1.0)

rgb = np.stack([out_L, out_L, out_L], axis=-1)
img = Image.fromarray((rgb * 255).astype(np.uint8), mode='RGB')
img.save(S + 'engraved.jpg', quality=88, optimize=True, progressive=True)

im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')


