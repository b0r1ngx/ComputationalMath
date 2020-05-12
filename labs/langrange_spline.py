# Основные математические функции
import numpy as np
# Интеполяция и получение значений функции
# при помощью полинома Лагранжа и Сплайн-функция
from scipy.interpolate import lagrange, CubicSpline
# Презентация функции с помощью графика
import matplotlib.pyplot as plot


# Функция
def f(x):
    return np.sin(x ** 2)


# Узлы для построения
xk = np.array([round(0.2 * k, 1) for k in range(7)])

# Полином Лагранжа 6-й степени
Lx = lagrange(xk, f(xk))
# Сплайн-функция
Sx = CubicSpline(xk, f(xk))

yk = [round(0.1 + 0.2 * k, 1) for k in range(6)]

x = np.arange(0, 5, 0.1)
y = f(x)
plot.title('sin^2')
plot.plot(x, y)
plot.show()