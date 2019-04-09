#!/usr/bin/env python
import numpy as np

def poiss(mean,k):
    
    mean = np.float64(mean)
    k = np.int64(k)
    
    # Calculation of factorial
    a = np.arange(1, k+1)
    k_faklog = np.sum( np.log(a) )
    
    
    # Calculation of the numerator
    logP = k*np.log(mean) - mean - k_faklog
    
    return(np.exp(logP))

np.savetxt('poiss_1a.txt', np.array([poiss(1.,0.), poiss(5.,10.), poiss(3.,21.), poiss(2.6,40.), poiss(101.,200.)]))
    
print(" (1,0):",poiss(1.,0.),'\n',"(5,10):",poiss(5.,10.),'\n',"(3,21):",poiss(3.,21.), 
      '\n',"(2.6,40):",poiss(2.6,40.),'\n', "(101,200):",poiss(101.,200))

