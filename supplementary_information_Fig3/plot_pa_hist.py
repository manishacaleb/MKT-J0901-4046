#!/usr/env/python

import numpy as np
import matplotlib.pyplot as plt
import sys,os
import glob
import matplotlib.gridspec as gridspec
import matplotlib


# Set up plot paramters
def init_tex(fontsize):
    # set plotting font properties
    font = {"family": "sans serif",
        "weight": "regular",
        "size": fontsize}

    params = {
          "font.size": 13,
          "font.weight": "normal",
          "xtick.major.size": 3.5,
          "xtick.minor.size": 1.5,
          "ytick.major.size": 3.5,
          "ytick.minor.size": 1.5,
          "xtick.major.width": 1.5,
          "xtick.minor.width": 2.0,
          "ytick.major.width": 1.5,
          "ytick.minor.width": 2.0,
          "lines.linewidth": 1.5,
          "lines.markersize": 5,
          "axes.linewidth": 1.2,
          "legend.loc": "best",
          "text.usetex": False,
          "xtick.labelsize" : 10,
          "ytick.labelsize" : 10,
          }
    plt.rc("font", **font)
    matplotlib.rcParams.update(params)


init_tex(18)

# get all the files
files1  = sorted(glob.glob("*2021-02-01*.cen_stokes_corr.txt"))
files2  = sorted(glob.glob("*2021-04-02*.cen_stokes_corr.txt"))
files = np.append(files1,files2)
phases = np.arange(0,1024)*(1.5/1024)
ind = 0
index = 0

# Set up grid spec config
fig = plt.figure(figsize=(1,2))
gs1 = gridspec.GridSpec(ncols = 1, nrows=2, bottom=0.1, top=0.9, left= 0.08, right= 0.98, wspace=0.15, hspace=0.05, height_ratios=[2,1], width_ratios=[1])


# Generate the PA histogram
tot = np.zeros((len(files), 1024))
PA_fin = np.zeros((10,1024))
for i in range(len(files)):
  data = np.loadtxt(files[i])
  StokesI = np.roll(data[:,3],300)
  tot[i,:] = StokesI


for j in range(1024):
    PA_sum = np.zeros(1)
    ind = 0
    for i in range(len(files)):
       data = np.loadtxt(files[i])
       PA = np.roll(data[:,7],300)
       PA_err = np.roll(data[:,8],300)
       PA [PA_err == 0.0] = np.nan
       PAs = PA[j]
       if (ind == 0):
         PA_sum = PAs
         ind = 1
       else:
         PA_sum = np.append(PA_sum, PAs)

    freqs, bins = np.histogram(PA_sum, bins=10, range=(-120,120))
    PA_fin[:,j] =freqs[::-1]

ax1 = fig.add_subplot(gs1[0,0])
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.imshow(PA_fin, aspect='auto', extent=(0, 1.5, -120.0, 120.0),cmap='YlGnBu_r', interpolation='bicubic')
ax1.set_ylabel("PA ($^\circ$)")
ax2 =fig.add_subplot(gs1[1,0], sharex=ax1)
ax2.plot(phases, np.mean(tot, axis=0))
ax2.set_ylabel("Power (arb. units)")
ax2.set_xlabel("Time (s)")
plt.tight_layout()
plt.show()


