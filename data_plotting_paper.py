import csv
import datetime
import pandas as pd

import matplotlib.pyplot as plt


def parse_pred_file(order, dist, threshold):
    for instance in instances:
        # pre-analyse trivial predictions:
        trivial_predictions = []
        general_predictions = []
        with open('../analysis_data/predictions/bpi19-' + str(order) + '-' + str(dist) + '-' + str(threshold) + '_' + str(instance) + '.csv') as pred_file:
            r = csv.reader(pred_file, delimiter= ',')
            count_0 = 0
            count_1 = 0
            count_total = 0
            summands = []
            for row_idx, row in enumerate(r):
                pred = int(row[3])
                if pred == -1:
                    count_1 += 1
                elif pred == 0:
                    count_0 += 1
                else:
                    with open("data/instances/" + str(instance) + ".csv") as actual:
                        r = csv.reader(actual)
                        for i in range(0, row_idx):
                            next(r)
                        current_event = next(r)
                        # assert(row[1] == current_event[19])
                        actual_spread = -1
                        counter = 0
                        for i in range(0, pred):
                            next_event = next(r)
                            counter += 1
                            if next_event[19] == 'Clear Invoice':
                                actual_spread = counter
                                break
                        if actual_spread != -1:
                            summands.append(1-(pred-actual_spread)/dist)
                count_total += 1
            trivial_predictions.append(count_0 + count_1)
            general_predictions.append(count_total)
            if len(summands) == 0:
                quality = 1.0
                if order == 2:
                    print("")
            else:
                quality = sum(summands) / len(summands)
        return sum(trivial_predictions) / sum(general_predictions), quality


thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
max_distances = [2, 3, 5, 10]
orders = [1, 2]
instances = range(0, 100)
precisions = {}
colors = ["#F6A800", "#DD640C", "#B1063A", "#B10ffB"]

# get precisions
for order in orders:
    precisions[order] = {}
    for dist in max_distances:
        with open('../analysis_data/logs/precision_' + str(order) + '_' + str(dist) + '.csv') as f:
            r = csv.reader(f)
            precisions[order][dist] = []
            for prec in r:
                precisions[order][dist].append(float(prec[0]))

for order in orders:
    non_trivial_percentages = []
    spread_qualities = []
    for i, d in enumerate(max_distances):
        non_trivial_percentages.append([])
        spread_qualities.append([])
        for t in thresholds:
            trivial, spread_quality = parse_pred_file(order, d, t)
            non_trivial_percentages[i].append(1 - trivial)
            spread_qualities[i].append(spread_quality)
        plt.plot(thresholds, precisions[order][d], "-", color=colors[i], label='precision')
        plt.plot(thresholds, non_trivial_percentages[i], '--', color=colors[i], label='non_trivial_perc')
        plt.plot(thresholds, spread_qualities[i], ':', color=colors[i], label='spread_quality')
        plt.plot(thresholds, precisions[order][d], ".", color=colors[i])
        plt.plot(thresholds, non_trivial_percentages[i], '.', color=colors[i])
        plt.plot(thresholds, spread_qualities[i], '.', color=colors[i])
        plt.legend()
        plt.title("Maximal Distance " + str(d))
        axes = plt.gca()
        axes.set_ylim([0.0, 1.1])
        plt.xlabel('Threshold')
        plt.savefig("results/" + str(order) + "_" + str(d) + ".png")
        plt.show()

for o in orders:
    times = []
    times_d = {}
    for d in max_distances:
        times_d[d] = []
        with open("../analysis_data/logs/duration_" + str(o) + "_" + str(d) + ".csv") as f:
            for t in f:
                t = float(t)
                times.append(t)
                times_d[d].append(t)
    mean_times = []
    for key, value in times_d.items():
        mean_times.append(round(sum(value) / len(value) * 1000, 4))
    plt.plot(max_distances, mean_times)
    print("Mean times ms order " + str(o) + ": " + str(mean_times))
    print("Mean Duration order " + str(o) + ": " + str(sum(times) / len(times)))
    print("Times for Order " + str(o) + ": " + str(times_d))
plt.legend()
plt.title("Mean Performance")
axes = plt.gca()
axes.set_ylim([0.0, 5])
plt.xlabel('Threshold')
plt.savefig("results/performance.png")
plt.show()

for order, ps in precisions.items():
    mean_order = []
    for k, p in ps.items():
        mean = sum(p)/len(p)
        mean_order.append(mean)
        # print("Mean Prec Order " + str(order) + ", dist " + str(k) + ": " + str(mean))
    print("Mean Prec Order " + str(order) + ": " + str(sum(mean_order)/len(mean_order)))

print(precisions[1])
print(precisions[2])

print(min(precisions[2][3]))
print(max(precisions[2][2]))
