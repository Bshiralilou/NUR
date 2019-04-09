#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

f = open('integral_2a.txt', 'r')
lines = tuple(f)
a=float(lines[0])
b=float(lines[1])
c=float(lines[2])
A=float(lines[3])

def interpolate( x, y, xi):
    
    n = len(x)
    dx = np.diff(x)
    m = np.diff(y) / dx      # The slope between points
    
    # Adding two points to the left and two to the right 
    m1 = 2.0 * m[0] - m[1]
    m2 = 2.0 * m1 - m[0]
    m3 = 2.0 * m[n - 2] - m[n - 3]
    m4 = 2.0 * m3 - m[n - 2]
    # All the points for the interpolation
    m_all = np.concatenate(([m2], [m1], m, [m3], [m4]))
    
    # Deriving the parameters of the interpolation
    dm = np.abs(np.diff(m_all))
    f1 = dm[2:n + 2]
    f2 = dm[0:n]
    f12 = f1 + f2 
    # b = slope at points
    ids = np.nonzero(f12 > 1e-9 * np.max(f12))[0]
    b = m_all[1:n + 1]

    b[ids] = (f1[ids] * m_all[ids + 1] + f2[ids] * m_all[ids + 2]) / f12[ids]
    # Higher order parameters
    c = (3.0 * m - 2.0 * b[0:n - 1] - b[1:n]) / dx
    d = (b[0:n - 1] + b[1:n] - 2.0 * m) / dx ** 2

    bins = np.digitize(xi, x)
    bins = np.minimum(bins, n - 1) - 1
    bb = bins[0:len(xi)]
    wj = xi - x[bb]

    return ((wj * d[bb] + c[bb]) * wj + b[bb]) * wj + y[bb]

#----- Generating the plot

n = lambda x: A*100.*(x/b)**(a-3.)*np.exp(-(x/b)**c)
X = np.array([1e-4, 1e-2, 1e-1, 1., 5.])
Y = n(X)
x_new = np.linspace( -4, np.log10(5), 100)
y_new = interpolate( np.log10(X), np.log10(Y), x_new)
plt.scatter(np.log10(X), np.log10(Y))
plt.plot(x_new, y_new)
plt.xlabel('x')
plt.ylabel('logn(x)')
plt.savefig('./Plots/interp_2b.png')
plt.close()
