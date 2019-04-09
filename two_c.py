#!/usr/bin/env python
import numpy as np

f = open('integral_2a.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])
A=float(lines[3])

def ridder (A, a, b, c, x):
    #defining the number density function
    N_sat=100.
    f=lambda xx: N_sat*A*(xx/b)**(a-3.)*np.exp(-(xx/b)**c) #f=lambda xx: xx**2
   
    #defining the Ridder differentiation
    n = 2        # The initial n for differentiation
    h0 = 8.5e-4  # The optimized value for h0 
    R = np.tile(np.nan, (n,n))
    
    # The first differentiation    
    R[0,0] = 0.5 * (f(x +h0) - f(x-h0)) / h0
    h = h0/2.
    R[0,1] = 0.5 * (f(x +h) - f(x-h)) / h
    R[1,0] = (4. * R[0, 1] - R[0, 0])/(4.-1.)
    
    # Generating higher order differentials by checking the relative error
    while h0**(2*(n-2)) > np.absolute(R[n-1,0] - R[n-2,0]):
        n += 1
        R = np.pad( R, ((0,1),(0,1)), 'constant', constant_values = np.nan)
        h = h0/2**(n-1)
        R[0,n-1] = 0.5 * (f(x+h) - f(x-h)) / h

        for k in range(1,n):
            i = k
            j = n-i-1
            R[i,j] = (4.**i * R[i-1, j+1] - R[i-1, j])/(4.**i - 1.)
    
    return R[n-1,0]

numerical = ridder(A,a,b,c,b)
analytical = 100.*A*(a - c -3.)/(b * np.e)
print("analytical:",analytical,"numerical:",numerical)
np.savetxt('df_2c.txt', np.array([numerical, analytical]) )
