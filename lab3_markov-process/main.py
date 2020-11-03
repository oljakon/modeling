from random import random
from numpy import linalg
from prettytable import PrettyTable

TIME_DELTA = 1e-3
EPS = 1e-3


def limit_probabilities(matrix):
    n = len(matrix)
    return linalg.solve([[-sum(matrix[i]) + matrix[i][i] if i == j else matrix[j][i]for j in range(n)]
                         if i != n - 1 else [1 for j in range(n)] for i in range(n)],
                        [0 if i != n - 1 else 1 for i in range(n)]).tolist()


def probability_increments(matrix, start_probabilities):
    n = len(matrix)
    return [TIME_DELTA * sum([-sum(matrix[i]) * start_probabilities[j] if i == j
            else matrix[j][i] * start_probabilities[j] for j in range(n)])
            for i in range(n)]


def limit_times(matrix, limit_probabilities):
    n = len(matrix)
    start_probabilities = [1.0 / n for i in range(n)]
    current_time = 0.0
    current_probabilities = start_probabilities.copy()
    limit_times = [0.0 for i in range(n)]
    while not all(limit_times):
        dp = probability_increments(matrix, start_probabilities)
        for i in range(n):
            if not limit_times[i] and abs(current_probabilities[i] - limit_probabilities[i]) <= EPS:
                limit_times[i] = current_time
            current_probabilities[i] += dp[i]
            current_time += TIME_DELTA
    return limit_times


if __name__ == '__main__':
    size = 10

    matrix = [[round(random(), 4) if i != j else 0.0 for j in range(size)] for i in range(size)]

    table = PrettyTable()
    names = [""]
    for i in range(1, size + 1, 1):
        names.append(str(i))
    table.field_names = names

    for i in range(size):
        tmp = [i + 1]
        tmp.extend(item for item in matrix[i])
        table.add_row(tmp)
    print(table)

    probabilities = limit_probabilities(matrix)
    times = limit_times(matrix, probabilities)

    limit_table = PrettyTable()
    limit_table.field_names = ["", "Предельные вероятности", "Время нахождения в предельных состояниях"]
    for i in range(size):
        tmp = [i + 1]
        tmp.append(round(probabilities[i], 4))
        tmp.append(round(times[i], 4))
        limit_table.add_row(tmp)
    print(limit_table)
