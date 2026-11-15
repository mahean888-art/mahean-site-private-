import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import os
S=os.path.dirname(os.path.abspath(__file__))+'/'
a=np.asarray(Image.open(S+'original.jpg').convert('RGB')).astype(np.float32)/255
H,W,_=a.shape
L=0.3*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
ink=np.clip(ndi.grey_closing(L,size=(5,5))-L,0,1)   # black-hat: thin dark lines
dens=ndi.gaussian_filter((ink>0.06).astype(np.float32),7)
m=dens>0.11
m=ndi.binary_closing(m,iterations=5); m=ndi.binary_fill_holes(m); m=ndi.binary_opening(m,iterations=4)
lab,n=ndi.label(m); sizes=ndi.sum(m,lab,range(1,n+1))
keep=np.isin(lab,1+np.where(sizes>1500)[0])
print(n,(sizes>1500).sum())
Image.fromarray((keep*255).astype(np.uint8)).resize((W//2,H//2)).save(S+'mask4s.png')
np.save(S+'keep4.npy',keep)
