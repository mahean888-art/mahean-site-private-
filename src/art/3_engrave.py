import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
H, W = 941, 1672
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
xn = x / W
yn = y / H

# Exact left-to-right sunlit parchment gradient sampled from the Dune "The Fremen" plate:
# x=0.00: #cfc0a6 -> x=0.25: #dbd0bb -> x=0.50: #e8dfd0 -> x=0.75: #f0ebe0 -> x=1.00: #f4f1e8
stops_x = np.array([0.0, 0.25, 0.50, 0.75, 1.0], dtype=np.float32)
stops_rgb = np.array([
    [207, 192, 166],  # #cfc0a6 warm golden-sandstone left
    [220, 208, 188],  # #dcd0bc warm sand
    [233, 224, 208],  # #e9e0d0 luminous parchment center
    [241, 236, 225],  # #f1ece1 soft alabaster
    [245, 241, 232],  # #f5f1e8 sunlit desert alabaster right
], dtype=np.float32) / 255.0

# Slight diagonal angle (light entering gently from right / upper-right)
t = np.clip(xn * 0.94 + (1.0 - yn) * 0.08 - 0.02, 0.0, 1.0)
out = np.empty((H, W, 3), dtype=np.float32)
for c in range(3):
    out[..., c] = np.interp(t, stops_x, stops_rgb[:, c])

# Whisper-soft subtle bottom-left & top-left warmth (keeps edges natural, zero blotches)
edge_warm = np.exp(-((xn / 0.30) ** 2 + ((yn - 0.95) / 0.45) ** 2) * 0.5) * 0.028
out = np.clip(out - edge_warm[..., None] * np.array([0.55, 0.75, 1.0], dtype=np.float32), 0.0, 1.0)

# Ultra-fine archival cotton-rag grain (imperceptible over text, silky tactile finish)
rng = np.random.default_rng(42)
grain = rng.normal(0.0, 0.0045, (H, W, 1)).astype(np.float32)
out = np.clip(out + grain, 0.0, 1.0)

img = Image.fromarray((out * 255).astype(np.uint8), mode='RGB')
img.save(S + 'engraved.jpg', quality=92, optimize=True, progressive=True)

im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')







