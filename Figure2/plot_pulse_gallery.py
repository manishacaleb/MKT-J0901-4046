#! /usr/bin/env python

import matplotlib.pyplot as plt
import psrchive
import numpy as np
import matplotlib.gridspec as gridspec

params = {
          "font.size": 12,
          "xtick.major.size": 6,
          "ytick.major.size": 6,
          "xtick.major.width": 2,
          "ytick.major.width": 2,
          "lines.linewidth": 1.3,
          "axes.linewidth": 2.0,
          "text.usetex": False,    
          "xtick.labelsize" : 12,
          "ytick.labelsize" : 12,
          }

import matplotlib
matplotlib.rcParams.update(params)

def plotspectrum(archive, t, chan):
	arch = psrchive.Archive_load(archive)
	arch.dedisperse()
	arch.remove_baseline()
	arch.fscrunch_to_nchan(chan)	
	
	freq_lo = arch.get_centre_frequency() - arch.get_bandwidth()/2.0
	freq_hi = arch.get_centre_frequency() + arch.get_bandwidth()/2.0
	data = arch.get_data()

	weights = arch.get_weights()
	profile = np.zeros((data.shape[2], data.shape[3]))

	# subintegration, polarization, channel, and profile bin.
	for i in range(data.shape[3]):
        	profile[:,i] = data[:,0,:,:].mean(0)[:,i] * weights

	plt.imshow(profile, cmap='PuRd', aspect='auto',extent=(-1.0*t, t, freq_hi, freq_lo))
#	plt.xlim(-0.5, 0.5)

def plot_timeseries(archive, t):
        arch = psrchive.Archive_load(archive)
        arch.dedisperse()
        arch.remove_baseline()
#	arch.bscrunch_to_nbin(512)	
        data = arch.get_data()
	weights = arch.get_weights()
	profile = np.zeros((data.shape[2], data.shape[3]))

	for i in range(data.shape[3]):
        	profile[:,i] = data[:,0,:,:].mean(0)[:,i] * weights

	time_series = np.average(profile, axis=0)
	time = np.linspace(-1.0*t, t, num=data.shape[3])
	plt.plot(time, time_series, 'k-')
	plt.xlim(-1.0*t, t)
#	plt.xlim(-0.5, 0.5)

fs = 11


fig = plt.figure(figsize=(15, 10))

gs2 = gridspec.GridSpec(2, 4, bottom=0.1, top=0.45, wspace=0.05, hspace=0.0,
                        height_ratios=[1, 3], width_ratios=[4, 4, 4, 4])



ax1 = fig.add_subplot(gs2[0, 0])
plot_timeseries('normal.ar', 4.02832029906798/2)
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])
ax1.text(10, 0.7, 'Normal', fontsize=fs)
ax1.set_title('Normal')
ax1.set_xlim(-1.0, 1.0)
ax5 = fig.add_subplot(gs2[1, 0])
plotspectrum('normal.ar', 4.02832029906798/2, 128)
#ax5.yaxis.set_ticks([])
#ax5.xaxis.set_ticks([])
ax5.set_xlim(-1.0, 1.0)
ax5.set_ylabel('Frequency (MHz)')
ax5.set_xlabel('Time (seconds)')

ax2 = fig.add_subplot(gs2[0, 1])
plot_timeseries('QP.ar', 1.2816149533/2)
ax2.text(10, 0.2, 'Quasi-periodic', fontsize=fs)
ax2.xaxis.set_ticks([])
ax2.yaxis.set_ticks([])
ax2.set_title('Quasi-periodic')
ax6 = fig.add_subplot(gs2[1, 1])
plotspectrum('QP.ar', 1.2816149533/2, 128)
#ax6.xaxis.set_ticks([])
ax6.yaxis.set_ticks([])
#ax6.set_ylabel('Frequency (MHz)')
ax6.set_xlabel('Time (seconds)')


ax3 = fig.add_subplot(gs2[0, 2])
plot_timeseries('spiky.ar', 1.55969555140286/2)
ax3.xaxis.set_ticks([])
ax3.yaxis.set_ticks([])
ax3.text(10, 0.5, 'Spiky', fontsize=fs)
ax3.set_title('Spiky')
ax3.set_xlim(-0.3, 0.3)
ax7 = fig.add_subplot(gs2[1, 2])
plotspectrum('spiky.ar', 1.55969555140286/2, 64)
ax7.yaxis.set_ticks([])
#ax7.xaxis.set_ticks([])
ax7.set_xlim(-0.3, 0.3)
ax7.set_xlabel('Time (seconds)')


gs1 = gridspec.GridSpec(2, 4, bottom=0.55, top=0.9, wspace=0.05, hspace=0.0,
                        height_ratios=[1, 3], width_ratios=[4, 4, 4, 4])

ax1 = fig.add_subplot(gs1[0, 0])
plot_timeseries('partially_nulling.ar', 2.24400564705893/2)
ax1.text(10, 0.5, 'Partially nulling', fontsize=fs)
ax1.xaxis.set_ticks([])
ax1.yaxis.set_ticks([])
ax1.set_title('Partially nulling')
ax1.set_xlim(-0.7, 0.7)
ax5 = fig.add_subplot(gs1[1, 0])
plotspectrum('partially_nulling.ar', 2.24400564705893/2, 128)
#ax5.yaxis.set_ticks([])
#ax5.xaxis.set_ticks([])
ax5.set_xlim(-0.7, 0.7)
ax5.set_ylabel('Frequency (MHz)')
#ax5.set_xlabel('Time (seconds)')


ax2 = fig.add_subplot(gs1[0, 1])
plot_timeseries('splitpeak.ar', 2.28641016822575/2)
ax2.xaxis.set_ticks([])
ax2.yaxis.set_ticks([])
ax2.text(10, 0.39, 'Split-peak', fontsize=fs)
ax2.set_title('Split-peak')
ax6 = fig.add_subplot(gs1[1, 1])
plotspectrum('splitpeak.ar', 2.28641016822575/2, 128)
ax6.yaxis.set_ticks([])
#ax6.xaxis.set_ticks([])
#ax6.set_xlabel('Time (seconds)')

ax3 = fig.add_subplot(gs1[0, 2])
plot_timeseries('threepeaks.ar', 1.55081788235302/2)
ax3.xaxis.set_ticks([])
ax3.yaxis.set_ticks([])
ax3.text(10, 0.07, 'Three peaks', fontsize=fs)
ax3.set_title('Three peaks')
ax3.set_xlim(-0.6, 0.6)
ax7 = fig.add_subplot(gs1[1, 2])
plotspectrum('threepeaks.ar', 1.55081788235302/2, 64)
ax7.yaxis.set_ticks([])
#ax7.xaxis.set_ticks([])
ax7.set_xlim(-0.6, 0.6)
#ax7.set_xlabel('Time (seconds)')


ax4 = fig.add_subplot(gs1[0, 3])
plot_timeseries('double_peak.ar', 2.68095247058837/2)
ax4.xaxis.set_ticks([])
ax4.yaxis.set_ticks([])
ax4.text(10, 0.7, 'Double-peak', fontsize=fs)
ax4.set_title('Double-peak')
ax4.set_xlim(-0.5, 0.5)
ax8 = fig.add_subplot(gs1[1, 3])
plotspectrum('double_peak.ar', 2.68095247058837/2, 128)
ax8.yaxis.set_ticks([])
#ax8.xaxis.set_ticks([])
ax8.set_xlim(-0.5, 0.5)

plt.tight_layout()

plt.show()

#plt.savefig('MTP0013_pulse_gallery_BuGn.png', dpi=500)


