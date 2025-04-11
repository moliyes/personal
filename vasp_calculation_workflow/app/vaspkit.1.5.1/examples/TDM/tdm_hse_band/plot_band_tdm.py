#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #silent mode
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
#------------------ FONT_setup ----------------------
font = {'family' : 'arial', 
    'color'  : 'black',
    'weight' : 'normal',
    'size' : 13.0,
    }

#------------------- Data Read ----------------------
group_labels=[];xtick=[]
with open('KLABELS','r') as reader:
    lines=reader.readlines()[1:]
for i in lines:
    s=i.encode('utf-8')#.decode('latin-1')
    if len(s.split())==2 and not s.decode('utf-8','ignore').startswith('*'):
        group_labels.append(s.decode('utf-8','ignore').split()[0])
        xtick.append(float(s.split()[1]))
datas=np.loadtxt('REFORMATTED_BAND.dat',dtype=np.float64)
for index in range(len(group_labels)):
    if group_labels[index]=='GAMMA':
        group_labels[index]=u'Γ'

#--------------------- PLOTs ------------------------
fig = plt.figure(figsize=(4, 5))
gs1 = GridSpec(5, 1)
gs1.update(left=0.20, right=.9, wspace=0.50)
axe = plt.subplot(gs1[:-1, :])
axe.axhline(y=0, xmin=0, xmax=1,linestyle= '--',linewidth=0.5,color='0.5')
for i in xtick[1:-1]:
    axe.axvline(x=i, ymin=0, ymax=1,linestyle= '--',linewidth=0.5,color='0.5')
colormaps='blue'
axe.plot(datas[:,0],datas[:,1:]-0.2,linewidth=2.0,color=colormaps)
#axe.plot(datas[:,0],datas[:,1:]-0.2,marker='o',linewidth=2.0,color=colormaps)
#axe.scatter(datas[:,0],datas[:,1:]-0.2,color=colormaps)
axe.set_ylabel(r'$\mathrm{E}$-$\mathrm{E_{VBM}}$ (eV)',fontdict=font)
axe.set_xticks(xtick)
plt.yticks(fontsize=font['size']-2,fontname=font['family'])
axe.set_xticklabels(group_labels, rotation=0,fontsize=font['size']-2,fontname=font['family'])
axe.set_xlim((xtick[0], xtick[-1]))
plt.setp(axe.get_xticklabels(), visible=False)
plt.ylim((-2,  5)) # set y limits manually

axe = plt.subplot(gs1[-1, :])
tdm=np.loadtxt('TDM.dat',dtype=np.float64)
axe.axhline(y=0, xmin=0, xmax=1,linestyle= '--',linewidth=0.5,color='0.5')
for i in xtick[1:-1]:
    axe.axvline(x=i, ymin=0, ymax=1,linestyle= '--',linewidth=0.5,color='0.5')
colormaps='blue'
axe.plot(tdm[:,0],tdm[:,4],linewidth=2.0,color=colormaps)
axe.set_ylabel(r'$\mathrm{P}^2 (\mathrm{Debye}^2$)',fontdict=font)
axe.set_xticks(xtick)
plt.yticks(fontsize=font['size']-2,fontname=font['family'])
axe.set_xticklabels(group_labels, rotation=0,fontsize=font['size']-2,fontname=font['family'])
axe.set_xlim((xtick[0], xtick[-1]))
plt.ylim((0, 400)) # set y limits manually
#plt.tight_layout()
plt.savefig('band_tdm.pdf',dpi= 300)
