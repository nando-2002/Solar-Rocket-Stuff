import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import savgol_filter

#my favourite font for matplotlib
plt.rcParams.update({
    "font.family": "monospace"
})


def areaRatio (val):
    term1 = 1 / val**2
    term2 = (2 / (gam + 1)) * (1 + (gam - 1) / 2 * val**2)
    area_ratio_squared = term1 * (term2 ** ((gam + 1) / (gam - 1)))
    
    return area_ratio_squared**0.5

#from Mach num, P, T and v can be calculated with isentropic relations
def machnumbers ():
   
    subsonicM = np.linspace(0.3, 1, 1000)
    supersonicM = np.linspace(1, 10, 10000)
    subratios = areaRatio(subsonicM)
    supratios = areaRatio(supersonicM)
    
    actualM = np.zeros(x.size)
    
    #populate subsonic values
    for i in range(0, 250):
        for j in range(subsonicM.size):
            if (abs(Arat[i] - subratios[j]) <= 0.0025):
                actualM[i] = subsonicM[j]
                break
    #populate supersonic values
    for i in range(138, 165):
        for j in range(supersonicM.size):
            if (abs(Arat[i] - supratios[j]) <= 0.0001):
                actualM[i] = supersonicM[j]
                break
    
    for i in range(165, x.size):
        for j in range(supersonicM.size):
            if (abs(Arat[i] - supratios[j]) <= 0.01):
                actualM[i] = supersonicM[j]
                break
    
    for i in range(x.size - 1):
        if (actualM[i] == 0):
            actualM[i] = 0.5*(actualM[i - 1] + actualM[i + 1])
    
    return actualM

#import the values for the equilibrium constant vs temperature for 0.5H2 -> H.
#NIST JANAF uses log base 10 and its for 1 mol of H. This is why it must be squared

hydrogendata = pd.read_excel(
    'HydrogenAtom.xlsx', usecols='A, H', skiprows = range(3))
enthalpydata = pd.read_excel(
    'HydrogenAtom.xlsx', usecols='F', skiprows = range(3))

hydrogendata_array = hydrogendata.to_numpy()
Hf = enthalpydata.to_numpy()

removelog = (10**hydrogendata_array[:,1])**2
# print(hydrogendata_array[:,1])

def logdata_H():
    plt.figure()
    plt.grid('on')
    #plt.title("$log_{10}(K_p)$ for $H_2 \leftrightarrow 2H$")
    plt.plot(hydrogendata_array[:,0], hydrogendata_array[:,1], linewidth = 0.75)

def normdata_H():
    plt.figure()
    plt.grid('on')
    #plt.title("$K_p$ for $H_2 \leftrightarrow 2H$")
    plt.plot(hydrogendata_array[:,0], removelog, linewidth = 0.75)
    
def plotPvT(pres, temp, title):
    plt.figure()
    plt.gca().invert_xaxis()
    plt.xticks(np.linspace(300, 3500, 33))
    plt.xlim(3500, 300)
    #plt.yticks(np.linspace(0, 20, 21))
    plt.grid('on')
    plt.title(title)
    plt.plot(temp, pres, linewidth = 0.75)
    

#creating the nozzle profile from Krieger 1951

#x = np.linspace(0, 10, 1001) # x axis is 100 units long
x = np.arange(0, 50, 0.01)
noz = np.zeros(x.size)
noz[:(10)] = 1  #straight chamber
noz[(10):(53)] = np.sqrt(1 - (x[(10):(53)] -0.1)**2) #convergent circle
noz[(53):(191)] = ( 2.707 - np.sqrt(4 - (x[(53):(191)] - 1.393)**2) ) #throat and divergent circle
noz[(191):] = (0.26795 * x[(191):] + 0.2635) #divergent cone

noz = noz + 1.75

#isentropic Area-Mach relations
#At = 45.319 #1.5707
#At = A[139]
#At = 26.3973

A = np.pi * noz[:]**2 
At = A[139]
Arat = A/At
gam = 1.36

M = machnumbers()
M = savgol_filter(M, 100, 3)


#defining some initial conditions

Po, To, P, T = 20, 5000, np.zeros(x.size), np.zeros(x.size)
P = Po * (1 + (gam - 1)/2 * M**2)**((-gam)/(gam - 1))
T = To * (1 + (gam - 1)/2 * M**2)**(-1)
vel = M * np.sqrt(gam * (8.314/(1.89*10**-3)) * T)

#plt.plot(x[:], vel[:])

#from here, the chemical kinetic solution can begin

