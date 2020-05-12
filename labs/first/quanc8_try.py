import numpy as np

from first.QUANC8 import QUANC8


def f(x):
    return np.abs(x ** 2 + x - 2) ** -1

FUN = f
A = 0.0
B = 2.1
ABSERR = 0.00001
RELERR = 0.00001  # +00000
RESULT = 0.0
ERREST = 0.0
FLAG = 0.0
NOFUN = 0
QUANC8(FUN, A, B, ABSERR, RELERR, RESULT, ERREST, NOFUN, FLAG)

print(RESULT)
print(ERREST)
print(NOFUN)
print(FLAG)

