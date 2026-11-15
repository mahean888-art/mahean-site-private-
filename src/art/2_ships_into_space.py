import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import os
S=os.path.dirname(os.path.abspath(__file__))+'/'
a=np.asarray(Image.open(S+'original.jpg').convert('RGB')).astype(np.float32)/255
H,W,_=a.shape
keep=np.load(S+'keep4.npy')
k=ndi.binary_erosion(keep,iterations=3)
mx=a.max(-1); mn=a.min(-1); sat=(mx-mn)/(mx+1e-6)
hullish=np.clip((0.86-sat)/0.18,0,1)
hullish=ndi.grey_closing(hullish,size=(3,3))
w=(ndi.gaussian_filter(k.astype(np.float32),1.5)*ndi.gaussian_filter(hullish,0.8))[...,None]
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
# steel hull: keep linework, cool grey with a little blue, darker overall
Ln=np.clip((L-0.08)/0.85,0,1)**1.15
hull=np.stack([0.10+0.62*Ln,0.13+0.70*Ln,0.17+0.78*Ln],-1)
y,x=np.mgrid[0:H,0:W].astype(np.float32)
# rim light from below-centre (planet glow)
rim=np.exp(-((x-W*0.5)**2/(2*(W*0.45)**2)))*np.clip((y/H-0.3)/0.7,0,1)
hull=hull*(0.78+0.35*rim[...,None]*np.array([0.7,0.9,1.1]))
rng=np.random.default_rng(11)
def noise(scale):
    sm=rng.random((H//scale+2,W//scale+2)).astype(np.float32); return ndi.zoom(sm,scale,order=3)[:H,:W]
n=sum(noise(s)*wt for s,wt in [(180,.5),(70,.3),(28,.15),(11,.05)]); n=(n-n.min())/(n.max()-n.min())
sp=np.zeros((H,W,3),np.float32)
sp+=np.array([0.03,0.09,0.15])+ (y/H)[...,None]*np.array([0.01,0.06,0.10])
sp+=(np.exp(-((x-W*0.5)**2+(y-H*1.05)**2)/(2*(H*0.55)**2)))[...,None]*np.array([0.04,0.20,0.30])
neb=np.clip(n*1.5-0.5,0,1)**1.5
sp+=neb[...,None]*np.array([0.05,0.18,0.26])
st=np.zeros((H,W),np.float32); N=3200
ys=rng.integers(0,H,N); xs=rng.integers(0,W,N); st[ys,xs]=0.15+rng.random(N)**4*1.6
st=ndi.gaussian_filter(st,0.55)*3.2
sp+=st[...,None]*np.array([0.9,0.95,1.0])
for _ in range(10):
    sx,sy=rng.integers(0,W),rng.integers(0,H); b=0.4+rng.random()*0.5
    d=np.hypot(x-sx,y-sy); sp+=(b*np.exp(-d**2/3)+0.06*b*np.exp(-d/8))[...,None]
wm=w[...,0]>0.35
lab,n=ndi.label(wm); idx=np.arange(1,n+1)
area=ndi.sum(wm,lab,idx)
objs=ndi.find_objects(lab)
drop=[]
for i,sl in enumerate(objs):
    h=sl[0].stop-sl[0].start; ww=sl[1].stop-sl[1].start
    solidity=area[i]/(h*ww+1e-6)
    if area[i]<2600 and solidity<0.42: drop.append(i+1)
    elif area[i]<500: drop.append(i+1)
dm=np.isin(lab,drop); dm=ndi.binary_dilation(dm,iterations=3)
w=w*(1-ndi.gaussian_filter(dm.astype(np.float32),1.5))[...,None]
print('components',n,'dropped',len(drop))
from PIL import ImageDraw
sc=W/1100.0
poly=[(1100,120),(1062,128),(1000,212),(928,288),(918,330),(965,335),(1045,250),(1100,205)]
pm=Image.new('L',(W,H),0); ImageDraw.Draw(pm).polygon([(px*sc,py*sc) for px,py in poly],fill=255)
pm=np.asarray(pm.filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(3))).astype(np.float32)/255
w=w*(1-pm)[...,None]
out=sp*(1-w)+hull*w
Image.fromarray((np.clip(out,0,1)**(1/1.05)*255).astype(np.uint8)).save(S+'ships-in-space.jpg',quality=86,optimize=True,progressive=True)
im=Image.open(S+'ships-in-space.jpg'); im.thumbnail((1100,1100)); im.save(S+'orig_space2_s.png')
im=Image.open(S+'ships-in-space.jpg'); im.crop((int(W*0.6),int(H*0.4),int(W*0.95),int(H*0.9))).save(S+'orig_space2_c.png')

# ---- ships-only RGBA layer for the right side
x0 = int(W*0.50)
alpha = w[...,0].copy()*0.72
st2 = np.clip(st*0.9,0,1)
alpha = np.maximum(alpha, st2*0.9)
rgb = hull*w + (1-w)*np.array([0.85,0.92,1.0])  # star colour where not hull
xx = (np.arange(W)-x0)/(W*0.14)
fade = np.clip(xx,0,1); fade = fade*fade*(3-2*fade)
alpha = alpha*fade[None,:]
rgba = np.dstack([np.clip(rgb,0,1)**(1/1.05), alpha])[:, x0:]
Image.fromarray((rgba*255).astype(np.uint8),'RGBA').save(S+'ships_layer.webp', quality=85, method=6)
import os; print('layer', os.path.getsize(S+'ships_layer.webp'), rgba.shape)
