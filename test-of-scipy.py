import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import pandas as pd

hydrogendata = pd.read_excel(
    'HydrogenAtom.xlsx', usecols='A, H', skiprows = range(3))

print(hydrogendata)