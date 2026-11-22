import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
H, W = 941, 1672
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
xn = x / W
yn = y / H

# Dune archival sandstone-parchment palette sampled from the Fremen / Emperor plates:
# Warm sunlit parchment center (#e5ded0), luminous alabaster-sand light on the right (#f1ede4),
# and deeper warm sandstone-taupe depth along the outer left & lower-left edges (#c7baa4).
sand_mid = np.array([229, 222, 208], dtype=np.float32) / 255.0   # #e5ded0 warm parchment core
sand_lit = np.array([242, 238, 229], dtype=np.float32) / 255.0   # #f2eee5 sunlit alabaster-sand
sand_shd = np.array([196, 184, 163], dtype=np.float32) / 255.0   # #c4b8a3 warm desert taupe edge

# Soft sunlit sweep from upper-right / right (matching "The Fremen" plate lighting)
d_lit = ((xn - 0.96) / 0.52) ** 2 + ((yn - 0.42) / 0.68) ** 2
w_lit = np.exp(-0.5 * d_lit) * 0.85

# Warm sandstone shadow grounding the left & lower-left perimeter (bridging both Dune plates)
d_shd1 = ((xn + 0.08) / 0.36) ** 2 + ((yn - 0.10) / 0.55) ** 2
d_shd2 = ((xn + 0.06) / 0.40) ** 2 + ((yn - 0.98) / 0.48) ** 2
w_shd = np.clip(0.72 * np.exp(-0.5 * d_shd1) + 0.78 * np.exp(-0.5 * d_shd2), 0.0, 0.92)

# Subtle lower-right corner warmth so the page feels softly framed like an archival sheet
d_br = ((xn - 1.04) / 0.28) ** 2 + ((yn - 1.04) / 0.32) ** 2
w_shd = np.clip(w_shd + 0.32 * np.exp(-0.5 * d_br), 0.0, 0.95)

out = sand_mid[None, None, :] * (1.0 - w_lit[..., None]) + sand_lit[None, None, :] * w_lit[..., None]
out = out * (1.0 - w_shd[..., None] * 0.65) + sand_shd[None, None, :] * (w_shd[..., None] * 0.65)

# Ultra-fine warm mineral / cotton-rag paper grain (tactile, never noisy over text)
rng = np.random.default_rng(42)
grain = rng.normal(0.0, 0.0085, (H, W, 1)).astype(np.float32)
out = np.clip(out + grain, 0.0, 1.0)

img = Image.fromarray((out * 255).astype(np.uint8), mode='RGB')
img.save(S + 'engraved.jpg', quality=90, optimize=True, progressive=True)

im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')






