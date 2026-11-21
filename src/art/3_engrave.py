import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
H, W = 941, 1672
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
xn = x / W
yn = y / H

# Pure Maven Creative / Form Bio monochrome studio background (no ships, no stars):
# Deep velvety obsidian #0c0c0c across the reading & navigation center,
# framed by soft diagonal silver-graphite atmospheric light sweeps at the outer corners.
base = np.full((H, W), 0.047, dtype=np.float32)  # #0c0c0c

# Top-right diagonal silver light sweep (echoing Form Bio's top-right #707070 grain)
d_tr = ((xn - 1.06) / 0.36) ** 2 + ((yn + 0.08) / 0.56) ** 2
light_tr = 0.36 * np.exp(-0.5 * d_tr)

# Bottom-left diagonal graphite counter-sweep (echoing Form Bio's bottom-left #454545 grain)
d_bl = ((xn + 0.06) / 0.28) ** 2 + ((yn - 1.08) / 0.44) ** 2
light_bl = 0.22 * np.exp(-0.5 * d_bl)

# Subtle secondary mid-right silver breath so wide monitors feel balanced and sculptural
d_mr = ((xn - 1.08) / 0.22) ** 2 + ((yn - 0.52) / 0.50) ** 2
light_mr = 0.08 * np.exp(-0.5 * d_mr)

out_L = np.clip(base + light_tr + light_bl + light_mr, 0.045, 0.52)

# Authentic Form Bio fine 1px analog monochrome film grain:
# quiet velvety grain in #0c0c0c reading center (~3.8/255), richer grain in the silver sweeps (~14-18/255)
rng = np.random.default_rng(42)
noise = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
norm_v = np.clip((out_L - 0.047) / 0.38, 0.0, 1.0)
sigma = 0.015 + 0.052 * np.power(norm_v, 0.72)
out_L = np.clip(out_L + noise * sigma, 0.0, 1.0)

rgb = np.stack([out_L, out_L, out_L], axis=-1)
img = Image.fromarray((rgb * 255).astype(np.uint8), mode='RGB')
img.save(S + 'engraved.jpg', quality=88, optimize=True, progressive=True)

im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')



