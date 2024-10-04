import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
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
removelog = (10**hydrogendata_array[:,1])**2
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
    #plt.yticks(np.linspace(0, 20, 21))
    plt.grid('on')
    plt.title(title)
    plt.plot(temp, pres, linewidth = 0.75)

#input the chamber conditions computed from equilibrium calcs
nH = np.linspace(0.1235, 0, 64) #mole fraction
dnH = nH
Po = 2.0*10**6
To = 3500
Ho = 72882.23
gamma_o = 1.36
Cp = 33.43/(2*10**(-3))

#independent variable is temperature
T = np.arange(300, To, 50)
Pisent = Po*(T/To)**(gamma_o/(gamma_o - 1))
visent = np.sqrt(2*Cp*(To - T))

#plotPvT(Pisent, T, "Isentropic Pressure vs. Exit Temperature")

for i in range (0, T.size - 1):
    diffT = T[i]%100
    if (diffT > 50):
        correcT = T[i] + diffT
    else:
        correcT = T[i] - diffT
    indexT = correcT/100 + 2
    
    
    indexReal = (int(indexT))
    Kp = 1/removelog[indexReal]
    
    
    dnH[i] = ((10**4)*(2 - nH[i]))/(visent[i]*8.3145*T[i])*(
        Pisent[i]*nH[i]**2 - ((1 - nH[i])*Pisent[i])/(Kp))
    nH[i + 1] = nH[i] + dnH[i]
    
#plotPvT(nH, T, "Mole Fraction of Hydrogen atoms vs. Exit Temperature")
plotPvT(visent/9.8, T, "Specific impulse, isentropic")