#!/usr/bin/python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib as mpl
mpl.use('Agg') #silent mode
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

group_labels=[]
x=[]

with open("KLABELS",'r') as reader:
    lines=reader.readlines()[1:]
for i in lines:
    s=i.encode('utf-8')#.decode('latin-1')
    if len(s.split())==2 and not s.decode('utf-8','ignore').startswith("*"):
        group_labels.append(s.decode('utf-8','ignore').split()[0])
        x.append(float(s.split()[1]))

#hsp=np.loadtxt(open("KLABELS", encoding='utf8'), dtype=np.string_,skiprows=1,usecols = (0,1))
df=np.loadtxt("BAND-REFORMATTED.dat",dtype=np.float64)

for index in range(len(group_labels)):
    if group_labels[index]=="GAMMA":
        group_labels[index]=u"Γ"

#except:
    #print("failed to open KLABELS containing High symmetry point!")



axe = plt.subplot(111)
axe.plot(df[:,0],df[:,1:],linewidth=1.0,color='blue')
font = {'family' : 'arial',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 13,  
        }  

#axe.set_xlabel(r'$\mathbf{k}$-points',fontsize=13)
axe.set_ylabel(r'${E}$-$E_{f}$ (eV)',fontdict=font)
axe.set_xticks(x)
plt.yticks(fontsize=10,fontname='arial')
#plt.yticks(fontdict=ticksfont)
axe.set_xticklabels(group_labels, rotation=0,fontsize=10,fontname='arial')
axe.axhline(y=0, xmin=0, xmax=1,linestyle= '--',linewidth=0.5,color='0.5')
for i in x[1:-1]:
	axe.axvline(x=i, ymin=0, ymax=1,linestyle= '--',linewidth=0.5,color='0.5')
axe.set_xlim((x[0], x[-1]))
plt.ylim((-15, 10)) # set y limits manually
fig = plt.gcf()
fig.set_size_inches(8,6)
#plt.show()
plt.savefig('band.png',dpi=1000)