#input the chamber conditions computed from equilibrium calcs
nH = np.zeros(x.size); nH[:] = 0.85; #nH[1:] = 0.1235 #mole fraction also so that derivative doesn't go crazy
dnH = np.zeros(x.size); dnH[:] = 0.1;

#Po, P, To, T, and vel are required. Additionally, Cp and R (specific) are needed 
Cp = 33.43/(2*10**(-3)) #(per mass, not mol)
R = 8.314/(1.89*10**-3)

kf = 10**16
Kpp = np.zeros(x.size)#eq const
Kpr = np.zeros(x.size)

for i in range (x.size):
    diffT = T[i]%100
    if (diffT > 50):
        correcT = T[i] + (100 - diffT)
    else:
        correcT = T[i] - diffT 
    indexT = correcT/100 + 2
    indexReal = (int(indexT))
    H = Hf[indexReal]*1000
    Kpp[i] = ( (np.e)**(np.log(10**(-35.613)) + (0.958*H/8.314)*( (1/298.15) - (1/T[i]) )) )**2
    Kpr[i] = 1/Kpp[i]
    #remember to double the enthalpy from the NIST table cuz 2 moles of H not 1 mole




for i in range (x.size - 3):
    
    '''
    # diffT = T[i]%100
    # if (diffT > 50):
    #     correcT = T[i] + (100 - diffT)
    # else:
    #     correcT = T[i] - diffT
    # # correcT = T[i] + diffT
    
    
    # indexT = correcT/100 + 2
    # indexReal = (int(indexT))
    # Kp = 1/removelog[indexReal] #nearest value of Kp in the table
    
    
    #kpdebug[i] = indexReal
    '''
    
    #computing from krieger's formula for dnH/dx
    
    dnH[i] = ( (kf * (2 - nH[i]))/(vel[i] * (R * T[i])**2) )*(
        (nH[i]*P[i])**2 - ((1 - nH[i]) * P[i])/Kpr[i] )
    dnH[i + 1] = ( (kf * (2 - nH[i + 1]))/(vel[i + 1] * (R * T[i + 1])**2) )*( 
        (nH[i + 1]*P[i + 1])**2 - ((1 - nH[i + 1]) * P[i])/Kpr[i + 1] )
    dnH[i + 2] = ( (kf * (2 - nH[i + 2]))/(vel[i + 2] * (R * T[i + 2])**2) )*( 
        (nH[i + 2]*P[i + 2])**2 - ((1 - nH[i + 2]) * P[i])/Kpr[i + 2] )
    dnH[i + 3] = ( (kf * (2 - nH[i + 3]))/(vel[i + 3] * (R * T[i + 3])**2) )*( 
        (nH[i + 3]*P[i + 3])**2 - ((1 - nH[i + 3]) * P[i])/Kpr[i + 3] )

    #print(dnH[i])
    nH[i + 3] = nH[i]  - (3*0.01/8) * (
        dnH[i] + 3*dnH[i + 1] + 3*dnH[i + 2] + dnH[i + 3])
    
    '''
    dnH[i] = ( (10**15 * (2 - nH[i]))/(vel[i] * (R * T[i])**2) )*(
        (nH[i]*P[i])**2 - ((1 - nH[i]) * P[i])/Kpr[i] )
    nH[i + 1] = nH[i] - dnH[i]
    '''

dnH = savgol_filter(dnH, 100, 3)
nH = savgol_filter(nH, 100, 3)
# plt.title("Kp")
# plt.xlim(1500, 3500)
# plt.ylim(-0.01, 0.6)
# plt.plot(T, Kpp); 
# plt.plot(hydrogendata_array[:,0], removelog);


# plt.plot(x, nH)

plt.subplot(2, 1, 1)
plt.title("\small Rate of formation of $H_2$")
plt.plot(x, dnH)
plt.axvline(1.39, linestyle = 'dashed', color = 'black')

# plt.subplot(2, 2, 2)
# plt.title("\small Nozzle Contour")
# plt.plot(x, noz)

plt.subplot(2, 1, 2)
# plt.title("\small Equilibrium Data")
# plt.xlim(1500, 3500)
# plt.ylim(-0.01, 0.3)
# plt.plot(T, Kpr); plt.plot(hydrogendata_array[:,0], removelog); plt.plot(T, Kpr**2)
plt.title("\small nH")
plt.plot(x, nH)
plt.axvline(1.39, linestyle = 'dashed', color = 'black')


# plt.subplot(2, 2, 4)
# plt.title("\small Velocity")
# plt.plot(x, vel)

# plt.title("\small Nozzle Contour")
