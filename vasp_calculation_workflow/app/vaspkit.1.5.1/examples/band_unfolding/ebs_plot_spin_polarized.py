#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #silent mode
mpl.rcParams['font.size'] = 13.
#mpl.rc('font',family='Times New Roman')
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
hsp=np.loadtxt("KLABELS", dtype=np.string_,skiprows=1,usecols = (0,1))
group_labels = hsp[:-1,0].tolist()
group_labels = [i.decode('utf-8','ignore') for i in group_labels]
for index in range(len(group_labels)):
	if group_labels[index]=="GAMMA":
		group_labels[index]=u"Γ"

x = [float(i) for i in hsp[:-1,1].tolist()]
lwd=0.2
op=0.8
scaler=20
fig= plt.figure(figsize=(8,6))

data=np.loadtxt("EBS_UP.dat")
kpt=data[:,0]                   # kpath 
eng=data[:,1]                   # energy level
wgt=data[:,2]*scaler            # weight, scaler is enlargement factor
ax = fig.add_subplot(111)
ax.scatter(kpt,eng,wgt,edgecolor = 'blue',alpha=op,label='Spin-up')

data=np.loadtxt("EBS_DW.dat")
kpt=data[:,0]                   # kpath
eng=data[:,1]                   # energy level
wgt=data[:,2]*scaler            # weight, scaler is enlargement factor
ax.scatter(kpt,eng,wgt,edgecolor = 'red',alpha=op,label='Spin-down')
ax.set_ylabel(r'$\mathrm{Energy}$ (eV)')

ax.set_ylim(-10,10)
ytick=np.arange(-10, 10.1, 2)
ax.legend(loc='best',shadow=False,labelspacing=0.1)
ax.set_xticks(x)
#plt.yticks(fontsize=10,fontname='arial')
ax.set_xticklabels(group_labels, rotation=0)
ax.axhline(y=0, xmin=0, xmax=1,linestyle= '-',linewidth=0.5,color='0.5')
for i in x[1:-1]:
	ax.axvline(x=i, ymin=0, ymax=1,linestyle= '-',linewidth=0.5,color='0.5')
ax.set_xlim((x[0], x[-1]))
#plt.show()
plt.savefig('EBS.pdf',dpi=1000)
