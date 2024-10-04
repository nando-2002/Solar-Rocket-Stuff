import numpy as np
import matplotlib.pyplot as plt
from labellines import labelLines


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif"
})

plt.clf()
plt.title("Performance of Various Fuels at T/W ratio 1")
x = np.linspace(2500, 8000, 500)
atoms = [1, 3.2, 4.2, 6]
names = ['Atomic H', 'Dissociated CH4', 'Dissociated NH3', 'Dissociated Water']
#names = ['Atomic H', 'Dissociated CH4', 'Dissociated NH3', 'Dissociated Water', 'Magnetically Augmented H'
lines = []
plt.grid('on')
plt.xlim(2500, 8000)
plt.ylim(0, 2500)
plt.xlabel("Temperature in Kelvin")
plt.ylabel("Specific Impulse (seconds)")

plt.axvline(5800, linestyle = 'dashed', color = 'black')


for i in range(len(atoms)):
    # if (i == len(atoms) - 1):
    #     #y = np.sqrt((2*1.4*8.134*x)/((1.4 - 1)*atoms[i]*10**-3))*(1/9.81)*1.5
    #     print("test")
    #else:
    #print(i)
    y = np.sqrt((2*1.4*8.134*x)/((1.4 - 1)*atoms[i]*10**-3))*(1/9.81) 
    #print(y)           
    line, = plt.plot(x, y, label= names[i], linewidth=0.5)
    lines.append(line)
    
y = 0*x + 450;
line, = plt.plot(x, y, label= 'Chemical Propulsion Limit', linestyle = 'dashed', linewidth=0.5)
lines.append(line)
labelLines(lines, zorder=2.5)



plt.show()