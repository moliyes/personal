#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #silent mode
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

with open("PDOS_USER.dat",'r') as reader:
	legend = reader.readline()
legends=legend.split()[1:]
legends=[i.replace('_',' ') for i in legends]
legend_s=tuple(legends)

df=np.loadtxt("PDOS_USER.dat",dtype=np.float64,skiprows=1)

axe = plt.subplot(111)
axe.plot(df[:,0],df[:,1:],linewidth=1.0)

font = {'family' : 'arial',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 13,  
        }  

axe.set_xlabel(r'${E}$-$E_{f}$ (eV)',fontdict=font)
axe.set_ylabel(r'PDOS (states/eV)',fontdict=font)

plt.yticks(fontsize=10,fontname='arial')

plt.legend(legend_s,loc='best')
leg = plt.gca().get_legend() 
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12) 

#plt.xlim((-15, 10)) # set x limits manually
#plt.ylim((-15, 10)) # set y limits manually

fig = plt.gcf()
fig.set_size_inches(8,6)
#plt.show()
plt.savefig('DOS.png',dpi=1000)
