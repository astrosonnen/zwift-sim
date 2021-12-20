import h5py
import numpy as np
from scipy.optimize import leastsq


# copies the values of speed as a function of Power/mass and rider weight, from Eric Schlange's Zwiftinsider test
weight_grid = np.array([50., 75., 100.])
Wkg_grid = np.array([2., 3., 4.])

v_2Wkg = np.array([29., 31.2, 32.8])
v_3Wkg = np.array([33.8, 36., 38.])
v_4Wkg = np.array([37.5, 40., 43.])

v_grid = np.vstack((v_2Wkg, v_3Wkg, v_4Wkg))

output = h5py.File('zinsider_flat_test.hdf5', 'w')
output.create_dataset('weight_grid', data = weight_grid)
output.create_dataset('Wkg_grid', data = Wkg_grid)
output.create_dataset('speed_grid', data = v_grid)


