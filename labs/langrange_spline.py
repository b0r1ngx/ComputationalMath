# Основные математические функции
import numpy as np
# Интеполяция и получение значений функции
# при помощью полинома Лагранжа и Сплайн-функции
from scipy.interpolate import lagrange, CubicSpline
# Презентация функций с помощью графиков
import matplotlib.pyplot as plot
# Исходная функция по заданию
def f(x):
    return np.sin(x ** 2)
# Узлы для построения
xk = np.array([round(0.2 * k, 1) for k in range(7)])
# Полином Лагранжа 6-й степени
Lx = lagrange(xk, f(xk))
# Сплайн-функция
Sx = CubicSpline(xk, f(xk))
# Точки в которых будем вычислять значения всех заданных функций
yk = np.array([round(0.1 + 0.2 * k, 1) for k in range(6)])
# Блок вывода графиков и данных в консоль
plot.title('f(x) = sin(x^2)')
plot.plot(xk, f(xk), 'tab:orange')
plot.show()

plot.title('L(x)')
plot.plot(xk, Lx(xk), 'g-')
plot.show()

plot.title('S(x)')
plot.plot(xk, Lx(xk), 'r-')
plot.show()
# График совмещения всех заданных функций
fig, ax = plot.subplots(figsize=(6.5, 4))
ax.plot(xk, f(xk), 'o', label='xk')
ax.plot(xk, f(xk), label='f(x)')
ax.plot(xk, Lx(xk), label='L(x)')
ax.plot(xk, Sx(xk), label='S(x)')
ax.legend(loc='upper left', ncol=2)
plot.show()

print('\t'*5 + 'Values of each point of Yk:')
print('Yk\t\tf(x)=sin(x^2)\t\t\tL(x)\t\t\t\tS(x)')
for i in range(len(yk)):
    print('{}\t\t{:0.10f}\t\t{:0.10f}\t\t{:0.10f}'.format(yk[i], f(yk[i]), Lx(yk[i]), Sx(yk[i])))
print()
print('\t\t\tDifference between affine functions:')
print('f(x): ' + str((f(yk) ** 2).sum()))
print('L(x): ' + str((Lx(yk) ** 2).sum()))
print('S(x): ' + str((Sx(yk) ** 2).sum()))
