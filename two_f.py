#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

f = open('integral_2a.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])
A=float(lines[3])

def bisec( A, a, b, c, tol = 1e-7):
    # the distribution
    f = lambda xx: (A*xx**(2.)*(xx/b)**(a-3.)*np.exp(-(xx/b)**c)*4.*np.pi)
    
    x_max= b*((a-1.)/c)**(1./c)
    y_max=f(x_max)
    N=lambda xx: ((A*xx**(2.)*(xx/b)**(a-3.)*np.exp(-(xx/b)**c)*4.*np.pi) - (y_max/2.))*100
    
   # Bisection
   # We divide the algorithm in two search parts in order to get accurate results.
   # (of course we know in priori that there are two roots for this distribution)
    root_1 = 0. 
    root_2 = 0.
    
    # Initial points of search 1
    a_ = 1e-3
    b_ = x_max
    c_ = 0.5*(a_+b_)
  
    while (b_ - a_) > 2.*tol:
        if N(c_) == 0.:
            root_1 = c_
        elif N(a_)*N(c_) < 0.:
            b_ = c_
            c_ = 0.5*(a_+b_)
        elif N(a_)*N(c_) > 0.:
            a_ = c_
            c_ = 0.5*(a_+b_)
    root_1= c_
    #------------------------------
    # Initial points of search 2
    a_ = x_max
    b_ = 5.
    c_ = 0.5*(a_+b_)
  
    while (b_ - a_)> 2.*tol:
        if N(c_) == 0.:
            root_1 = c_
        elif N(a_)*N(c_) < 0.:
            b_ = c_
            c_ = 0.5*(a_+b_)
        elif N(a_)*N(c_) > 0.:
            a_ = c_
            c_ = 0.5*(a_+b_)
    root_2= c_
    
    return root_1, root_2
    
print("the roots are:", bisec( A, a, b, c))