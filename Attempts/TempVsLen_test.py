import numpy as np
from matplotlib import pyplot as plt


def area_ratio_squared(M, gam):
    """
    Calculate the area ratio squared (A/A*)^2 given Mach number M and specific heat ratio gam.
    
    Parameters:
    M (float): Mach number
    gam (float): Specific heat ratio (gamma)
    
    Returns:
    float: The calculated area ratio squared.
    """
    term1 = 1 / M**2
    term2 = (2 / (gam + 1)) * (1 + (gam - 1) / 2 * M**2)
    area_ratio_squared = term1 * (term2 ** ((gam + 1) / (gam - 1)))
    
    return area_ratio_squared


M_input = np.linspace(1, 7, 100)  
gam_input = 1.36  
result = area_ratio_squared(M_input, gam_input)**0.5
R = 8.314/(1.89*10**-3)

length = (np.sqrt(result/3.1416) - 0.5642)/0.2679
T = 3500*(1 + (gam_input - 1)/2 * M_input**2)**(-1)

plt.gca().invert_xaxis()
plt.plot(T, result)