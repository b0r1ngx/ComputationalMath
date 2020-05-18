# Study of the dependence of luminosity on temperature for a blackbody
import numpy as np
from matplotlib import pyplot as plot
from scipy import integrate
# T - temperature in Kelvin.
# E - radiation power in W / cm^2.
lambd = 5.548752 * 10 ** -5
lambda1 = 5.548752 * 0.00001
lambda2 = 13.02892 * 10 ** -5

EFF = (64.77 / T ** 4)


def pick_step(function, a, b, step):
    x = np.arange(a, b, step)
    y = function(x)
    return x, y

def rkf45(f, t, x0):
    r = (integrate.ode(f)
         .set_integrator('dopri5', atol=0.001)
         .set_initial_value(x0, t[0]))
    x = np.zeros((len(t), len(x0)))
    x[0] = x0
    for i in range(1, len(t)):
        x[i] = r.integrate(t[i])
        # if not r.successful():
        #     raise RuntimeError("Error")
    return x[:, 0]

a = 1000
b = 9000
step = 1000
