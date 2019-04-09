#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from two_h import trilinear

#----- Loglikelihood
def LL (A, a, b, c, x = 1):
    # calculation of -log(likelihood) from distribution in eq.2
    
    logL = np.log10(A) + (a - 3.)*np.log10(x) - (a + 3.)*np.log10(b) - (x/b)**c
    
    return -logL


#----- Gradient of loglikelihood
def gradient( a_init, b_init, c_init, x = 1):
    
    # We need derivatives of A w.r.t (a, b, c)
    # Calling the interpolation function from 2.h
    A = trilinear(a_init, b_init, c_init)
    
    # Using the basic definition of differentiation
    h0= 1e-2  # step size for differentiation
    A_a = (trilinear(a_init-h0, b_init, c_init) - trilinear(a_init+h0, b_init, c_init))/(2.*h0)
    A_b = (trilinear(a_init, b_init-h0, c_init) - trilinear(a_init, b_init+h0, c_init))/(2.*h0)
    A_c = (trilinear(a_init, b_init, c_init-h0) - trilinear(a_init, b_init, c_init+h0))/(2.*h0)
    
    # Gradient values, calculated analytically
    d_a = A_a/A + np.log10(x/b_init)
    d_b = A_b/A - (a_init + 3.)/b_init - (c_init/b_init)*(x/b_init)**c_init
    d_c = A_c/A + np.log10(x/b_init)*(x/b_init)**c_init
    
    return np.array([d_a, d_b, d_c])
    
    
#----- The function that needs to get minimized to find step size alpha
def g_alpha (alpha, a, b, c, d):

    alpha1, alpha2, alpha3 = alpha
    A = trilinear( a + alpha1, b + alpha2, c + alpha3)
    
    return LL(A, a+alpha1*d[0], b+alpha2*d[1], c+alpha3*d[2] )
    

#----- Conjugate gradient method for minimization of -logL
def CG(a_init, b_init, c_init, tol = 1e-2):
    
    # Initial calculation of gradient --> initial direction
    a_0 = a_init
    b_0 = b_init
    c_0 = c_init
    d = -1. * gradient( a_0, b_0, c_0)
    gamma = 0.          # Polak- Ribiere choice for gamma0
    
    # Calculating optimized alpha with an initial guess
    # alpha --> step size
    initial = np.array([1e-4,1e-4,1e-4])
    alpha_opt = optimize.minimize( g_alpha, initial, args =(a_0, b_0, c_0, d))
    alpha = alpha_opt.x
    
    # Next best values for parameters
    a_1 = a_0 + alpha[0]*d[0]
    b_1 = b_0 + alpha[1]*d[1]
    c_1 = c_0 + alpha[2]*d[2]
    
    # Defining a condition to check for convergence
    A_0 = trilinear(a_0, b_0, c_0)
    A_1 = trilinear(a_1, b_1, c_1)
                          
    cond_num = abs( LL(A_1, a_1, b_1, c_1) - LL(A_0, a_0, b_0, c_0) )
    cond_denum = abs( LL(A_1, a_1, b_1, c_1) + LL(A_0, a_0, b_0, c_0) )                   
    cond = cond_num/(0.5*cond_denum)   # The condition                 
    while cond > tol: 
        
    # finding the next optimized direction (Polak- Ribiere choice for gamma)
        num = np.inner( gradient(a_0, b_0, c_0) - gradient(a_1, b_1, c_1) , -gradient(a_1, b_1, c_1) )
        denum = np.inner( gradient(a_0, b_0, c_0) , gradient(a_1, b_1, c_1) )
        gamma =  num/denum
        
        # Setting the new direction 
        d = -gradient( a_1, b_1, c_1) + gamma*d                  
        # Finding the step size alpha using minimization of g_alpha
        initial = np.array([1e-4,1e-4,1e-4])
        alpha_opt = optimize.minimize( g_alpha, initial, args = (a_1, b_1, c_1, d))
        alpha = res.x

        # Updating the values for parameters
        a_0 = a_1
        b_0 = b_1
        c_0 = c_1
        
        a_1 = a_0 + alpha[0]*d[0]
        b_1 = b_0 + alpha[1]*d[0]
        c_1 = c_0 + alpha[2]*d[0]
        
        # Updating the convergence condition based on the new calculated parameters
        A_0 = trilinear(a_0, b_0, c_0)
        A_1 = trilinear(a_1, b_1, c_1)

        cond_num = abs( LL(A_1, a_1, b_1, c_1) - LL(A_0, a_0, b_0, c_0) )
        cond_denum = abs( LL(A_1, a_1, b_1, c_1) + LL(A_0, a_0, b_0, c_0) )                   
        cond = cond_num/(0.5*cond_denum)                 
        
        
    return a_1, b_1, c_1
    
CG(1.1, 1.5, 3., tol = 1e-2)
