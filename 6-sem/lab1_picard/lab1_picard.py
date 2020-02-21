from math import sqrt
from numpy import arange
from prettytable import PrettyTable

def func(x, u):
    return x ** 2  + u ** 2


def picard_1(x):
    return x ** 3 / 3


def picard_2(x):
    return x ** 3 / 3 * (1 + x ** 4 / 21)


def picard_3(x):
    return x ** 3 / 3 * (1 + (x ** 4 / 21) + (2 / 693 * x ** 8) + (1 / 19845 * x ** 12))


def picard_4(x):
    return x ** 3 / 3 + (x ** 7 / 63) + (2 / 2079 * x ** 11) + (13 / 218295 * x ** 15) + (82 / 37328445 * x ** 19) + \
           (662 / 10438212015 * x ** 23) + (4 / 3341878155 * x ** 27) + (x ** 31 / 10987690975)


def explicit_scheme(x, y, h):
    return y + h * func(x, y)


def implicit_scheme(x, y, h):
    D = 1 - 4 * h * (y + h * (x + h) ** 2)
    if D < 0:
        return float("NaN")
    else:
        return (1 - sqrt(D)) / (2 * h)


def calculate_picard(x_values, func):
    y_values = []
    for x_cur in x_values:
        result = func(x_cur)
        if result <= 10e+300:
            y_values.append(round(result, 8))
        else:
            y_values.append(float('inf'))

    return y_values


def calculate_euler(step, x_end, func):
    y_values = []
    y_values.append(0.0)
    for x_cur in arange(step, x_end + step, step):
        result = func(x_cur - step, y_values[-1], step)
        if result <= 10e+300:
            y_values.append(result)
        else:
            y_values.append(float('inf'))

    return y_values


if __name__ == "__main__":
    step = 0.000001
    x_end = 2

    x_values = []

    for i in arange(0, x_end + step, step):
        x_values.append(round(i, 5))

    picard_first = calculate_picard(x_values, picard_1)
    picard_second = calculate_picard(x_values, picard_2)
    picard_third = calculate_picard(x_values, picard_3)
    picard_fourth = calculate_picard(x_values, picard_4)
    euler_exp = calculate_euler(step, x_end, explicit_scheme)
    euler_imp = calculate_euler(step, x_end, implicit_scheme)

    table = PrettyTable()

    table = PrettyTable()
    table.add_column('X', x_values)
    table.add_column('Пикар (1 приближение)', picard_first)
    table.add_column('Пикар (2 приближение)', picard_second)
    table.add_column('Пикар (3 приближение)', picard_third)
    table.add_column('Пикар (4 приближение)', picard_fourth)
    table.add_column('Эйлер (явная схема)', euler_exp)
    table.add_column('Эйлер (неявная схема)', euler_imp)

    print(table)
