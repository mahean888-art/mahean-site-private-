import numpy as np
from PIL import Image
import os

S = os.path.dirname(os.path.abspath(__file__)) + '/'
a = np.asarray(Image.open(S + 'ships-in-space.jpg').convert('RGB')).astype(np.float32) / 255.0
H, W, _ = a.shape
y, x = np.mgrid[0:H, 0:W].astype(np.float32)

# Deep midnight-ink canvas matching the darkest space sky (#080d15)
bg = np.array([8, 13, 21], dtype=np.float32) / 255.0

# Keep the original ink-drawn ships and stars crisp; deepen the background sky
# and calm the mid-field nebula without artificial scanlines or spotlight blobs.
v = np.clip((a - 0.035) / 0.965, 0.0, 1.0)
v = np.power(v, 1.32) * 0.90

# Smooth fade into pure solid #080d15 across the left/middle reading zone
fx = np.clip((x / W - 0.42) / 0.28, 0.0, 1.0)
fx = fx * fx * (3.0 - 2.0 * fx)

# Gentle top/bottom vertical feather so edges blend seamlessly
fy = np.clip(1.0 - np.abs(y / H - 0.52) / 0.62, 0.0, 1.0) ** 0.35
mask = (fx * fy)[..., None]

out = bg + (v - bg) * mask
Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)).save(
    S + 'engraved.jpg', quality=88, optimize=True, progressive=True
)
im = Image.open(S + 'engraved.jpg')
im.thumbnail((1100, 1100))
im.save(S + 'engrave_s.png')

