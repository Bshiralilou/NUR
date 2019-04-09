#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def integral( a, b, c, xlim = 5.):
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


# Parameter values to calculate the integral
interv_a = np.array([1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2., 2.1, 2.2, 2.3, 2.4, 2.5])
interv_b = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1., 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.])
interv_c = np.array([1.5, 1.6, 1.7, 1.8, 1.9, 2., 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, \
                     3., 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.])

f=open('2h.txt','w')
    
for a in interv_a:
    for b in interv_b:
        for c in interv_c:
            A = 1./(4.* np.pi* integral(a,b,c) )
            f.write('{},{},{},{} \n'.format(a,b,c,A) )
            
f.close()

# Trilinear interpolation

def trilinear(x, y, z):

    # Min coordinates of the grid
    min_a = 1.1
    min_b = 0.5
    min_c = 1.5
    delta = 0.1
    
    # Finding where in the grid the point (x,y,z) is located
    # We call it the grid cell
    pos_a = (x - min_a) / delta
    pos_b = (y - min_b) / delta
    pos_c = (z - min_c) / delta
    
    i_a = int(np.floor(pos_a))
    i_b = int(np.floor(pos_b))
    i_c = int(np.floor(pos_c))
    
    #Reading relevant parameters from file
    f = open('2h.txt', 'r')
    lines = tuple(f)
    
    # From this we can find the corner edge of the grid cell (a0, b0, c0)
    line_000 = lines[ 15*25*i_a + 25*i_b + i_c]  #reading the relevant line from the file and splitting it to its elements
    elements = line_000.split(",")
    a0 = float(elements[0])
    b0 = float(elements[1])
    c0 = float(elements[2])
    
    #finding the values of A at the (a0, b0, c0) grid cell point
    c000 = float(elements[-1])
    
    # We do the same for the rest of the edges but in a more compact way!  
    c100 = float(lines[15*25*(i_a+1) + 25*i_b     + i_c    ].split(",")[-1])
    c001 = float(lines[15*25*i_a     + 25*i_b     + (i_c+1)].split(",")[-1])
    c101 = float(lines[15*25*(i_a+1) + 25*i_b     + (i_c+1)].split(",")[-1])
    c010 = float(lines[15*25*i_a     + 25*(i_b+1) + i_c    ].split(",")[-1])
    c110 = float(lines[15*25*(i_a+1) + 25*(i_b+1) + i_c    ].split(",")[-1])
    c011 = float(lines[15*25*i_a     + 25*(i_b+1) + (i_c+1)].split(",")[-1])
    c111 = float(lines[15*25*(i_a+1) + 25*(i_b+1) + (i_c+1)].split(",")[-1])
    
    # finding local coordinates of the point within the grid cell. We need this for the interpolation
    l_a = (pos_a - a0) + min_a
    l_b = (pos_b - b0) + min_b
    l_c = (pos_c - c0) + min_c
    
    #Interpolating along x
    c00 = c000*(1.-l_a) + c100*l_a
    c01 = c001*(1.-l_a) + c101*l_a
    c10 = c010*(1.-l_a) + c110*l_a
    c11 = c011*(1.-l_a) + c111*l_a
    #Interpolating along y
    c0 = c00*(1.-l_b) + c10*l_b
    c1 = c01*(1.-l_b) + c11*l_b
    #Interpolating along z
    c = c0*(1.-l_c) + c1*l_c
    
    return c