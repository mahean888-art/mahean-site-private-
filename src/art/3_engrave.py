import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import os
S=os.path.dirname(os.path.abspath(__file__))+'/'
a=np.asarray(Image.open(S+'ships-in-space.jpg').convert('RGB')).astype(np.float32)/255
H,W,_=a.shape
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
# contrast: crush the sky, lift the hulls
L=np.clip((L-0.16)/0.62,0,1)**1.25
y,x=np.mgrid[0:H,0:W].astype(np.float32)
# glow behind the fleet (like the converter's light)
gx,gy=W*0.80,H*0.42
glow=np.exp(-((x-gx)**2+(y-gy)**2)/(2*(H*0.33)**2))
L=np.clip(L+0.22*glow,0,1)
# engraving line screen: thin diagonal hatching, stronger in midtones
t=(x*0.6+y*0.8)/1.7
hatch=(np.sin(t*np.pi)*0.5+0.5)
mid=np.clip(1-np.abs(L-0.45)/0.45,0,1)
L=L*(1-0.28*mid*(hatch<0.45))
# duotone navy -> pale steel-cream
dark=np.array([20,41,59])/255; light=np.array([196,222,242])/255
out=dark+(light-dark)*L[...,None]
# vignette / left fade baked in
fx=np.clip((x/W-0.05)/0.45,0,1); fx=fx*fx*(3-2*fx)
fy=np.clip(1-np.abs(y/H-0.5)/0.55,0,1)**0.6
f=(fx*fy)[...,None]
out=dark+(out-dark)*f
Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)).save(S+'engraved.jpg',quality=86,optimize=True,progressive=True)
im=Image.open(S+'engraved.jpg'); im.thumbnail((1100,1100)); im.save(S+'engrave_s.png')
