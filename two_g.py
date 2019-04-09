#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from two_e import positions
from one_a import poiss

# Histogram of number of satellites in radial bin from (2.e)
bin1000 = np.logspace(np.log10(1e-4), np.log10(5.), 20)
n, bins = np.histogram( positions[:,:,0], bin1000)

# Finding the bin with maximum number of satellites
binmax = np.where( n == max(n))
leftbin = bin1000[binmax[0]][0]
rightbin = bin1000[binmax[0] + 1][0]

# Finding the position of satellites that are inside binmax using mask
mask1 = positions[:,:,0] >= leftbin
mask2 = positions[:,:,0] < rightbin
mask = mask1 * mask2

components = ((positions[:,:,0])[mask]).reshape(((positions[:,:,0])[mask]).size)

#Quick sort algorithm

#----- The function to find partitioning index for sorting

def partition( array, low, high): 
    i = ( low - 1 )           # index of smaller element 
    pivot = array[high]       # pivot : the last element

    for j in range(low , high): 

        # If current element is smaller than or 
        # equal to pivot the index of smaller element is incremented
        if array[j] <= pivot: 
            i = i+1
            array[i], array[j] = array[j], array[i] 

    array[i+1], array[high] = array[high], array[i+1] 
    
    return i+1


#----- The general quick sort function

def quickSort(arr, low, high): 
    if low < high: 

        pi = partition(arr,low,high) 

        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 
        
    return

#----- A function to calculate statistics
def statistics( arr, len_arr, P16 = 16, P84 = 84):
    if len_arr %2 == 0:
        median = (arr[int( (len_arr/2) - 1 )] + arr[int( len_arr/2 )])/2.
    else:
        median = arr[int( 0.5*(len_arr - 1) )]
        
    # Ordinal rank numbers and the corresponding percentiles
    n16 = int(np.ceil(P16*len_arr/100))
    perc16 = arr[n16]
    
    n84 = int(np.ceil(P84*len_arr/100))
    perc84 = arr[n84]
    
    return median, perc16, perc84
    
    
quickSort( components, 0, len(components) - 1)
print ("The sorted array is: ", components)
np.savetxt('sortarray_2g.txt', components )
 
median, perc16, perc84 = statistics(components, len(components))

#----- The histogram and Poisson distribution

m1 = (leftbin < positions[:,:,0])
m2 = (positions[:,:,0] < rightbin)
mask = m1*m2
# C= number of galaxies in binmax for each halo --> 1000 values
C= np.sum(mask, axis=1) 

# The distribution for halos with galaxy numbers = C
N, borders = np.histogram( C, np.arange( min(C), max(C) ))
Centers = np.arange( min(C) + 0.5 , max(C) - 1)

# Normalizing the distribution and making the plot
plt.bar( Centers , N/1000, label = 'Histogram')

# The poisson distribution

mean = np.sum(N*Centers/1000)    # The mean value for poisson distrubution
pois_values = np.zeros( len(Centers) ) 
for i, C_i in enumerate(Centers):
    pois_values[i] = poiss(mean, C_i)
    
    
plt.plot(Centers, pois_values, color ='red', label = 'Poisson distribution')
plt.legend()
plt.xlabel('Number of galaxies')
plt.ylabel('Number density of halos')
plt.savefig('./Plots/distribs_2g.png')
plt.show()
