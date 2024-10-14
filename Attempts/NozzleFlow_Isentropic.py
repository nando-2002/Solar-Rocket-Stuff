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


# Given data
gam_input = 1.36
R = 8.314/(1.89*10**-3)

To = 6000
T = np.linspace(300, To, 100)

M_input = np.sqrt(2 * ((To / T) - 1) / (gam_input - 1))

# Calculate area ratio
result = area_ratio_squared(M_input, gam_input)**0.5

length = (np.sqrt(result/3.1416) - 0.5642)/0.2679

# Plotting
plt.subplot(1, 3, 1)
plt.gca().invert_xaxis()  # Invert x-axis (for temperature)
plt.plot(T, length)
plt.xlabel("Temperature (K)")
plt.ylabel("Length")
plt.title("Nozzle Length vs Temperature (with M as dependent)")
plt.grid(True)

plt.subplot(1, 3, 2)
plt.gca().invert_xaxis()  # Invert x-axis (for temperature)
plt.plot(T, M_input)
plt.xlabel("Temperature (K)")
plt.ylabel("Mach Number")
plt.title("Mach Number vs Temperature (with M as dependent)")
plt.grid(True)

plt.subplot(1, 3, 3)
plt.gca().invert_xaxis()  # Invert x-axis (for temperature)
plt.plot(T, result)
plt.xlabel("Temperature (K)")
plt.ylabel("Area")
plt.title("Area Ratio vs Temperature (with M as dependent)")
plt.grid(True)
plt.show()
