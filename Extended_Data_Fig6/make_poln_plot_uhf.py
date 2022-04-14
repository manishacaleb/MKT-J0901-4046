#!/usr/env/python

import matplotlib as mp
import numpy as np
import matplotlib.pyplot as plt
import os,sys
import matplotlib.gridspec as gridspec
import matplotlib
import glob

# Set up plotting parameters
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

#read files and separate out all the Stokes parameters
files  = np.array([sys.argv[1], sys.argv[2]])
fig = plt.figure(figsize=(int(len(files)),2))
gs1 = gridspec.GridSpec(ncols = len(files), nrows=2, bottom=0.1, top=0.9, left= 0.08, right= 0.98, wspace=0.15, hspace=0.05, height_ratios=[1,3], width_ratios=[1,1])
ind = 0
for i in range(1):

 for k in range(2):

   data = np.loadtxt(files[ind], comments='File')

   phases = np.arange(0,1024)*(1.5/1024)
   StokesI = np.roll(data[:,0] - np.mean(data[900:1000,0]),0)
   StokesU = data[:,1]
   StokesQ = data[:,2]
   StokesV = np.roll(data[:,3] - np.mean(data[900:1000,3]),0)

   L = np.sqrt(pow(StokesU,2) + pow(StokesQ,2))
   L = np.roll(L - np.mean(L[900:1000]),0)
   V = StokesV

# Rotate the phase
   PA = np.roll(data[:,4],0)
   PA_err = np.roll(data[:,5],0)
   for j in range(len(PA)):
      if(PA[j] == 0):
          PA[j] = -180
   PA [PA_err == 0 ] = np.nan
#plot
   ax1 = fig.add_subplot(gs1[0 + 2*i, k])
   ind += 1
   ax1.errorbar(phases, PA, yerr=PA_err, fmt='k.', capsize=4, barsabove=True)
   ax1.set_title("737 MHz")
   plt.setp(ax1.get_xticklabels(), visible=False)
   if (k == 0):
     ax1.set_ylabel('PA ($^\circ$)')
   if ( k!=0 and i == 0):
     ax1.set_yticklabels([])
   if( k!=0 and i==1):
     ax1.set_yticklabels([])
     ax1.set_xlim(0.2, 1.2)
   ax2 = fig.add_subplot(gs1[1 + 2*i, k], sharex=ax1)
   ax2.plot(phases, StokesI,'k-')
   ax2.plot(phases, L, 'r-')
   ax2.plot(phases,V, 'b-')
   if (k ==0):
     ax2.set_ylabel('Flux (arb units)')
   if (k != 0 and i == 0):
     ax2.set_yticklabels([])
     ax2.set_xlim(0.15,1.1)
     ax2.set_xlabel('Time (s)')
   else:
     ax2.set_xlabel('Time (s)')
     ax2.set_xlim(0.37,1.3)

plt.show()
