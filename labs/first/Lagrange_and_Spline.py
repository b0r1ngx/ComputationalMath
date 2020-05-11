import numpy
from matplotlib import pyplot
from scipy import integrate
from scipy import interpolate


def function(x):
    return numpy.sin(x ** 2)


def lagrange(X, Y, Xn):
    Yn = numpy.zeros(len(Xn))
    n = len(X)

    for k in range(0, n):
        t = numpy.ones(len(Xn))

        for j in range(0, k):
            t *= (Xn - X[j]) / (X[k] - X[j])

        for j in range(k + 1, n):
            t *= (Xn - X[j]) / (X[k] - X[j])

        Yn += Y[k] * t

    return Yn

def pick(func, a, b, count):
    X = numpy.linspace(a, b, count)
    Y = func(X)
    return (X, Y)


a = -0.1
b = 1.3
# Lagrange
Xk, Y = pick(lambda Xn: lagrange(X, Yf, Xn), a, b, count=1000)

pyplot.title('Lagrange over (X, Yf)')
pyplot.plot(Xk, Y, 'b-')
pyplot.show()

# Spline
coefficients = interpolate.CubicSpline(X, Yf)
Y_spline = coefficients(Xk)

pyplot.title('Spline over (X, Yf)')
pyplot.plot(Xk, Y_spline, 'k-')
pyplot.show()
