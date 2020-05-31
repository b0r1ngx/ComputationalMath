# Study of the dependence of luminosity on temperature for a blackbody.
# T - temperature in Kelvin.
# E - radiation power in W / cm^2.
# λ1, λ2 - wavelength.
# EFF - luminosity in %.
import numpy as np
from math import sqrt, cos, pi, exp
from matplotlib import pyplot as plot
from scipy.optimize import fsolve, minimize
from scipy.integrate import quad as QUANC8
from scipy.interpolate import lagrange, CubicSpline
# Given: finding the boundaries of integration: λ1 and λ2
def y(x):
    return sqrt(x) - 2 * cos(pi * x / 2)
x0 = np.arange(1)
y = min(fsolve(y, x0))  # min(of all roots)
print('y=', y)  # y ≈ 0.7208828427280686
# λ1 ≈ 4 * 10^-5
LAMBDA1d = y * 5.548752 * 0.00001
def z(z):
    return exp(z)*(2*z**2-4)+(2*z**2-1)**2+exp(2*z)-3*z**4
x1 = np.arange(0.1, 1.0)  # interval [a,b]
z = minimize(z, x1)['x'][0]
print('z=', z)  # z ≈ 0.5372744438775525
# λ2 ≈ 7 * 10^-5
LAMBDA2d = z * 13.02892 * 0.00001

def fEFF(T):
    integral = QUANC8(lambda x: f(x, T), LAMBDA1d, LAMBDA2d)
    return (64.77 / T ** 4) * integral[0]
def f(x, T):
    return (x**5*(exp(1.432/(T*x)) - 1))**-1

T = np.array([500*T for T in range(2, 21)])
EFF = np.array([fEFF(500*T) for T in range(2, 21)])
fig, ax = plot.subplots(figsize=(6.5, 4))
plot.title('%luminosity from T')
ax.plot(T, EFF, 'o', label='x')
ax.plot(T, EFF, label='f(x)')
ax.legend(loc='upper left')
plot.show()
# Exploring maximum of luminosity ~ 7000°К
# start with ~ [6700 7300], then closer and closer
p = 7000
for k in range(27, 1, -25):
    print('k=', k)
    T = np.array([k*T for T in range(int((p - 10*k)/k), int((p + 10*k)/k))])
    EFF = np.array([fEFF(k*T) for T in range(int((p - 10*k)/k), int((p + 10*k)/k))])
    fig, ax = plot.subplots(figsize=(6.5, 4))
    plot.title('%luminosity from T, 7000±{} closer'.format(10*k))
    ax.plot(T, EFF, 'o', label='x')
    ax.plot(T, EFF, label='f(x)')
    ax.legend(loc='upper left')
    plot.show()
# Last jump in to maximum
T = np.array([T/200 for T in range(2*700895, 2*700901)])
EFF = np.array([fEFF(T/200) for T in range(2*700895, 2*700901)])
fig, ax = plot.subplots(figsize=(6.5, 4))
plot.title('%luminosity from T, 7009±1 closer')
ax.plot(T, EFF, 'o', label='x')
ax.plot(T, EFF, label='f(x)')
ax.legend(loc='upper left')
plot.show()
print('maximum of out BLACKBODY model is', max(np.array([fEFF(T/2000) for T in range(20*700895, 20*700901)])))
# Influence of errors, ±10%
for error in range(-10, 11, 4):
    LAMBDA1 = LAMBDA1d * (1 + 0.01 * error)
    LAMBDA2 = LAMBDA2d * (1 + 0.01 * error)
    def EFF(T):
        integral = QUANC8(lambda x: f(x, T), LAMBDA1, LAMBDA2)
        return (64.77 / T ** 4) * integral[0]
    T = np.array([500 * T for T in range(2, 21)])
    EFF = np.array([EFF(500*T) for T in range(2, 21)])
    fig, ax = plot.subplots(figsize=(6.5, 4))
    plot.title('%luminosity from T, error {}%'.format(error))
    ax.plot(T, EFF, 'o', label='x')
    ax.plot(T, EFF, label='f(x)')
    ax.legend(loc='upper left')
    plot.show()
