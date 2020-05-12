from scipy.integrate import quad as QUANC8
# Specified function with m = -1
def fx1(x):
    return abs(x ** 2 + x - 2) ** -1
# Specified function with m = -0.5
def f05(x):
    return abs(x ** 2 + x - 2) ** (-0.5)
# List with wanted allowable errors
err = [0.01, 0.005, 0.001, 0.0001, 0.000001]
# List with values after integration of function f1 at interval [0, 1-err]
f0 = []
# List with values after integration of function f1 at interval [1+err, 2]
f1 = []
# List with values after integration of function f05 at interval [0, 1-err]
f2 = []
# List with values after integration of function f05 at interval [1+err, 2]
f3 = []
# Fill lists with their values of computed integrals at given intervals
for i in range(len(err)):
    f0.append(QUANC8(lambda x: fx1(x), 0, 1 - err[i], limit=30))
for i in range(len(err)):
    f1.append(QUANC8(lambda x: fx1(x), 1 + err[i], 2, limit=30))
for i in range(len(err)):
    f2.append(QUANC8(lambda x: f05(x), 0, 1 - err[i], limit=30))
for i in range(len(err)):
    f3.append(QUANC8(lambda x: f05(x), 1 + err[i], 2, limit=30))
# Print values of computed integrals
for i in range(len(err)):
    print('Computed integral at m = -1, with allowable error {}%:'.format(round(err[i] * 100, 5)),
          ((f0[i] + f1[i])[0] - (f0[i] + f1[i])[2]))
for i in range(len(err)):
    print('Computed integral at m = -0.5, with allowable error {}%:'.format(round(err[i] * 100, 5)),
          ((f2[i] + f3[i])[0] - (f2[i] + f3[i])[2]))
