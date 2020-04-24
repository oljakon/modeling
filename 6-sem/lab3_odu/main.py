import matplotlib.pyplot as plt
import numpy as np

# коэффициенты теплопроводности и теплоотдачи
def k(x):
    return a / (x - b)

def alpha(x):
    return c / (x - d)


def p(x):
    return 2 * alpha(x) / R

def f(x):
    return 2 * alpha(x) * T0 / R


# метод средних
def x_plus_half(x):
    return (k(x) + k(x + h)) / 2

def x_minus_half(x):
    return (k(x) + k(x - h)) / 2


# коэффициенты разностной схемы
def A(x):
    return x_plus_half(x) / h

def C(x):
    return x_minus_half(x) / h

def B(x):
    return A(x) + C(x) + p(x) * h

def D(x):
    return f(x) * h


# левое граничное условие
def left_boundary_condition():
    K0 = x_plus_half(0) + h * h * (p(0) + p(h)) / 16 + h * h * p(0) / 4
    M0 = -x_plus_half(0) + h * h * (p(0) + p(h)) / 16
    P0 = h * F0 + h * h / 4 * ((f(0) + f(h)) / 2 + f(0))
    return K0, M0, P0

# правое граничное условие
def right_boundary_condition():
    KN = -x_minus_half(l) / h - aN - p(l) * h / 4 - ((p(l) + p(l - h)) * h) / 16
    MN = x_minus_half(l) / h - ((p(l) + p(l - h)) * h) / 16
    PN = - aN * T0 - h * (f(l) + f(l - h) + f(l)) / 8
    return KN, MN, PN


if __name__ == "__main__":
    K0 = 0.4
    KN = 0.1
    a0 = 0.05
    aN = 0.01
    l = 10
    T0 = 300
    R = 0.5
    F0 = 50
    h = 1e-3

    # параметры коэффициентов теплопроводности и теплоотдачи
    b = (KN * l) / (KN - K0)
    a = - K0 * b
    d = (aN * l) / (aN - a0)
    c = - a0 * d

    K0, M0, P0 = left_boundary_condition()
    KN, MN, PN = right_boundary_condition()

    # прямой ход
    # массивы прогоночных коэффициентов
    eps = [0]
    eta = [0]

    eps1 = -M0 / K0
    eta1 = P0 / K0

    eps.append(eps1)
    eta.append(eta1)

    x = h
    n = 1
    while x + h < l:
        eps.append(C(x) / (B(x) - A(x) * eps[n]))
        eta.append((A(x) * eta[n] + D(x)) / (B(x) - A(x) * eps[n]))
        n += 1
        x += h

    # обратный ход
    t = [0] * (n + 1)
    # значение функции в последней точке
    t[n] = (PN - MN * eta[n]) / (KN + MN * eps[n])

    for i in range(n - 1, -1, -1):
        t[i] = eps[i + 1] * t[i + 1] + eta[i + 1]

    x = [i for i in np.arange(0, l, h)]

    plt.plot(x, t[:-1])
    plt.xlabel("X, cm")
    plt.ylabel("T, K")
    plt.grid()
    plt.show()
