import csv

import math
import matplotlib.pyplot as plt
import numpy as np

filename = 'ikkanditnietuitspreken.csv'

columns = {}
rows = []
data = {}


# hulp functie om te kijken of de waarde een integer is
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        # anders reageren als het de eerste regel is, dat zijn namelijk de kolomnamen
        if line_count == 0:
            line_count += 1
            i = 0
            for c in row:
                columns[c] = i
                data[i] = []
                i += 1
        else:
            line_count += 1
            # alleen importeren als het maanddata is, niet de cummulatieven over een jaar
            if 'JJ00' in row[columns['Perioden']]:
                pass
            else:
                rows.append(row)
                i = 0
                for c in row:
                    if is_number(c):
                        data[i].append(int(c))
                    else:
                        data[i].append(c)
                    i = i + 1
    print(f'Processed {line_count} lines.')


def calculate_mean(ls, stringify=False):
    if stringify:
        return str(calculate_sum(ls) / calculate_len(ls))
    return calculate_sum(ls) / calculate_len(ls)


def calculate_sum(ls):
    outcome = 0

    for iter in ls:
        outcome += int(iter)
    return outcome


def calculate_len(ls):
    if isinstance(ls, (float, int)):
        return int(ls)

    teller = 0
    for iter in ls:
        teller += 1
    return int(teller)


def quick_sort(l):
    if len(l) <= 1:
        return l
    else:
        return quick_sort([e for e in l[1:] if e <= l[0]]) + [l[0]] + \
               quick_sort([e for e in l[1:] if e > l[0]])


def low_to_high(l):
    return quick_sort(l)


def high_to_low(l):
    return reverse_list(quick_sort(l))


def reverse_list(l):
    return [l[-1]] + reverse_list(l[:-1]) if l else []


def calculate_median(var):
    if len(var) == 0:
        return None
    else:
        sorted = quick_sort(var)
        return sorted[int(calculate_len(sorted) / 2)]


def calculate_list_multiplication(ls1, ls2):
    """ Under the assumption that both lists are the exact same length"""

    if calculate_len(ls1) == calculate_len(ls2):
        outcome = list()
        for i in range(len(ls1)):
            outcome.append(ls1[i] * ls2[i])
        return outcome


def get_highest_list(ls):
    highest = 0
    for x in ls:
        if x > 0:
            highest = x
    return highest


def get_highest_dict(dc):
    highest_val = 0
    occ_val = 0

    for val, occ_count in dc.items():
        if highest_val < occ_count:
            occ_val = val
            highest_val = occ_count
    return occ_val


def calculate_mode(ls):
    occ_counter = {}
    for value in ls:
        if value in occ_counter.keys():
            occ_counter[value] += 1
        else:
            occ_counter[value] = 1

    return get_highest_dict(occ_counter)


def calculate_standard_deviation(var):
    return math.sqrt(
        calculate_sum(pow(x - calculate_sum(var) / calculate_len(var), 2) for x in var) / calculate_len(var))


def calculate_confidence_interval(ls):
    standard_deviation = calculate_standard_deviation(ls)
    length = calculate_len(ls)
    mean = calculate_mean(ls)
    return [mean + 1.96 * (standard_deviation / (length ** .5)), mean - 1.96 * (standard_deviation / (length ** .5))]


def calculate_linear_regression(lst):
    """Based on https://www.sciencedirect.com/topics/engineering/regression-coefficient"""
    x = list(range(1, calculate_len(lst) + 1))
    y = lst

    ln = calculate_len(x)
    mean_x = calculate_mean(x)
    mean_y = calculate_mean(y)

    sum_xy = calculate_sum([a * b for a, b in zip(y, x)]) - ln * mean_y * mean_x
    sum_xx = calculate_sum([a * b for a, b in zip(x, x)]) - ln * mean_x * mean_x

    # regression
    z1 = sum_xy / sum_xx
    z0 = mean_y - z1 * mean_x

    return x, y, (z0, z1)


# Used to print all data and all column records
for column in columns:
    column_data = data[columns[column]]
    if is_number(column_data[0]):

        print(column)
        print("Gemiddlde: " + str(calculate_mean(column_data)))
        print("Mediaan: " + str(calculate_median(column_data)))
        print("Modus: " + str(calculate_mode(column_data)))
        print("Standard deviation: " + str(calculate_standard_deviation(column_data)))
        print('\r\n')

        set_ordered_by_magnitude = low_to_high(column_data)

        plt.subplots()

        incremental_increase = (set_ordered_by_magnitude[-1] - set_ordered_by_magnitude[0]) / 20

        plt.hist(set_ordered_by_magnitude,
                 bins=np.arange(min(set_ordered_by_magnitude), max(set_ordered_by_magnitude) + incremental_increase,
                                incremental_increase))

        mean = calculate_mean(set_ordered_by_magnitude)
        plt.axvline(x=mean, color='red')

        for iter in calculate_confidence_interval(set_ordered_by_magnitude):
            plt.axvline(x=iter, color='blue', linestyle='-.')

        plt.show()

        x_prediction, y, predicative = calculate_linear_regression(set_ordered_by_magnitude)

        plt.subplots()

        plt.scatter(x_prediction, y, color="red", s=15)

        y_axis_prediction = [predicative[0] + (coordinate * predicative[1]) for coordinate in x_prediction]

        plt.plot(x_prediction, y_axis_prediction, color="blue")
        plt.title('Trend')
        plt.xlabel('Period')
        plt.show()
