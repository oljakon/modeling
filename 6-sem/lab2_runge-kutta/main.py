from matplotlib import pyplot as plt
from numpy import arange
from math import pi
from scipy import integrate
from scipy.interpolate import InterpolatedUnivariateSpline


table1 = [[0.5, 6400, 0.4],
          [1.0, 6790, 0.55],
          [5.0, 7150, 1.7],
          [10.0, 7270, 3],
          [50.0, 8010, 11],
          [200.0, 9185, 32],
          [400.0, 10010, 40],
          [800.0, 11140, 41],
          [1200.0, 12010, 39]]


table2 = [[4000,  0.031],
          [5000, 0.27],
          [6000, 2.05],
          [7000, 6.06],
          [8000, 12],
          [9000, 19.9],
          [10000, 29.6],
          [11000, 41.1],
          [12000, 54.1],
          [13000, 67.7],
          [14000, 81.5]]


def f(x, y, z, Rp):
    return -((Rk + Rp) * y - z) / Lk


def phi(x, y, z):
    return -y / Ck


def interpolate(x, x_mas, y_mas):
    order = 1
    s = InterpolatedUnivariateSpline(x_mas, y_mas, k=order)
    return float(s(x))


def T(z):
    return T0 + (Tw - T0) * z ** m


def sigma(T):
    T_from_table = []
    for i in range (len(table2)):
        T_from_table.append(table2[i][0])

    sigm_from_table = []
    for j in range(len(table2)):
        sigm_from_table.append(table2[j][1])

    return interpolate(T, T_from_table, sigm_from_table)


def Rp(I):
    global m
    global T0

    I_from_table = []
    for i in range(len(table1)):
        I_from_table.append(table1[i][0])

    T0_from_table = []
    for j in range(len(table1)):
        T0_from_table.append(table1[j][1])

    m_from_table = []
    for z in range(len(table1)):
        m_from_table.append(table1[z][2])

    m = interpolate(I, I_from_table, m_from_table)
    T0 = interpolate(I, I_from_table, T0_from_table)

    func = lambda z: sigma(T(z)) * z
    integral = integrate.quad(func, 0, 1)
    Rp = Le / (2 * pi * R ** 2 * integral[0])

    return Rp


def runge_kutta_second_order(xn, yn, zn, hn, Rp):
    alpha = 0.5
    y_next = yn + hn * ((1 - alpha) * f(xn, yn, zn, Rp) + alpha * f(xn + hn / (2 * alpha),
                yn + hn / (2 * alpha) * f(xn, yn, zn, Rp),
                zn + hn / (2 * alpha) * phi(xn, yn, zn), Rp))

    z_next = zn + hn * ((1 - alpha) * phi(xn, yn, zn) + alpha * phi(xn + hn / (2 * alpha),
                yn + hn / (2 * alpha) * f(xn, yn, zn, Rp),
                zn + hn / (2 * alpha) * phi(xn, yn, zn)))

    return y_next, z_next


def runge_kutta_fourth_order(xn, yn, zn, hn, Rp):
    k1 = hn * f(xn, yn, zn, Rp)
    q1 = hn * phi(xn, yn, zn)

    k2 = hn * f(xn + hn / 2, yn + k1 / 2, zn + q1 / 2, Rp)
    q2 = hn * phi(xn + hn / 2, yn + k1 / 2, zn + q1 / 2)

    k3 = hn * f(xn + hn / 2, yn + k2 / 2, zn + q2 / 2, Rp)
    q3 = hn * phi(xn + hn / 2, yn + k2 / 2, zn + q2 / 2)

    k4 = hn * f(xn + hn, yn + k3, zn + q3, Rp)
    q4 = hn * phi(xn + hn, yn + k3, zn + q3)

    y_next = yn + (k1 + 2 * k2 + 2 * k3 + k4) / 6
    z_next = zn + (q1 + 2 * q2 + 2 * q3 + q4) / 6

    return y_next, z_next


