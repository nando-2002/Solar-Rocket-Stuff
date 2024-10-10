import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

#my favourite font for matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif"
})

#import the values for the equilibrium constant vs temperature for 0.5H2 -> H.
#NIST JANAF uses log base 10 and its for 1 mol of H. This is why it must be squared

hydrogendata = pd.read_excel(
    'HydrogenAtom.xlsx', usecols='A, H', skiprows = range(3))

hydrogendata_array = hydrogendata.to_numpy()
removelog = (10**hydrogendata_array[:,1])**0.5
# print(hydrogendata_array[:,1])

def logdata_H():
    plt.figure()
    plt.grid('on')
    plt.title("$log_{10}(K_p)$ for $H_2 \leftrightarrow 2H$")
    plt.plot(hydrogendata_array[:,0], hydrogendata_array[:,1], linewidth = 0.75)

def normdata_H():
    plt.figure()
    plt.grid('on')
    plt.title("$K_p$ for $H_2 \leftrightarrow 2H$")
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

#input the chamber conditions computed from equilibrium calcs
nH = np.zeros(320); nH[319] = 0.1235; nH[318] = 0.12 #mole fraction
dnH = np.zeros(320)
# x = np.zeros(320)
Po = 2.0*10**6
To = 3500
Ho = 72882.23
gamma_o = 1.36
Cp = 33.43/(2*10**(-3))
R = 8.314/(1.89*10**-3)

#independent variable is temperature
T = np.arange(300, To, 10)
Pisent = Po*(T/To)**(gamma_o/(gamma_o - 1))
visent = np.sqrt(2*Cp*(To - T))

M = np.sqrt(2 * (3500 / T - 1) / (gamma_o - 1))
alpha = np.sqrt((1/(M**2))*(2/(gamma_o - 1) * (1 + (gamma_o - 1)/(M**2) ))**((gamma_o + 1)/(gamma_o - 1)))

length = (np.sqrt(alpha/3.1416) - 0.5642)/0.2679

#plotPvT(Pisent, T, "Isentropic Pressure vs. Exit Temperature")

for i in range (T.size - 1, 0, -1):
    diffT = T[i]%100
    if (diffT > 50):
        correcT = T[i] + (100 - diffT)
    else:
        correcT = T[i] - diffT
    indexT = correcT/100 + 2
    indexReal = (int(indexT))
    Kp = 1/removelog[indexReal] #nearest value of Kp
    dnH[i] = ((10**4)*(2 - nH[i]))/(visent[i]*(R*T[i])**2)*((Pisent[i]*nH[i])**2 - ((1 - nH[i])*Pisent[i])/(Kp))*1
    #print(dnH[i])
    nH[i - 1] = nH[i] - dnH[i]
    
#plotPvT(nH, T, "Mole Fraction of Hydrogen atoms vs. Exit Temperature")
#plotPvT(visent/9.8, T, "Specific impulse, isentropic")

plotPvT(length, T, "Length of conical nozzle vs. exit Temperature")
#normdata_H()