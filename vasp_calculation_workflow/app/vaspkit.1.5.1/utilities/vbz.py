#!/usr/bin/python -u
# -*- coding: utf-8 -*-
# Copyright 2020 Vei WANG <wangvei@icloud.com>
# Updated: 2020/08/20
# Updated: 2021/01/21, Added 3D plot axes to equal scale
# Updated: 2021/05/26, Improved the display effect
# Updated: 2022/09/29, Fixed a bug in Axes3Dsubplot
import os
import numpy as np, numpy.linalg as npl
import linecache
from scipy.spatial import Voronoi
from itertools import product
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib import cm
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
mpl.rcParams['font.size'] = 14.
plt.rcParams["font.serif"] = "Times New Roman"
plt.rcParams['axes.labelweight'] = 'bold'

def read_poscar(poscar, species=None):
    try:
        poscar = open(poscar,'r')
    except IOError:
        print(" Error: The " + str(poscar) + " file NOT found!")
        exit()
    title = poscar.readline().strip()
    scale = float(poscar.readline().strip())
    s = float(scale)
    lattice_vectors = [[ float(v) for v in poscar.readline().split() ],
            [ float(v) for v in poscar.readline().split() ],
            [ float(v) for v in poscar.readline().split() ]]
    lattice_vectors = np.array(lattice_vectors)*s
    lattice_vectors_2D = lattice_vectors[0:2,0:2]*s
    reciprocal_lattice_vectors= np.linalg.inv(lattice_vectors).T
    reciprocal_lattice_vectors=reciprocal_lattice_vectors*np.pi*2
    reciprocal_lattice_vectors_2D= np.linalg.inv(lattice_vectors_2D).T
    reciprocal_lattice_vectors_2D=reciprocal_lattice_vectors_2D*np.pi*2
    return reciprocal_lattice_vectors, reciprocal_lattice_vectors_2D

def read_high_symmetry_points():                  
    try:
        hpts_file = open("HIGH_SYMMETRY_POINTS",'r') 
    except IOError:
        print(" Error: The HIGH_SYMMETRY_POINT file NOT found!")
        exit()
    read_htps=hpts_file.readline()                      
    n=0                                  
    hpts=[]                              
    while True:                          
        read_htps=hpts_file.readline()                  
        hpts.append(read_htps)                  
        n=n+1                            
        if read_htps.find('use') > 0:           
            break     
    hpts_file.close()                             
    kpts=[]                              
    klabels=[]                            
    for i in range(0,n-3):               
        kpts.append(hpts[i].split()[0:3])
        klabels.append(hpts[i].split()[3])
    kpts=np.array(kpts,dtype=np.float64)
    return kpts, klabels                

def is_greek_letter(klabels):                                                          
    Greek_alphabets=['Alpha','Beta','Gamma','Delta','Epsilon','Zeta','Eta','Theta','Iota',
    'Kappa','Lambda','Mu','Nu','Xi','Omicron','Pi','Rho','Sigma','Tau','Upsilon','Phi','Chi','Psi','Pega']                                  
    group_labels=[]                                                                    
    for i in range(len(klabels)):                                                      
        klabel=klabels[i]                                                              
        for j in range(len(Greek_alphabets)):                                          
            if (klabel.find(Greek_alphabets[j].upper())>=0):                           
                latex_exp=r''+'$\\'+str(Greek_alphabets[j])+'$'                        
                klabel=klabel.replace(str(Greek_alphabets[j].upper()),str(latex_exp))  
        if (klabel.find('_')>0):                                                       
           n=klabel.find('_')                                                          
           klabel=klabel[:n]+'$'+klabel[n:n+2]+'$'+klabel[n+2:]                        
        group_labels.append(klabel)                                                    
    klabels=group_labels                                                               
    return klabels         
    
def read_kpoints(kpoints_file='KPATH.in'):                                                
    try:                                                                               
         kpoints = open(kpoints_file,'r')                                                      
    except IOError:                                                                    
        print(' Error: The ' + str(kpoints_file) + ' file NOT found!')                        
        exit()	
    is_line_mode=linecache.getline(kpoints_file,3)
    if (is_line_mode.upper().find('L') < 0):
       print(' Error: The '+ str(kpoints_file) + 'file MUST be Line-Mode.')
       exit()
    is_reciprocal=linecache.getline(kpoints_file,4)
    if (is_reciprocal.upper().find('R') < 0):
       print(' Error: The k-points MUST be in reciprocal coordinates.')
       exit()
    kpoints = open(kpoints_file,'r')
    kpoints_lines = kpoints.readlines()
    n=len(kpoints_lines)-4
    kpaths=np.zeros((n,3),dtype=float)
    nkpaths=0
    for i in range(4,len(kpoints_lines)):
        if (kpoints_lines[i].strip()!=''):
           kpaths[nkpaths,:]=[float(x) for x in kpoints_lines[i].split()[0:3]]
           nkpaths=nkpaths+1
    kpaths=kpaths[0:nkpaths,:]
    return kpaths     
     
 
