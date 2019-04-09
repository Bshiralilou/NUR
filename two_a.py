#!/usr/bin/env python
import numpy as np

f = open('random.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])

def integ( a, b, c, xlim = 5.):
    # Defining the number density function as f(x)
    f = lambda x: x**(a-1)/(b**(a-3.))*np.exp(-(x/b)**c)
    # f(x) = n(x)*x**2
    
    # Defining the Romberg integration
    n = 10
    lim1 = 0.    # Lower integration limit
    lim2 = xlim  # Upper integration limit
    h0 = (lim2-lim1)/(2.**n)  # The smallest integral step
    
    F = np.tile(np.nan, 2**n + 1)
    for i, F_i in enumerate(F):
        F[i] = f(lim1 + h0*i)
        
    # Making an n*n grid for the Riemann sums
    R = np.tile( np.nan, (n,n))
    for j in range(n):
        # The first column
        if j == 0:
            for i in range(0,n):
                h = h0 * 2**(n-i)
                R[i,j] = h * np.sum(F[0:2**n :2**(n-i)]) - 0.5*h*(F[0]+F[2**n])
        # The other columns 
        else:
            for i in range(j,n):
                R[i,j] = (4.**j * R[i, j-1] - R[i-1, j-1])/(4.**j-1.)
    
    
    return R[n-1,n-1]

A = 1./(4.* np.pi* integ(a,b,c) )
print('a = {}, b = {}, c = {}, A = {}'.format(a,b,c,A)) 
np.savetxt('integral_2a.txt', np.array([a,b,c,A]))