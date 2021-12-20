import h5py
import numpy as np
from scipy.optimize import leastsq


showfit = False
flat_test = h5py.File('zinsider_flat_test.hdf5', 'r')

weight_grid = flat_test['weight_grid'][()]
Wkg_grid = flat_test['Wkg_grid'][()]
v_grid = flat_test['speed_grid'][()]

# fits a binary quadratic model in rider's weight and Power/weight to the Zwiftinsider flat test data

W, P = np.meshgrid(weight_grid, Wkg_grid)
Wkg_piv = 3.
weight_piv = 75.

def fitv(p):
    return (p[0] + p[1]*(W-weight_piv) + p[2]*(P-Wkg_piv) + p[3]*(W-weight_piv)**2 + p[4]*(W-weight_piv)*(P-Wkg_piv) + p[5]*(P-Wkg_piv)**2).flatten()

def errv(p):
    return fitv(p) - v_grid.flatten()

guess = np.array([40., 0., 1., 0., 0., 0.])

pfit = leastsq(errv, guess)[0]
print(pfit)

# stores coefficients in an .hdf5 file
output = h5py.File('quadratic_fit.hdf5', 'w')
output.attrs['weight_piv'] = weight_piv
output.attrs['Wkg_piv'] = Wkg_piv
for n in range(6):
    output.attrs['p_%d'%n] = pfit[n]

if showfit:
    import pylab
    
    def modelv(weight, Wkg):
        return pfit[0] + pfit[1]*(weight - weight_piv) + pfit[2]*(Wkg - Wkg_piv) + pfit[3]*(weight - weight_piv)**2 + pfit[4]*(weight - weight_piv) * (Wkg - Wkg_piv) + pfit[5]*(Wkg - Wkg_piv)**2

    nweight = 51
    weight_arr = np.linspace(50., 100., nweight)
    
    nWkg = 7
    Wkg_arr = np.linspace(2., 5., nWkg)
    
    for i in range(nWkg):
        pylab.plot(weight_arr, modelv(weight_arr, Wkg_arr[i]*np.ones(nweight)))
    
    pylab.scatter(weight_grid, v_2Wkg, color='k')
    pylab.scatter(weight_grid, v_3Wkg, color='k')
    pylab.scatter(weight_grid, v_4Wkg, color='k')
    
    pylab.show()

