#!/usr/env/python

import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt
import os,sys
import matplotlib.gridspec as gridspec
import matplotlib
import glob

def init_tex(fontsize):
    # set plotting font properties
    font = {"family": "sans serif",
        "weight": "regular",
        "size": fontsize}

    params = {
          "font.size": 13,
          "font.weight": "normal",
          "xtick.major.size": 5,
          "xtick.minor.size": 3,
          "ytick.major.size": 5,
          "ytick.minor.size": 2,
          "xtick.major.width": 2.5,
          "xtick.minor.width": 3,
          "ytick.major.width": 2.5,
          "ytick.minor.width": 3,
          "lines.linewidth": 1.5,
          "lines.markersize": 7,
          "axes.linewidth": 2.0,
          "legend.loc": "best",
          "text.usetex": False,    
          "xtick.labelsize" : 12,
          "ytick.labelsize" : 12,
          }
    plt.rc("font", **font)
    matplotlib.rcParams.update(params)

init_tex(18)


# Read data
files  = np.array([sys.argv[1], sys.argv[2]])
fig = plt.figure(figsize=(2,len(files)))

gs1 = gridspec.GridSpec(ncols = len(files), nrows=2, bottom=0.1, top=0.9, left= 0.08, right= 0.98, wspace=0.15, hspace=0.0, height_ratios=[1,3], width_ratios=[1,1])
ind = 0
for i in range(1):

 for k in range(2):

   data = np.loadtxt(files[ind], comments='File')

   phases = np.arange(0,1024)*(1.5/1024)
   StokesI = np.roll(data[:,3] - np.mean(data[900:1000,0]),100)
   StokesU = data[:,4]
   StokesQ = data[:,5]
   StokesV = np.roll(data[:,6] - np.mean(data[900:1000,3]),100)

   L = np.sqrt(pow(StokesU,2) + pow(StokesQ,2))
   L = np.roll(L - np.mean(L[900:1000]),100)
   V = StokesV

# Rotate the phase
   PA = np.roll(data[:,7],100)
   PA_err = np.roll(data[:,8],100)
   for j in range(len(PA)):
      if(PA[j] == 0):
          PA[j] = -180
   PA [PA_err == 0 ] = np.nan
#plot
   ax1 = fig.add_subplot(gs1[0 + 2*i, k])
   ind += 1
   ax1.errorbar(phases, PA, yerr=PA_err, fmt='k.', capsize=4, barsabove=True)
   ax1.set_title("1284 MHz")
   plt.setp(ax1.get_xticklabels(), visible=False)
   if (k == 0):
     ax1.set_ylabel('PA ($^\circ$)')
   if ( k!=0 and i == 0):
     ax1.set_yticklabels([])
   if( k!=0 and i==1):
     ax1.set_yticklabels([])
   ax1.set_xlim(0.05, 1.1)
   ax2 = fig.add_subplot(gs1[1 + 2*i, k], sharex=ax1)
   ax2.plot(phases, StokesI,'k-')
   ax2.plot(phases, L, 'r-')
   ax2.plot(phases,V, 'b-')
   if (k ==0):
     ax2.set_ylabel('Flux (arb units)')
   if (k != 0 and i == 0):
     ax2.set_yticklabels([])
   elif(k !=0 and i==1):
     ax2.set_yticklabels([])
   ax2.set_xlabel('Time (s)')
   ax2.set_xlim(0.05,1.1)

plt.tight_layout()
plt.show()
