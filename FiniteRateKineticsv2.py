import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd

#my favourite font for matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif"
})

def areaRatio (val):
    term1 = 1 / val**2
    term2 = (2 / (gam + 1)) * (1 + (gam - 1) / 2 * val**2)
    area_ratio_squared = term1 * (term2 ** ((gam + 1) / (gam - 1)))
    
    return area_ratio_squared**0.5

#from Mach num, P, T and v can be calculated with isentropic relations
def machnumbers ():
   
    subsonicM = np.linspace(0.3, 1, 1000)
    supersonicM = np.linspace(1, 4.5, 5000)
    subratios = areaRatio(subsonicM)
    supratios = areaRatio(supersonicM)
    
    actualM = np.zeros(x.size)
    
    #populate subsonic values
    for i in range(0, 250):
        for j in range(1000):
            if (abs(Arat[i] - subratios[j]) <= 0.0025):
                actualM[i] = subsonicM[j]
                break
    #populate supersonic values
    for i in range(138, 165):
        for j in range(5000):
            if (abs(Arat[i] - supratios[j]) <= 0.0001):
                actualM[i] = supersonicM[j]
                break
    
    for i in range(165, 1001):
        for j in range(5000):
            if (abs(Arat[i] - supratios[j]) <= 0.01):
                actualM[i] = supersonicM[j]
                break
    
    for i in range(1000):
        if (actualM[i] == 0):
            actualM[i] = 0.5*(actualM[i - 1] + actualM[i + 1])
    
    return actualM
    

#creating the nozzle profile from Krieger 1951

x = np.linspace(0, 10, 1001) # x axis is 100 units long
noz = np.zeros(x.size)
noz[:10] = 1 #straight chamber
noz[10:53] = np.sqrt(1 - (x[10:53] -0.1)**2) #convergent circle
noz[53:191] = 2.707 - np.sqrt(4 - (x[53:191] - 1.393)**2) #throat and divergent circle
noz[191:1001] = 0.26795 * x[191:1001] + 0.2635 #divergent cone

#isentropic Area-Mach relations
At = 1.5707 #actual throat area
A = np.pi * noz[:]**2 
Arat = A/At
gam = 1.36

M = machnumbers()

#defining some initial conditions

Po, To, P, T = 20, 3500, np.zeros(x.size), np.zeros(x.size)
P = Po * (1 + (gam - 1)/2 * M**2)**((-gam)/(gam - 1))
T = To * (1 + (gam - 1)/2 * M**2)**(-1)
#plt.plot(x[:], T[:])

#from here, the chemical kinetic solution can begin
