import matplotlib.pyplot as plt
import numpy as np
from math import fabs

a1 = 0.0134
b1 = 1
c1 = 4.35e-4
m1 = 1
a2 = 2.049
b2 = 0.563e-3
c2 = 0.528e5
m2 = 1
alpha0 = 0.05
alphaN = 0.01
l = 10
T0 = 300
R = 0.5
F0 = 50

h = 1e-3
t = 1


def k(T):
    return a1 * (b1 + c1 * T ** m1)


def c(T):
    return a2 + b2 * T ** m2 - (c2 / T ** 2)


def alpha(x):
    d = (alphaN * l) / (alphaN - alpha0)
    c = - alpha0 * d
    return c / (x - d)


def p(x):
    return 2 * alpha(x) / R


def f(x):
    return 2 * alpha(x) * T0 / R


def func_plus_half(x, step, func):
    return (func(x) + func(x + step)) / 2


def func_minus_half(x, step, func):
    return (func(x) + func(x - step)) / 2


def A(T):
    return t / h * func_minus_half(T, t, k)


def D(T):
    return t / h * func_plus_half(T, t, k)


def B(x, T):
    return A(T) + D(T) + c(T) * h + p(x) * h * t


def F(x, T):
    return f(x) * h * t + c(T) * T * h


def left_boundary_condition(T_prev):
    K0 = h / 8 * func_plus_half(T_prev[0], t, c) + h / 4 * c(T_prev[0]) + \
         func_plus_half(T_prev[0], t, k) * t / h + \
         t * h / 8 * p(h / 2) + t * h / 4 * p(0)

    M0 = h / 8 * func_plus_half(T_prev[0], t, c) - \
         func_plus_half(T_prev[0], t, k) * t / h + \
         t * h * p(h / 2) / 8

    P0 = h / 8 * func_plus_half(T_prev[0], t, c) * (T_prev[0] + T_prev[1]) + \
         h / 4 * c(T_prev[0]) * T_prev[0] + \
         F0 * t + t * h / 8 * (3 * f(0) + f(h))

    return K0, M0, P0


def right_boundary_condition(T_prev):
    KN = h / 8 * func_minus_half(T_prev[-1], t, c) + h / 4 * c(T_prev[-1]) + \
         func_minus_half(T_prev[-1], t, k) * t / h + t * alphaN + \
         t * h / 8 * p(l - h / 2) + t * h / 4 * p(l)

    MN = h / 8 * func_minus_half(T_prev[-1], t, c) - \
         func_minus_half(T_prev[-1], t, k) * t / h + \
         t * h * p(l - h / 2) / 8

    PN = h / 8 * func_minus_half(T_prev[-1], t, c) * (T_prev[-1] + T_prev[-2]) + \
         h / 4 * c(T_prev[-1]) * T_prev[-1] + t * alphaN * T0 + \
         t * h / 4 * (f(l) + f(l - h / 2))

    return KN, MN, PN


def run(T_prev, K0, M0, P0, KN, MN, PN):
    eps = [0, -M0 / K0]
    eta = [0, P0 / K0]

    x = h
    n = 1
    while (x + h < l):
        eps.append(D(T_prev[n]) / (B(x, T_prev[n]) - A(T_prev[n]) * eps[n]))
        eta.append((F(x, T_prev[n]) + A(T_prev[n]) * eta[n]) / (B(x, T_prev[n]) - A(T_prev[n]) * eps[n]))
        n += 1
        x += h

    y = [0] * (n + 1)
    y[n] = (PN - MN * eta[n]) / (KN + MN * eps[n])

    for i in range(n - 1, -1, -1):
        y[i] = eps[i + 1] * y[i + 1] + eta[i + 1]

    return y


def main():
    # Метод простых итераций
    step1 = int(l / h)
    T = [T0] * (step1 + 1)
    T_new = [0] * (step1 + 1)
    ti = 0
    res = []
    res.append(T)

    while True:
        prev = T
        while True:
            K0, M0, P0 = left_boundary_condition(prev)
            KN, MN, PN = right_boundary_condition(prev)
            T_new = run(prev, K0, M0, P0, KN, MN, PN)

            max = fabs((T[0] - T_new[0]) / T_new[0])
            for step2, j in zip(T, T_new):
                d = fabs(step2 - j) / j
                if d > max:
                    max = d
            if max < 1:
                break

            prev = T_new
        res.append(T_new)
        ti += t

        check_eps = 0
        for i, j in zip(T, T_new):
            if fabs((i - j) / j) > 1e-2:
                check_eps = 1
        if check_eps == 0:
            break
        T = T_new

    x = [i for i in np.arange(0, l, h)]
    te = [i for i in range(0, ti, t)]

    step1 = 0
    for i in res:
        if (step1 % 2 == 0):
            plt.plot(x, i[:-1])
        step1 += 1
    plt.plot(x, res[-1][:-1])
    plt.xlabel("x, cm")
    plt.ylabel("T, K")
    plt.grid()
    plt.show()

    step2 = 0
    while (step2 < l / 3):
        point = [j[int(step2 / h)] for j in res]
        plt.plot(te, point[:-1])
        step2 += 0.1
    plt.xlabel("t, sec")
    plt.ylabel("T, K")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()