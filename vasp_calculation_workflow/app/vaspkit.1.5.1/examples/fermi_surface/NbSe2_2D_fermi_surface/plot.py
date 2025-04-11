import numpy as np
from matplotlib import pyplot as plt
import linecache

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
    """
    Get the vertices, lines and facets of the primitive cell.
    """
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

def read_fermi_surface_2D(fname,reciprocal_lattice_vectors_2D):
    data=np.loadtxt(fname)   
    gamma_centered = linecache.getline(fname, 3).split()[1]
    kgrid_2d=np.matmul(data[:,0:2],reciprocal_lattice_vectors_2D)
    kx=data[:,0]
    ky=data[:,1] 
    kx=kgrid_2d[:,0]        
    ky=kgrid_2d[:,1]        
    return kx, ky, gamma_centered

scaler=5
reciprocal_lattice_vectors,reciprocal_lattice_vectors_2D=read_poscar('POSCAR')
points, lines, faces=get_primitive_cell_2d(reciprocal_lattice_vectors_2D)
kx, ky, gamma_centered=read_fermi_surface_2D("FERMI_SURFACE_2D.dat",reciprocal_lattice_vectors_2D)
fig = plt.figure(figsize=(5,5))
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.axis('equal')
x0=sum(points[:, 0])/points.shape[0]
y0=sum(points[:, 1])/points.shape[0]
for l in lines:
    if (gamma_centered == 'F'):
       ax.plot(l[:, 0], l[:, 1], color='k', lw=1.0)
    else:
       ax.plot(l[:, 0]-x0, l[:, 1]-y0, color='k', lw=1.0)
       ax.scatter(0,0,10,color='k')
       ax.text(0, 0,r'$\Gamma$',c='k',fontsize=12)
ax.scatter(kx,ky,scaler,color='blue',alpha=0.8)
plt.savefig('FERMI_SURFACE_2D.pdf',dpi=400)
