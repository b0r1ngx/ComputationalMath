import numpy as np
from matplotlib import pyplot as plot
from scipy import integrate


# Pick points of `function` at interval `[a, b]` with `step`
def pick_step(function, a, b, step):
    x = np.arange(a, b, step)
    y = function(x)
    return x, y


# Method Adams 3th - not work as well, not running as well to the points
# def adam(f, T, X0):
#     X = np.zeros((len(T), len(X0)))
#     X[0] = X0
#
#     h = T[1] - T[0]
#
#     Xk_1 = X[0] - 1 * h * f(T[0], X[0])
#     Xk_2 = X[0] - 2 * h * f(T[0], X[0])
#     X[0] = Xk_1 + (h / 12) * (5 * f(T[0], X[0]) + 8 * f(T[-1], Xk_1) - f(T[-2], Xk_2))
#     X[1] = Xk_1 + (h / 12) * (5 * f(T[1], X[1]) + 8 * f(T[0], X[0]) - f(T[-1], Xk_1))
#     for it in range(2, len(T)):
#         X[it] = X[it - 1] + (h / 12) * (5 * f(T[it], X[it]) + 8 * f(T[it - 1], X[it - 1]) - f(T[it - 2], X[it - 2]))
#     return X[:, 0]

# Method Adams 3th.
def adam(f, T, X0):
    X = np.zeros((len(T) + 2, len(X0)))
    X2 = np.zeros((len(T), len(X0)))

    h = T[1] - T[0]
    X987 = rkf45(f, [T[0], T[0] - h, T[0] - 2 * h], X0)
    X[0] = X987[2]
    X[1] = X987[1]
    X[2] = X0

    for it in range(3, len(T) + 2):
        X[it] = X[it - 1] + (h / 12.0) * (
                23 * f(T[it - 3] - h, X[it - 1]) - 16 * f(T[it - 3] - 2 * h, X[it - 2]) + 5 * f(T[it - 3] - 3 * h,
                                                                                                X[it - 3]))
    for it in range(0, len(T)):
        X2[it] = X[it + 2]

    return X2[:, 0]


# Trapezoid Method
def trapeze(f, T, X0):
    X = np.zeros((len(T), len(X0)))

    X[0] = X0
    h = T[1] - T[0]
    X[1] = X[0] + h * (f(T[0], X[0]))
    for it in range(2, len(T)):
        X[it] = X[it - 1] + (h / 2) * (f(T[it - 1], X[it - 1]) + f(T[it - 2], X[it - 2]))
    return X[:, 0]


# RKF45
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


# Advanced method of Euler
def advanced_euler(f, t, x0):
    x = np.zeros((len(t), len(x0)))
    x[0] = x0
    h = t[1] - t[0]
    for i in range(1, len(t)):
        approximation = f(t[i - 1], x[i - 1])
        x[i] = x[i - 1] + h * f(t[i - 1] + h / 2, x[i - 1] + h / 2 * approximation)
    return x[:, 0]


# Method Runge-Kutta 3th order
def runge_kutta3(f, t, x0):
    x = np.zeros((len(t), len(x0)))
    x[0] = x0
    h = t[1] - t[0]
    for i in range(1, len(t)):
        k1 = h * f(t[i - 1], x[i - 1])
        k2 = h * f(t[i - 1] + h / 2, x[i - 1] + k1 / 2)
        k3 = h * f(t[i - 1] + h, x[i - 1] - k1 + 2 * k2)
        x[i] = x[i - 1] + (k1 + 4 * k2 + k3) / 6
    return x[:, 0]


# differential 2nd order
def f(t, x):
    dx = np.zeros(x.shape)
    dx[0] = x[1]
    dx[1] = (-1) * dx[0] / (2 * t)
    return dx


# Exact solution - 2*√t
def y(t):
    return 2 * np.sqrt(t)


# Exploration of the given task with `step` try
def exploring_with(step):
    # Interval [a, b]
    a = 1
    b = 2
    # Initial conditions
    x0 = np.array([2, 1])
    # Used methods
    t, X_original = pick_step(y, a, b, step)
    X_rkf45 = rkf45(f, t, x0)
    X_euler = advanced_euler(f, t, x0)
    X_runge_kutta3 = runge_kutta3(f, t, x0)
    X_adams3th = adam(f, t, x0)
    X_trapeze = trapeze(f, t, x0)
    # Graphs
    fig, ax = plot.subplots(figsize=(6.5, 5))
    ax.plot(t, y(t), 'o', label='1<=t<=2')
    ax.plot(t, y(t), label='√2')
    ax.plot(t, X_rkf45, label='RKF45')
    ax.plot(t, X_runge_kutta3, label='RungeK3')
    ax.plot(t, X_euler, label='+Euler')
    ax.plot(t, X_adams3th, label='Adams3th')
    ax.plot(t, X_trapeze, label='Trapeze')
    ax.legend(loc='upper left', ncol=2)
    plot.show()
    # Compute tolerances of every method of each point
    ltol_of_rkf45 = abs(X_rkf45 - X_original)
    ltol_of_euler = abs(X_euler - X_original)
    ltol_of_runge3 = abs(X_runge_kutta3 - X_original)
    ltol_of_adams3 = abs(X_adams3th - X_original)
    ltol_of_trapeze = abs(X_trapeze - X_original)
    # methods = ('RKF45', 'Runge-Kutta 3', '+Euler')
    # for i in range(len(methods)):
    #     print('Local tolerance of {}'.format(methods[i]), ltol_of)
    print('Local tolerance of RKF45:', ltol_of_rkf45[1])
    print('Local tolerance of Euler:', ltol_of_euler[1])
    print('Local tolerance of Runge-Kutta 3th:', ltol_of_runge3[1])
    print('Local tolerance of Adams 3th:', ltol_of_adams3[1])
    print('Local tolerance of Trapeze:', ltol_of_trapeze[1])
    print('Global tolerance of RKF45:', ltol_of_rkf45.sum())
    print('Global tolerance of Euler:', ltol_of_euler.sum())
    print('Global tolerance of Runge-Kutta 3th:', ltol_of_runge3.sum())
    print('Global tolerance of Adams 3th:', ltol_of_adams3.sum())
    print('Global tolerance of Trapeze:', ltol_of_trapeze.sum())
    print('h={}^3 for Euler(2th order):'.format(step / 2), (step / 2) ** 3)
    print('h={}^3 for Trapeze:'.format(step / 2), (step / 2) ** 3)
    print('h={}^4 for RK3(3th order):'.format(step / 2), (step / 2) ** 4)
    print('h={}^4 for Adams 3th:'.format(step / 2), (step / 2) ** 4)

    print('\t\tValues of each method of t points (inclusive):')
    print(' t\t\ty(t)\t\t\tRKF45\t\t\t+Euler\t\tRunge Kutta 3')
    for i in range(1, len(t)):
        print('{:0.1f}\t{:0.10f}\t{:0.10f}\t{:0.10f}\t{:0.10f}'
              .format(t[i], X_original[i], X_rkf45[i], X_euler[i], X_runge_kutta3[i]))
    print()


# Exploring with different step
exploring_with(step=0.1)
exploring_with(step=0.05)
exploring_with(step=0.025)
exploring_with(step=0.0125)
