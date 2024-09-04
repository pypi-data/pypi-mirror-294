# IMPORT PACKAGES
import numpy as np
import pandas as pd


# FIXED PARAMETERS
pi = np.pi
mp = 1.6726e-24 # grams
mu = 1.22 # mean molecular weight
pc = 3.086e18 # cm
print('OK till now')

# import data
import pkgutil
from io import BytesIO
data = pkgutil.get_data(__name__, "resources/GMC_e23.csv")

df = pd.read_csv(BytesIO(data))
print(df['e23_logM31'])
