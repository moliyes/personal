import numpy as np
from matplotlib import pyplot as plt
import linecache  
import matplotlib as mpl

def read_poscar(poscar, species=None):
    poscar = open(poscar,'r')
    title = poscar.readline().strip()
    scale = float(poscar.readline().strip())
    s = float(scale)
    lattice_vectors = [[ float(v) for v in poscar.readline().split() ],
            [ float(v) for v in poscar.readline().split() ],
            [ float(v) for v in poscar.readline().split() ]]
    lattice_vectors = np.array(lattice_vectors)*s
    lattice_vectors_2D=lattice_vectors[0:2,0:2]
    reciprocal_lattice_vectors_2D= np.linalg.inv(lattice_vectors_2D).T*np.pi*2
    reciprocal_lattice_vectors= np.linalg.inv(lattice_vectors).T*np.pi*2
    return reciprocal_lattice_vectors,reciprocal_lattice_vectors_2D

def get_primitive_cell_2d(lattice_vectors):
    lattice_vectors = np.asarray(lattice_vectors, dtype=float)
    assert lattice_vectors.shape == (2, 2)

    dx, dy = np.mgrid[0:2, 0:2]
    dxyz = np.c_[dx.ravel(), dy.ravel()]
    px, py = np.tensordot(lattice_vectors, [dx, dy], axes=[0, 0])
    points = np.c_[px.ravel(), py.ravel()]

    lines = []
    faces = None

    for ii in range(len(points)):
        for jj in range(ii):
            if np.abs(dxyz[ii] - dxyz[jj]).sum() == 1:
                lines.append(np.vstack([points[ii], points[jj]]))
    return points, lines, faces

def read_spin_texture_2D(datafile='SPINTEXTURE_2D_GAMMA_CENTER.dat'):
    data=np.loadtxt(datafile)    
    kx=data[:,0]
    ky=data[:,1]
    sx=data[:,3]
    sy=data[:,4]
    sz=data[:,5]
    for i in range(sx.shape[0]):
        norm=np.sqrt(sx[i]*sx[i]+sy[i]*sy[i])
        if (norm > 0.01):
           sx[i]=sx[i]/norm
           sy[i]=sy[i]/norm    	   	
           sz[i]=sz[i]/sz.max()
    return kx, ky, sx, sy, sz

reciprocal_lattice_vectors,reciprocal_lattice_vectors_2D=read_poscar('POSCAR')
points, lines, faces=get_primitive_cell_2d(reciprocal_lattice_vectors_2D)
kx, ky, sx, sy, sz=read_spin_texture_2D("SPINTEXTURE_2D_GAMMA_CENTER.dat")
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.axis('equal')
norm= mpl.colors.Normalize(sz.min(), sz.max())
icmap='hsv'
tk = np.linspace(sz.min(), sz.max(), 5, endpoint=True)
sm = mpl.cm.ScalarMappable(cmap=icmap, norm=norm)
plt.colorbar(sm, ticks = tk, shrink = 0.5, format='%.2f')
ax.quiver(kx,ky,sx,sy,sz,width=0.003, scale=10, pivot='mid', scale_units='inches', cmap=icmap, norm=norm)      


#ax.quiver(kx,ky,sx,sy,sz,width=0.002, scale=10, scale_units='inches')

#import matplotlib.transforms as mtransforms
#krange = 1.0
#origin = [-krange/2,-krange/2]
#test=np.reshape(sz,(30,30))
#im = ax.imshow(test,
#               extent=[origin[0],krange/2,origin[1],krange/2],
#               aspect=1,interpolation='lanczos',origin='lower')
#               
#trans_data = mtransforms.Affine2D().skew_deg(-15, -15).rotate_deg(-15) + ax.transData
#im.set_transform(trans_data)
#              
x0=sum(points[:, 0])/points.shape[0]
y0=sum(points[:, 1])/points.shape[0]

for l in lines:
    ax.plot(l[:, 0]-x0, l[:, 1]-y0, color='k', lw=1.0)
    ax.scatter(0,0,2,color='k')
    ax.text(0, 0,r'$\Gamma$',c='k',fontsize=15)
plt.savefig('SPINTEXTURE_2D_GAMMA_CENTER.pdf',dpi=400)
