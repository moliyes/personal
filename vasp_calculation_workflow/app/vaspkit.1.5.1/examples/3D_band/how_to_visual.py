#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #silent mode
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d.axes3d import Axes3D


try:
	kx_mesh=np.loadtxt('KX.grd')      
	ky_mesh=np.loadtxt('KY.grd')   
	CBM_mesh=np.loadtxt('BAND_LUMO.grd')        
	VBM_mesh=np.loadtxt('BAND_HOMO.grd')

except:
    print("Failed to open grds!")


font = {'family' : 'arial',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 13,  
        }  

fig = plt.figure()

ax0 = fig.add_subplot(131, projection="3d")     

cmap = plt.cm.get_cmap("hsv") 
ax0.plot_surface(kx_mesh,ky_mesh,VBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)
ax0.plot_surface(kx_mesh,ky_mesh,CBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)

ax0.contourf(kx_mesh,ky_mesh,CBM_mesh,zdir='z',offset=0,cmap=cmap)

#ax0.set_xlabel(r'$\mathbf{k}_{x}$',fontdict=font)
ax0.set_ylabel(r'$\mathbf{k}_{y}$',fontdict=font)
ax0.set_zlabel(r'$Energy (eV)$',fontdict=font)
ax0.set_zlim((-5,5))
ax0.set_xticks([])
ax0.view_init(elev=0, azim=0)
  
ax = fig.add_subplot(132, projection="3d")     

cmap = plt.cm.get_cmap("hsv") 
ax.plot_surface(kx_mesh,ky_mesh,VBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)
ax.plot_surface(kx_mesh,ky_mesh,CBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)

ax.contourf(kx_mesh,ky_mesh,CBM_mesh,zdir='z',offset=0,cmap=cmap)

ax.set_xlabel(r'$\mathbf{k}_{x}$',fontdict=font)
ax.set_ylabel(r'$\mathbf{k}_{y}$',fontdict=font)
ax.set_zlabel(r'$Energy (eV)$',fontdict=font)
ax.set_zlim((-5,5))
ax.view_init(elev=0, azim=45)


ax1 = fig.add_subplot(133, projection="3d")     

cmap = plt.cm.get_cmap("hsv") 
ax1.plot_surface(kx_mesh,ky_mesh,VBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)
ax1.plot_surface(kx_mesh,ky_mesh,CBM_mesh,alpha=0.7,rstride=1,cstride=1,cmap=cmap,lw=0)

ax1.contourf(kx_mesh,ky_mesh,CBM_mesh,zdir='z',offset=0,cmap=cmap)

ax1.set_xlabel(r'$\mathbf{k}_{x}$',fontdict=font)
ax1.set_ylabel(r'$\mathbf{k}_{y}$',fontdict=font)
ax1.set_zlabel(r'$Energy (eV)$',fontdict=font)
ax1.set_zlim((-5,5))
ax1.view_init(elev=5, azim=45)

fig = plt.gcf()
fig.set_size_inches(8,6)

plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
#plt.show()
plt.savefig('3D.png',dpi=300,pad_inches = 0)
