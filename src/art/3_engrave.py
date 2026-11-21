import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
H, W = 941, 1672
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
xn = x / W
yn = y / H

# Maven Creative "darker yet glowy" monochrome atmosphere:
# Deep velvety dark obsidian (#090909) with high-contrast sculptural silver-mist glow —
# genuinely dark and calm behind the text, yet alive with a soft darkroom luminescence.
base = np.full((H, W), 0.034, dtype=np.float32)  # #090909 deep velvety dark

aspect = W / H
dx = (xn - 0.48) * aspect
dy = (yn - 0.50)
r = np.hypot(dx, dy)

# Soft sculptural crescent / backlit eclipse glow — darker inside, softly glowing along a sweeping arc
# Stronger toward upper-right & lower-left (Form Bio diagonal lighting) so it glows without washing out the middle
angle = np.arctan2(dy, dx)
diag_bias = 0.55 + 0.45 * np.cos(2.0 * (angle + 0.55))  # peaks upper-right & lower-left
halo = 0.125 * np.exp(-0.5 * ((r - 0.58) / 0.17) ** 2) * diag_bias

# Subtle warm-neutral backlit bloom in the upper-right and lower-left corners (keeps edges alive, not dead black)
d_tr = ((xn - 1.00) / 0.30) ** 2 + ((yn + 0.02) / 0.38) ** 2
glow_tr = 0.17 * np.exp(-0.5 * d_tr)

d_bl = ((xn + 0.02) / 0.28) ** 2 + ((yn - 1.02) / 0.36) ** 2
glow_bl = 0.13 * np.exp(-0.5 * d_bl)

# Faint, silky ambient breath behind center so the reading zone feels "not pure #000", yet stays deeply dark (#0d0d0d-#121212)
center_breath = 0.026 * np.exp(-0.5 * (r / 0.45) ** 2)

out_L = np.clip(base + center_breath + halo + glow_tr + glow_bl, 0.032, 0.32)

# Fine 1px monochrome film grain: silky & quiet in deep darks, subtly luminous across the silver glow
rng = np.random.default_rng(42)
noise = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
norm_v = np.clip((out_L - 0.034) / 0.25, 0.0, 1.0)
sigma = 0.011 + 0.038 * np.power(norm_v, 0.78)
out_L = np.clip(out_L + noise * sigma, 0.0, 1.0)

rgb = np.stack([out_L, out_L, out_L], axis=-1)
img = Image.fromarray((rgb * 255).astype(np.uint8), mode='RGB')
img.save(S + 'engraved.jpg', quality=88, optimize=True, progressive=True)

im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')





