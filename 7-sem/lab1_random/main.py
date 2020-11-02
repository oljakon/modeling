import math
import time
from scipy.stats import chisquare
from prettytable import PrettyTable


def program_generator(num, size):
    res = [0 for i in range(size + 1)]
    res[0] = math.ceil(time.time())
    for i in range(1, size + 1):
        res[i] = math.ceil(math.fmod((a * res[i - 1] + b), m))
    for i in range(size + 1):
        res[i] = str(res[i])[:num]
    res = [int(x) for x in res]
    return res[1:size+1]


def table_generator(num, size):
    ind = math.ceil(time.time()) % 10000
    digits = ""
    res = []
    with open('digits.txt', 'r') as f:
        for line in f.readlines():
            tmp = line.split()[1:]
            for elem in tmp:
                digits += elem
    while len(res) != size:
        val = digits[ind:ind+num]
        res.append(int(val))
        ind += num
    return res


def calculate_chi2(sequence):
    max_value = max(sequence)
    base = 1

    while max_value >= 1:
        max_value /= 10
        base *= 10

    freq_table = [0] * base
    for value in sequence:
        freq_table[value - base] += 1

    freq_table = [freq for freq in freq_table if freq != 0]
    chi2, prob = chisquare(freq_table)
    return chi2, prob


if __name__ == "__main__":
    n = 10
    n2 = 100

    m = 32767
    a = 1103515245 
    b = 12345

    progr1_10 = program_generator(1, n)
    progr2_10 = program_generator(2, n)
    progr3_10 = program_generator(3, n)

    progr_chi1_10 = calculate_chi2(progr1_10)
    progr_chi2_10 = calculate_chi2(progr2_10)
    progr_chi3_10 = calculate_chi2(progr3_10)

    table1_10 = table_generator(1, n)
    table2_10 = table_generator(2, n)
    table3_10 = table_generator(3, n)

    table_chi1_10 = calculate_chi2(table1_10)
    table_chi2_10 = calculate_chi2(table2_10)
    table_chi3_10 = calculate_chi2(table3_10)

    table1 = PrettyTable()
    table1.add_column("  N  ", [i for i in range(1, 11, 1)])
    table1.add_column("Одноразрядные", progr1_10)
    table1.add_column("Двухразрядные", progr2_10)
    table1.add_column("Трехразрядные", progr3_10)
    print("Программный генератор:")
    print(table1)

    print("Программный генератор: %d элементов" % n)
    print("1. Хи-квадрат(%f): %f" % (progr_chi1_10[0], progr_chi1_10[1]))
    print("2. Хи-квадрат(%f): %f" % (progr_chi2_10[0], progr_chi2_10[1]))
    print("3. Хи-квадрат(%f): %f" % (progr_chi3_10[0], progr_chi3_10[1]))

    table2 = PrettyTable()
    table2.add_column("  N  ", [i for i in range(1, 11, 1)])
    table2.add_column("Одноразрядные", table1_10)
    table2.add_column("Двухразрядные", table2_10)
    table2.add_column("Трехразрядные", table3_10)
    print("\n\nТабличный генератор:")
    print(table2)

    print("Табличный генератор: %d элементов" % n)
    print("1. Хи-квадрат(%f): %f" % (table_chi1_10[0], table_chi1_10[1]))
    print("2. Хи-квадрат(%f): %f" % (table_chi2_10[0], table_chi2_10[1]))
    print("3. Хи-квадрат(%f): %f" % (table_chi3_10[0], table_chi3_10[1]))


    progr1_100 = program_generator(1, n2)
    progr2_100 = program_generator(2, n2)
    progr3_100 = program_generator(3, n2)

    progr_chi1_100 = calculate_chi2(progr1_100)
    progr_chi2_100 = calculate_chi2(progr2_100)
    progr_chi3_100 = calculate_chi2(progr3_100)

    table1_100 = table_generator(1, n2)
    table2_100 = table_generator(2, n2)
    table3_100 = table_generator(3, n2)

    table_chi1_100 = calculate_chi2(table1_100)
    table_chi2_100 = calculate_chi2(table2_100)
    table_chi3_100 = calculate_chi2(table3_100)

    print("\n\nПрограммный генератор: %d элементов" % n2)
    print("1. Хи-квадрат(%f): %f" % (progr_chi1_100[0], progr_chi1_100[1]))
    print("2. Хи-квадрат(%f): %f" % (progr_chi2_100[0], progr_chi2_100[1]))
    print("3. Хи-квадрат(%f): %f" % (progr_chi3_100[0], progr_chi3_100[1]))

    print("\nТабличный генератор: %d элементов" % n2)
    print("1. Хи-квадрат(%f): %f" % (table_chi1_100[0], table_chi1_100[1]))
    print("2. Хи-квадрат(%f): %f" % (table_chi2_100[0], table_chi2_100[1]))
    print("3. Хи-квадрат(%f): %f" % (table_chi3_100[0], table_chi3_100[1]))