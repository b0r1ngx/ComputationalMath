import numpy
from matplotlib import pyplot
from scipy import integrate
from scipy import interpolate


def pick(func, a, b, count):
    '''
    Picks `count` points of `func` within
    the range `[a, b]`
    '''
    X = numpy.linspace(a, b, count)
    Y = func(X)
    return (X, Y)


def pick_step(func, a, b, step):
    '''
    Picks points of `func` within
    the range `[a, b]` with the
    specified `step`
    '''
    X = numpy.arange(a, b, step)
    Y = func(X)
    return (X, Y)


def lagrange(X, Y, Xn):
    '''
    Takes sample points of some function `(X, Y)` and calculates
    values at `Xn` via a lagrange polynom
    '''
    Yn = numpy.zeros(len(Xn))
    N = len(X)

    for k in range(0, N):
        t = numpy.ones(len(Xn))

        for j in range(0, k):
            t *= (Xn - X[j]) / (X[k] - X[j])

        for j in range(k + 1, N):
            t *= (Xn - X[j]) / (X[k] - X[j])

        Yn += Y[k] * t

    return Yn


def integrate_newton_cotes(func, a, b):
    '''
    Calculates an integral of `func`
    for t = a..b via newton-cotes of order 9.
    '''
    # Количество точек используемых в формуле Ньютона-Котеса
    N = 9

    # the 9 sample points
    X = numpy.linspace(a, b, N)

    # get newton-cotes coefficients
    # for the order N
    A, B = integrate.newton_cotes(N - 1)
    result = 0

    for it in range(N):
        result += A[it] * func(X[it])

    # multiply by the average step
    result *= (b - a) / (N - 1)
    return result


def quanc8(func, a, b, ai, bi, abs_error, rel_error, rough=None):
    '''
    Simulates QUANC8.
    `func` is the function we integrate.
    `rough` is an approximation of the a..b integral and
    will only be calculated at the 'root' call of quanc8
    recursion tree.
    '''
    middle = (ai + bi) / 2

    P = integrate_newton_cotes(func, ai, bi)
    P1 = integrate_newton_cotes(func, ai, middle)
    P2 = integrate_newton_cotes(func, middle, bi)
    Q = P1 + P2

    error = numpy.abs((Q - P) / 1023)
    h = bi - ai

    if rough == None:
        rough = P

    if error <= h / (b - a) * numpy.max([abs_error, rel_error * rough]):
        return Q

    return quanc8(func, a, b, ai, middle, abs_error, rel_error, rough) + \
           quanc8(func, a, b, middle, bi, abs_error, rel_error, rough)


def g(T):
    '''
    Function from inside of the integral
    '''
    return numpy.abs(T ** 2 + T - 2) ** -1


def f_quanc8(g, X):
    Y = numpy.zeros((len(X)))

    for it in range(len(Y)):
        Y[it] = quanc8(g, 0, X[it], 0, X[it], abs_error=0.00001, rel_error=0.0)

    return Y


# start and end of the range
a = 1
b = 3
h = 0.2

# +h, because I want b=3 to be included in our range
X, Yg = pick_step(g, a, b + h, step=h)

pyplot.title('Function g(t)')
pyplot.plot(X, Yg, 'g-')
pyplot.show()

Yf = f_quanc8(g, X)

pyplot.title('Function f(x)')
pyplot.plot(X, Yf, 'r-')
pyplot.show()

# Lagrange
Xk, Y_lagrange = pick(lambda Xn: lagrange(X, Yf, Xn), a, b, count=1000)

pyplot.title('Lagrange over (X, Yf)')
pyplot.plot(Xk, Y_lagrange, 'b-')
pyplot.show()

# Spline
coefficients = interpolate.CubicSpline(X, Yf)
Y_spline = coefficients(Xk)

pyplot.title('Spline over (X, Yf)')
pyplot.plot(Xk, Y_spline, 'k-')
pyplot.show()

# Comparison
# inverval start, step and count
# of points
l = 1.1
s = 0.2
c = 10

# hp for high precision
Xhp, Yhp = pick(lambda X: f_quanc8(g, X), l, l + s * c, count=c)

Yhp_lagrange = lagrange(X, Yf, Xhp)
Yhp_spline = coefficients(Xhp)

print('\t\t\t\tRaw Values')
print('X\tLagrange\t\tQUANC8\t\t\tSPLINE')

for it in range(len(Xhp)):
    print('{:0.1f}\t{}\t{}\t{}'.format(Xhp[it], Yhp_lagrange[it], Yhp[it], Yhp_spline[it]))

print()
print('\t\t\t\tDifference')
print('Lagrange:\t' + str(((Yhp_lagrange - Yhp) ** 2).sum()))
print('  Spline:\t' + str(((Yhp_spline - Yhp) ** 2).sum()))
