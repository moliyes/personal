import numpy as np
import matplotlib as mpl
mpl.rcParams['font.size'] = 13.
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

fig = plt.figure(figsize=(14,5))
fig.tight_layout()
plt.subplots_adjust(wspace=0.35, hspace =0)
ax = fig.add_subplot(141)
optical=np.loadtxt("ABSORPTION.dat")
ax.plot(optical[:,0],optical[:,1],lw=3,color='blue')
plt.xlim(2, 6)
plt.xticks(np.arange(2, 6.1, 1))
plt.ylim(0, 2.5E6)
plt.xlabel("Photon energy (eV)")
plt.ylabel(r"Absorption coefﬁcient $\alpha(\omega)$ (cm$^{-1}$)")
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax = fig.add_subplot(142)
optical=np.loadtxt("REFRACTIVE.dat")
ax.plot(optical[:,0],optical[:,1],lw=3,color='blue')
plt.xlim(0, 8)
plt.xticks(np.arange(0, 8.1, 2))
plt.ylim(0, 8)
plt.yticks(np.arange(0, 8.1, 2))
plt.xlabel("Photon energy (eV)")
plt.ylabel(r"Refractive index $n(\omega)$")

ax = fig.add_subplot(143)
optical=np.loadtxt("REFLECTIVITY.dat")
ax.plot(optical[:,0],optical[:,1],lw=3,color='blue')
plt.xlim(0, 8)
plt.xticks(np.arange(0, 8.1, 2))
plt.ylim(0, .8)
plt.yticks(np.arange(0, 0.81, .2))
plt.xlabel("Photon energy (eV)")
plt.ylabel(r"Reflectivity $R(\omega)$")

ax = fig.add_subplot(144)
optical=np.loadtxt("EXTINCTION.dat")
ax.plot(optical[:,0],optical[:,1],lw=3,color='blue')
plt.xlim(0, 8)
plt.xticks(np.arange(0, 8.1, 2))
plt.ylim(0, 6)
plt.yticks(np.arange(0, 6.1, 1))
plt.xlabel("Photon energy (eV)")
plt.ylabel(r"Extinction coefficient $k(\omega)$")
plt.savefig('Optical.pdf',dpi=100)
