import numpy
from matplotlib import pyplot
from scipy import integrate
from scipy import interpolate


def function05(T):
    return numpy.abs(T ** 2 + T - 2) ** (-0.5)


def function1(T):
    return numpy.abs(T ** 2 + T - 2) ** (-1)


def pick_step(func, a, b, step):
    X = numpy.arange(a, b, step)
    Y = func(X)
    return (X, Y)


def integrate_newton_cotes(func, a, b):
    N = 9
    X = numpy.linspace(a, b, N)
    A, B = integrate.newton_cotes(N - 1)
    result = 0

    for i in range(N):
        result += A[i] * func(X[i])

    result *= (b - a) / (N - 1)
    return result


def quanc8(func, a, b, ai, bi, abs_error, rel_error, rough=None):
    middle = (ai + bi) / 2

    P = integrate_newton_cotes(func, ai, bi)
    P1 = integrate_newton_cotes(func, ai, middle)
    P2 = integrate_newton_cotes(func, middle, bi)
    Q = P1 + P2

    error = numpy.abs((Q - P) / 1023)
    h = bi - ai

    if rough is None:
        rough = P

    if error <= h / (b - a) * numpy.max([abs_error, rel_error * rough]):
        return Q

    return quanc8(func, a, b, ai, middle, abs_error, rel_error, rough) + \
           quanc8(func, a, b, middle, bi, abs_error, rel_error, rough)


def f_quanc8(func, x):
    y = numpy.zeros(len(x))

    for i in range(len(y)):
        y[i] = quanc8(func, 0, x[i], 0, x[i], abs_error=0.00001, rel_error=0.0)

    return y


# m = -0.5
a = 0
b = 2
h = 0.2
X, Yg = pick_step(function05, a, b + h, step=h)

pyplot.title('X, Yg')
pyplot.plot(X, Yg, 'g-')
pyplot.show()

Yf = f_quanc8(function05, X)

pyplot.title('X, Yf')
pyplot.plot(X, Yf, 'r-')
pyplot.show()

# m = -1
X1, Yg1 = pick_step(function1, a, b + h, step=h)

pyplot.title('X1, Y1g')
pyplot.plot(X1, Yg1, 'b-')
pyplot.show()

Yf1 = f_quanc8(function1, X1)

# pyplot.title('X1, Y1f')
pyplot.plot(X, Yf1, 'k-')
pyplot.show()
