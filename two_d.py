#!/usr/bin/env python
import numpy as np
from one_b import rand

f = open('integral_2a.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])
A=float(lines[3])

def sat_pos( A, a, b, c, size = 100):

    prob = lambda xx: A*xx**(a-1.)/(b**(a-3.))*np.exp(-(xx/b)**c)*(4.*np.pi)   #p(x)dx
    
    x_max = b * ( (a - 1.)/c )**(1./c)  # The maximum x of the distribution found analytically
    p_max = prob(x_max)           # The maximum value of the distribution given x_max
    # We use P_max to put an upper bound for the rejection sampling below
        
 
    pos = np.tile(np.nan, (0,3))   # An array to store samples in it.

    while len(pos[:,0]) < size:
        #the loop goes on until 100 samples are accepted 
        x_sat = 5. * rand()        #uniform sampling in [0,5)
        y_sat = p_max * rand()     #uniform sampling in [0,p_max)
        
        if y_sat <= prob(x_sat) :
            pos = np.pad(pos , ((0,1),(0,0)) ,'constant', constant_values = np.nan)
            pos[-1,0] = x_sat
            # Sampling phi and theta, respectively
            pos[-1,1] = 2.*np.pi*rand()    
            pos[-1,2] = np.arccos(1-2*rand())
            
    np.savetxt('satellites_2d.txt', pos )

    return pos

pos100 = sat_pos(A,a,b,c)

