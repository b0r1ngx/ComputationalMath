import numpy as np
from scipy import linalg

N = 5
d = (10, 1000, 10000)

def create_matrix(n, d):
    for i in range(n):
        for k in range(n):
            # Knowing that in programming matrices and arrays start counting from 0
            # we must add these extra `+ 1` for each row(i) and column(k)
            C[i][k] = d + np.log2((i + 1) * (k + 1)) + np.cos((i + 1) * (k + 1))

for l in range(len(d)):
    C = np.zeros((N, N), dtype=np.float64)
    create_matrix(N, d[l])
    print('Матрица С:')
    print(C)
    print('Обратная матрица C:')
    invC = linalg.inv(C)
    print(invC)
    print('Матрица R:')
    R = np.eye(N) - invC * C
    print(R)
    print('Норма матрицы R:')
    print(linalg.norm(R, ord=1))
