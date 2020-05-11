import numpy as np
import scipy.linalg as linalg


def matrix_C(d, rows, columns):
    C = np.full((rows, columns), 0.0)
    for i in rows:
        for k in columns:
            C[i][k] = d + np.log2(i * k) + np.cos(i * k)
    return C


def norm(rows, columns, R):
    max_ = 0.0
    temp = 0.0
    for i in rows:
        temp = 0.0
        for j in columns:
            temp += abs(R[i][j])
        if temp > max_:
            max_ = temp
    return max_


def cond(rows, columns, C):
    return norm(rows, columns, C) * norm(rows, columns, linalg.inv(C))


def solve(d, rows, columns):
    C = matrix_C(d, rows, columns)
    P, L, U = linalg.lu(C)

    t = linalg.solve_triangular(L, P, lower=True)
    w = linalg.solve_triangular(U, t)

    R = np.full((rows, columns), 0.0)

    for i in rows:
        for j in columns:
            for k in range(N):
                R[i][j] += C[i][k] * w[k][j]

    for i in rows:
        for j in columns:
            R[i][j] = R[i][j] - P[i][j]

    n = norm(N, R)
    c = cond(N, C)
    n1 = norm(N, C)
    n2 = norm(N, linalg.inv(C))

    print('C = \n', C)
    print('n = ', n)
    print('n1 = ', n1)
    print('n2 = ', n2)
    print('cond = ', c)
    print('W = ', w)
    print('R = ', R)
    print()


N = 5
solve(10, N, N)
solve(1000, N, N)
solve(10000, N, N)
