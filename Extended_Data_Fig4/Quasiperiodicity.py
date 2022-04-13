import numpy as np
import os
import glob
import argparse
import logging
import matplotlib
from matplotlib import rcParams
import matplotlib.pyplot as plt
from astropy.io import ascii
from scipy import signal
import os
import matplotlib.gridspec as gridspec
from astropy import units as u
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from astropy import constants as const

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
          "axes.linewidth": 1.4,
          "legend.loc": "best",
          "text.usetex": False,    
          "xtick.labelsize" : 12,
          "ytick.labelsize" : 12,
          }

import matplotlib
matplotlib.rcParams.update(params)

rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'




d = np.genfromtxt('QP_timescales.txt', dtype=str) 

UTs = d[:,0].astype(str)

smoothed_peak = d[:,1].astype(float) # convolved with 32
xerr_low = d[:,2].astype(float) # convolved with 32 
xerr_high = d[:,3].astype(float) # convolved with 32 

zipped_lists = zip(smoothed_peak, UTs)
sorted_pairs = sorted(zipped_lists)

tuples = zip(*sorted_pairs)
list1, list2 = [ list(tuple) for tuple in  tuples]

idx = np.linspace(1, len(smoothed_peak), len(smoothed_peak))


# Make the plot

fig, ax = plt.subplots(figsize=(7.5, 6))

# asymmetric_error = np.array([[xerr_low, xerr_high]]).T 

plt.plot(list1, idx, marker = 'o', color = '#FC8D59', ls='none', ms=6, mec='#A50F15', mew=2)

plt.yticks(idx, list2)
plt.xlabel('Time lag (ms)')
plt.ylabel('UTC')
ax.xaxis.set_minor_locator(MultipleLocator(5))

plt.tight_layout()
plt.grid()

plt.savefig("Quasiperiodicity.pdf")
