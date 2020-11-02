import matplotlib.pyplot as plt
import numpy as np
from math import factorial, exp


def even_distribution(a, b, x):
    if a <= x < b:
        return (x - a) / (b - a)
    elif x < a:
        return 0
    else:
        return 1


def even_density(a, b, x):
    if a <= x <= b:
        return 1 / (b - a)
    else:
        return 0


def erlang_density(l, k, x):
    if x < 0:
        return 0
    return ((l ** k) * (x ** (k - 1)) * exp(-l * x)) / factorial(k - 1)


def erlang_distribution(l, k, x):
    if x < 0:
        return 0
    sum = 0
    for i in range(0, int(k)):
        sum += (exp(-l * x) * ((l * x) ** i)) / factorial(i)
    return 1 - sum


def erlang_second_bound(l, k):
    second_bound = 0
    while erlang_distribution(l, k, second_bound) < 0.999:
        second_bound += 1
    return second_bound + 1


if __name__ == "__main__":
    a = -3
    b = 3
    step = 1e-3
    diff = b - a
    val1 = a - diff / 2
    val2 = b + diff / 2

    even_x = np.arange(val1, val2, step)

    even_data_distribution = [even_distribution(a, b, val) for val in even_x]
    even_data_density = [even_density(a, b, val) for val in even_x]

    plt.figure(figsize=(14, 5))
    plt.subplot(121)
    plt.plot(even_x, even_data_distribution, color="red")
    plt.title('Функция равномерного распределения')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.grid(True)

    plt.subplot(122)
    plt.plot(even_x, even_data_density, color="red")
    plt.title('Плотность равномерного распределения')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)

    plt.show()

    l = 3
    k = 3
    second_bound = erlang_second_bound(l, k)

    erlang_x = np.arange(0, second_bound, step)

    erlang_data_density = [erlang_density(l, k, val) for val in erlang_x]
    erlang_data_distribution = [erlang_distribution(l, k, val) for val in erlang_x]

    plt.figure(figsize=(14,5))
    plt.subplot(121)
    plt.plot(erlang_x, erlang_data_distribution)
    plt.title('Функция распределения Эрланга')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.grid(True)

    plt.subplot(122)
    plt.plot(erlang_x, erlang_data_density)
    plt.title('Плотность распределения Эрланга')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)

    plt.show()