if __name__ == "__main__":
    R = 0.35
    Le = 12
    T0 = 0.0
    Tw = 2000.0
    m = 0.0

    Ck = 150e-6
    Lk = 60e-6
    Rk = 1
    Uc0 = 1500.0
    I0 = 0.5

    '''Lk = float(input("Введите индуктивность Lk: ")) 
    Ck = float(input("Введите емкость конденсатора Ck: "))
    Rk = float(input("Введите сопротивление Rk: "))
    Uc0 = float(input("Введите напряжение на конденсаторе в начальный момент времени Uc0: "))
    I0 = float(input("Введите силу тока в цепи в начальный момент времени I0: "))'''

    I_2order = I_4order = I0
    Uc_2order = Uc_4order = Uc0

    t_plot = []

    I_2order_plot = []
    U_2order_plot = []
    Rp_2order_plot = []
    T_2order_plot = []

    I_4order_plot = []
    U_4order_plot = []
    Rp_4order_plot = []
    T_4order_plot = []

    h = 1e-6
    for t in arange(0, 0.0003, h):
        Rp_2order = Rp(I_2order)
        Rp_4order = Rp(I_4order)
        if t > h:
            t_plot.append(t)
            I_2order_plot.append(I_2order)
            T_2order_plot.append(T0)
            U_2order_plot.append(Uc_2order)
            Rp_2order_plot.append(Rp_2order)
            I_4order_plot.append(I_4order)
            T_4order_plot.append(T0)
            U_4order_plot.append(Uc_4order)
            Rp_4order_plot.append(Rp_4order)
        I_2order, Uc_2order = runge_kutta_second_order(t, I_2order, Uc_2order, h, Rp_2order)
        I_4order, Uc_4order = runge_kutta_fourth_order(t, I_4order, Uc_4order, h, Rp_4order)

    plt.figure(1)
    plt.subplot(321)
    plt.plot(t_plot, I_4order_plot, label='I (4 order)')
    plt.xlabel('t')
    plt.ylabel('I, А (4 order)')
    plt.grid(True)

    plt.subplot(322)
    plt.plot(t_plot, U_4order_plot, label='Uc (4 order)')
    plt.xlabel('t')
    plt.ylabel('Uc, В (4 order)')
    plt.grid(True)

    plt.subplot(323)
    plt.plot(t_plot, Rp_4order_plot, label='Rp (4 order)')
    plt.xlabel('t')
    plt.ylabel('Rp, Ом (4 order)')
    plt.grid(True)

    for i in range(len(I_4order_plot)):
        I_4order_plot[i] *= Rp_4order_plot[i]

    plt.subplot(324)
    plt.plot(t_plot, I_4order_plot, label='I*Rp (4 order)')
    plt.xlabel('t')
    plt.ylabel('I*Rp, В (4 order)')
    plt.grid(True)

    plt.subplot(325)
    plt.plot(t_plot, T_4order_plot, label='T (4 order)')
    plt.xlabel('t')
    plt.ylabel('T, К (4 order)')
    plt.grid(True)


    plt.figure(2)
    plt.subplot(321)
    plt.plot(t_plot, I_2order_plot, label='I (2 order)')
    plt.xlabel('t')
    plt.ylabel('I, А (2 order)')
    plt.grid(True)

    plt.subplot(322)
    plt.plot(t_plot, U_2order_plot, label='Uc (2 order)')
    plt.xlabel('t')
    plt.ylabel('Uc, В (2 order)')
    plt.grid(True)

    plt.subplot(323)
    plt.plot(t_plot, Rp_2order_plot, label='Rp (2 order)')
    plt.xlabel('t')
    plt.ylabel('Rp, Ом (2 order)')
    plt.grid(True)

    for i in range(len(I_2order_plot)):
        I_2order_plot[i] *= Rp_2order_plot[i]

    plt.subplot(324)
    plt.plot(t_plot, I_2order_plot, label='I*Rp (2 order)')
    plt.xlabel('t')
    plt.ylabel('I*Rp, В (2 order)')
    plt.grid(True)

    plt.subplot(325)
    plt.plot(t_plot, T_2order_plot, label='T (2 order)')
    plt.xlabel('t')
    plt.ylabel('T, К (2 order)')
    plt.grid(True)

    plt.show()