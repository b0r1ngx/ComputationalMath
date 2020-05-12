import numpy
import scipy.linalg as linalg


def create_A(x, N):
    A = numpy.full((N, N), 1.1)

    for i in range(N):
        for j in range(N):
            A[i][j] = j + 1

    for it in range(N - 1):
        A[it + 1][it + 1] = x + 1

    return A


def norm(N, R):
    temp = 0.0
    max = 0.0

    for i in range(N):
        temp = 0.0

        for j in range(N):
            temp += abs(R[i][j])

        if temp > max:
            max = temp

    return max

def cond(N, A):
    return norm(N, A) * norm(N, linalg.inv(A))


def solve_system(x, N):
    A = create_A(x, N)
    P, L, U = linalg.lu(A)

    t = linalg.solve_triangular(L, P, lower=True)
    w = linalg.solve_triangular(U, t)

    R = numpy.full((N, N), 0.0)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                R[i][j] += A[i][k] * w[k][j]

    for i in range(N):
        for j in range(N):
            R[i][j] = R[i][j] - P[i][j]

    n = norm(N, R)
    c = cond(N, A)
    n1 = norm(N, A)
    n2 = norm(N, linalg.inv(A))

    print('A = \n', A)
    print('n = ', n)
    print('n1 = ', n1)
    print('n2 = ', n2)
    print('cond = ', c)
    print('W = ', w)
    print('R = ', R)
    print()

N = 5

solve_system(1.1, N)
solve_system(1.001, N)
solve_system(1.00001, N)