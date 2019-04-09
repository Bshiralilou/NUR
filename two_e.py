#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from two_d import sat_pos

f = open('integral_2a.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])
A=float(lines[3])

#----- Generating the positions catalog for 1000 halos
n_halo = 1000
positions = np.tile(np.nan,(0, 100, 3))     #A 3D array to store the satellites positions for all halos.

for i in range(n_halo):
    positions = np.pad(positions, ((0,1),(0,0),(0,0)), 'constant', constant_values= np.nan)
    
    #Calling the function from part 2.d for each halo:
    positions[-1,:,:] = sat_pos(A, a, b, c, size=100)
    
#----- Generating the log-log plot and the histogram

n = lambda xx: A*4*np.pi* xx**(2.)*(xx/b)**(a-3.)*np.exp(-(xx/b)**c)
m = np.linspace(1e-4,5.,100)
plt.loglog( m, n(m), label='Distribution')

bins = np.logspace( np.log10(1e-4), np.log10(5.), 20)
hist , borders = np.histogram( positions[:,:,0], bins)
PDF = np.tile(np.nan, len(hist))
centers = np.tile( np.nan, len(hist) )

for i in range(len(hist)):
    PDF[i] = hist[i]/(100*1000)/(borders[i+1]-borders[i])
    centers[i] = 0.5 * (borders[i+1] + borders[i])

plt.loglog( centers, PDF, label='Histogram')
plt.legend()
plt.xlabel('log(x)')
plt.ylabel('log p(x)')
plt.savefig('./Plots/hist_2e.png')
plt.show()
  