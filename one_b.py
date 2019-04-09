#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def rand(modulus= 2**64, a= 3935559000370003845, c= 2691343689449507681):
    # XOR shift
    rand.current ^= rand.current << 21
    rand.current ^= rand.current >> 35
    rand.current ^= rand.current << 4
    # LCG
    rand.current = (a * rand.current+ c) % modulus 
    
    return rand.current/(modulus-1)


rand.current = 13    # Seed
print('the seed value of the random generator is:', rand.current)

#----- generating the scatter plots

rands_scatt=[]
for i in range(1000):
    rands_scatt.append( rand() )
    
plt.scatter( rands_scatt[0:998], rands_scatt[1:999], marker= '.' )
plt.xlabel(r'$x_i$')
plt.ylabel(r'$x_{i+1}$')
plt.savefig('./Plots/scatt_1b.png')
plt.close()


#----- generating the histogram plot

rands_hist=[]
for i in range(1000000):
    rands_hist.append (rand() )

bins = np.arange(0,1.05,0.05)
plt.hist( rands_hist, bins )
plt.xlabel(r'$x_{random}$')
plt.ylabel("frequency")
plt.savefig('./Plots/hist_1b.png')
plt.close()

#----- Generating random values


a = 1.1+(2.5-1.1)*rand()
b = 0.5+(2.-0.5)*rand()
c = 1.5+(4.-1.5)*rand()

np.savetxt('random.txt', np.array([a, b, c]))