def get_Wigner_Seitz_BZ(reciprocal_lattice_vectors):                                              
    I = (np.indices((3, 3, 3)) - 1).reshape((3, 27))
    G = np.dot(reciprocal_lattice_vectors.T, I).T
    voronoi = Voronoi(G)                                                         
    bz = []        
    for pid, rid in zip(voronoi.ridge_points, voronoi.ridge_vertices):                 
        if -1 not in rid and 13 in pid:   
            normal = G[pid].sum(0)
            normal /= (normal**2).sum()**0.5  
            facets = voronoi.vertices[rid]  
            points = voronoi.vertices[rid]
            bz.append((points, normal, facets))                                                        
    return bz   

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.
    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(), ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)

def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])

def visualize_BZ_matplotlib(bz,reciprocal_lattice_vectors,kpts,klabels,kpaths):  
    fig = plt.figure()                                                                          
    fig.set_tight_layout(True)                                                                                
    ax = fig.add_subplot(111, projection='3d')                                                                    
    basis_vector_clrs = ['r', 'g', 'b']                                                                       
#    basis_vector_labs = [r'b$_1$', r'b$_2$', r'b$_3$']                                                        
    basis_vector_labs = [r'a*', r'b*', r'c*']
    for ii in range(3):                                                                                       
        arrow = Arrow3D([0,reciprocal_lattice_vectors[ii, 0]*0.9],                                                
                        [0,reciprocal_lattice_vectors[ii, 1]*0.9], [0,reciprocal_lattice_vectors[ii, 2]*0.9],         
                color=basis_vector_clrs[ii], mutation_scale=20,lw=1,arrowstyle='->')                          
        ax.add_artist(arrow)                                                                                  
        ax.text(reciprocal_lattice_vectors[ii, 0]*0.9, reciprocal_lattice_vectors[ii, 1]*0.9,                         
                reciprocal_lattice_vectors[ii, 2]*0.9, basis_vector_labs[ii],weight='bold')   
                                        
    elev0=12
    azim0=23
    ax.view_init(elev =elev0, azim=azim0)    
    elev0=elev0*np.pi/180
    azim0=azim0*np.pi/180
    x = np.sin(azim0)                                     
    y = np.cos(azim0)                                     
    view = [x * np.cos(elev0), y * np.cos(elev0), np.sin(elev0)]
    for points, normal, facets in bz:
        x, y, z = np.concatenate([points, points[:1]]).T    
        if np.dot(normal, view) < 0 :
            ls = ':'
        else:
            ls = '-'
        ax.plot(x, y, z, c='k', ls=ls, lw=1)
        polygon = Poly3DCollection([facets], alpha=0.03)                                              
        polygon.set_color('b')                                                                                
        ax.add_collection3d(polygon)                                                                                
    for i in range(len(klabels)):                                                                             
        kpt=np.dot(kpts[i,:],reciprocal_lattice_vectors)                                                      
        ax.scatter(kpt[0], kpt[1], kpt[2], c='b', marker='o', s=5, alpha=0.8)                                
        ax.text(kpt[0], kpt[1], kpt[2], klabels[i], c='k')                                                    
    for i in range(kpaths.shape[0]):                                                                          
        kpaths[i,:]=np.dot(kpaths[i,:],reciprocal_lattice_vectors)                                            
    for i in range(0,kpaths.shape[0],2):                                                                      
        arrow = Arrow3D([kpaths[i,0],kpaths[i+1,0]],[kpaths[i,1],kpaths[i+1,1]],                              
                        [kpaths[i,2],kpaths[i+1,2]],mutation_scale=12,lw=1.0,arrowstyle='->', color='magenta')
        ax.add_artist(arrow)                                                                                                                                                                                            
    ax.set_box_aspect([1,1,1])                                                                                
    set_axes_equal(ax)                                                                                        
    ax.set_axis_off()                                                                                         
    plt.tight_layout()                                                                                        
#    plt.show()
    plt.savefig('Brillouin_Zone_3D.pdf')
    
def welcome():
    print(' +-------------------------- Warm Tips --------------------------+')
    print(' | A VASPKIT Plugin to Visualize Brillouin Zone Using Matplotlib |')
    print(' |  First Generate HIGH_SYMMETRY_POINTS and PRIMCELL.vasp Files. |')
    print(' |  Do Remember to copy PRIMCELL.vasp to POSCAR unless you know  |')
    print(' |   what you are doing. Otherwise you might get wrong results!  |')
    print(' |  You can certainly use the customized k-Path in KPOINTS file. |')
    print(' +---------------------------------------------------------------+')
    
if __name__ == "__main__":   
   welcome()
   reciprocal_lattice_vectors, reciprocal_lattice_vectors_2D = read_poscar('POSCAR')   
   kpts,klabels = read_high_symmetry_points()
   klabels = is_greek_letter(klabels)
   kpaths = read_kpoints('KPOINTS')    
   bz = get_Wigner_Seitz_BZ(reciprocal_lattice_vectors) 
   visualize_BZ_matplotlib(bz,reciprocal_lattice_vectors,kpts,klabels,kpaths)
