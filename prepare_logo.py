from PIL import Image
import numpy as np
from pathlib import Path
BASE=Path(__file__).parent
p=BASE/'lataminds_original.png'
a=np.array(Image.open(p).convert('RGB'),dtype=np.uint8)
strength=255-np.min(a,axis=2)
ys,xs=np.where(strength>42)
x0,x1=max(0,xs.min()-16),min(a.shape[1],xs.max()+17)
y0,y1=max(0,ys.min()-16),min(a.shape[0],ys.max()+17)
b=a[y0:y1,x0:x1]
alpha=np.clip((255-b.astype(float).min(2)-16)*3.5,0,255).astype(np.uint8)
# Suprime la compresión/ruido de la imagen original casi blanca.
alpha[(b.min(axis=2)>235)&((b.max(axis=2).astype(int)-b.min(axis=2).astype(int))<10)]=0
rgba=np.concatenate([b,alpha[:,:,None]],axis=2)
im=Image.fromarray(rgba,'RGBA'); im.thumbnail((890,480),Image.Resampling.LANCZOS)
im.save(BASE/'LATAMinds_logo_transparente.png',optimize=True)
print('logo',im.size)
