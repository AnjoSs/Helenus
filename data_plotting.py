import csv

import matplotlib.pyplot as plt


def parse_pred_file(file_path, max_dist):
    with open(file_path) as pred_file:
        r = csv.reader(pred_file, delimiter=';')
        count_1 = 0
        count_0 = 0
        spread = 0
        count_total = 0
        summands = []
        for row_idx, row in enumerate(r):
            pred = int(row[3])
            if pred == -1:
                count_1 += 1
            elif pred == 0:
                count_0 += 1
            else:
                with open("data/mate.csv") as actual:
                    r = csv.reader(actual)
                    for i in range(0, row_idx):
                        next(r)
                    current_event = next(r)
                    assert(row[1] == current_event[0])
                    actual_spread = -1
                    counter = 0
                    for i in range(0, pred):
                        next_event = next(r)
                        counter += 1
                        if next_event[0] == 's':
                            actual_spread = counter
                            break
                    if actual_spread != -1:
                        summands.append(1-(pred-actual_spread)/max_dist)
            count_total += 1
        assert(len(summands) == count_total)
        spread_quality = sum(summands)/count_total
        # print("-1 percentage: " + str(count_1 / count_total) +
        #       "\n0 percentage: " + str(count_0 / count_total) +
        #       "\nmax spread: " + str(max_spread))
        return (count_1 + count_0) / count_total, spread_quality


# parse_pred_file('predictions/mate-2-10-0.7.csv')

thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
max_distances = [5, 10, 40]
orders = [1, 2]

""" 02-11 """
# res_1_05 = [0.552, 0.612, 0.678, 0.75, 0.778, 0.778, 0.778, 0.778, 0.778]
# res_1_10 = [0.552, 0.612, 0.678, 0.726, 0.792, 0.702, 0.65, 0.65, 0.65]
# res_1_40 = [0.552, 0.612, 0.678, 0.726, 0.792, 0.834, 0.872, 0.922, 0.966]
#
# res_2_05 = [0.602, 0.646, 0.688, 0.712, 0.760, 0.784, 0.784, 0.784, 0.784]
# res_2_10 = [0.602, 0.642, 0.686, 0.732, 0.740, 0.676, 0.652, 0.656, 0.656]
# res_2_40 = [0.602, 0.642, 0.686, 0.732, 0.786, 0.840, 0.884, 0.916, 0.964]
#
# results = dict()
# """ Order 1 """
# results[5] = res_1_05
# results[10] = res_1_10
# results[40] = res_1_40
# non_trivial_percentages = []
# for i, d in enumerate(max_distances):
#     non_trivial_percentages.append([])
#     for t in thresholds:
#         trivial, spread_quality = parse_pred_file('../analysis_data/predictions-02-11-2055/mate-1-' + str(d) + '-' + str(t) + '.csv', d)
#         non_trivial_percentages[i].append(1 - trivial)
#
# plt.plot(thresholds, results[5], "-b", label='precision for max_dist = 5')
# plt.plot(thresholds, non_trivial_percentages[0], '--b', label='non_trivial_perc for max_dist = 5')
# plt.plot(thresholds, results[5], ".b")
# plt.plot(thresholds, non_trivial_percentages[0], ".b")
#
# plt.plot(thresholds, results[10], "-g", label='precision for max_dist = 10')
# plt.plot(thresholds, non_trivial_percentages[1], '--g', label='non_trivial_perc for max_dist = 10')
# plt.plot(thresholds, results[10], "xg")
# plt.plot(thresholds, non_trivial_percentages[1], "xg")
#
# plt.plot(thresholds, results[40], "-r", label='precision for max_dist = 40')
# plt.plot(thresholds, non_trivial_percentages[2], '--r', label='non_trivial_perc for max_dist = 40')
# plt.plot(thresholds, results[40], ".r")
# plt.plot(thresholds, non_trivial_percentages[2], ".r")
#
# plt.legend()
# plt.title("Order 1 - old")
# plt.show()
#
# """ Order 2 """
# results[5] = res_2_05
# results[10] = res_2_10
# results[40] = res_2_40
# non_trivial_percentages = []
# for i, d in enumerate(max_distances):
#     non_trivial_percentages.append([])
#     for t in thresholds:
#         trivial, max_spread = parse_pred_file('../analysis_data/predictions-02-11-2055/mate-2-' + str(d) + '-' + str(t) + '.csv', d)
#         non_trivial_percentages[i].append(1 - trivial)
#
# plt.plot(thresholds, results[5], "-b", label='precision for max_dist = 5')
# plt.plot(thresholds, non_trivial_percentages[0], '--b', label='non_trivial_perc for max_dist = 5')
# plt.plot(thresholds, results[5], ".b")
# plt.plot(thresholds, non_trivial_percentages[0], ".b")
#
# plt.plot(thresholds, results[10], "-g", label='precision for max_dist = 10')
# plt.plot(thresholds, non_trivial_percentages[1], '--g', label='non_trivial_perc for max_dist = 10')
# plt.plot(thresholds, results[10], "xg")
# plt.plot(thresholds, non_trivial_percentages[1], "xg")
#
# plt.plot(thresholds, results[40], "-r", label='precision for max_dist = 40')
# plt.plot(thresholds, non_trivial_percentages[2], '--r', label='non_trivial_perc for max_dist = 40')
# plt.plot(thresholds, results[40], ".r")
# plt.plot(thresholds, non_trivial_percentages[2], ".r")
#
# plt.legend()
# plt.title("Order 2 - old")
# plt.show()

""" Order 1 Graph """
# plt.plot(thresholds, res_1_05, label='max_dist: 05')
# plt.plot(thresholds, res_1_10, label='max_dist: 10')
# plt.plot(thresholds, res_1_40, label='max_dist: 40')
# plt.plot(thresholds, res_1_05, ".b",
#          thresholds, res_1_10, ".b",
#          thresholds, res_1_40, ".b")
# axes = plt.gca()
# axes.set_ylim([0.5, 1.0])
# plt.xlabel('Threshold')
# plt.ylabel('Precision')
# plt.legend()
# plt.show()
#
# plt.plot(thresholds, res_2_05, label='max_dist: 05')
# plt.plot(thresholds, res_2_10, label='max_dist: 10')
# plt.plot(thresholds, res_2_40, label='max_dist: 40')
# plt.plot(thresholds, res_2_05, ".b",
#          thresholds, res_2_10, ".b",
#          thresholds, res_2_40, ".b")
# axes = plt.gca()
# axes.set_ylim([0.5, 1.0])
# plt.xlabel('Threshold')
# plt.ylabel('Precision')
# plt.legend()
# plt.show()

""" Real Graphics """
# for order in orders:
#     non_trivial_percentages = []
#     max_spreads = []
#     for i, d in enumerate(max_distances):
#         non_trivial_percentages.append([])
#         max_spreads.append([])
#         for t in thresholds:
#             trivial, max_spread = parse_pred_file('predictions/mate-' + str(order) + '-' + str(d) + '-' + str(t) + '.csv')
#             non_trivial_percentages[i].append(1 - trivial)
#             max_spreads[i].append(max_spread)
#
#     for i, d in enumerate(max_distances):
#         plt.plot(thresholds, max_spreads[i], label='max_spread ' + str(d))
#         plt.plot(thresholds, non_trivial_percentages[i], '--', label='non_trivial_perc ' + str(d))
#         plt.plot(thresholds, max_spreads[i], ".b",
#                  thresholds, non_trivial_percentages[i], ".b")
#     plt.legend()
#     plt.show()



""" Graphs for Presentation """
res_1_05 = [0.73, 0.748, 0.748, 0.748, 0.872, 0.872, 0.898, 0.92, 0.634]
res_1_10 = [0.73, 0.748, 0.748, 0.748, 0.872, 0.872, 0.898, 0.92, 0.958]
res_1_40 = [0.73, 0.748, 0.748, 0.748, 0.872, 0.872, 0.898, 0.92, 0.958]

res_2_05 = [0.744, 0.744, 0.768, 0.862, 0.884, 0.896, 0.874, 0.888, 0.786]
res_2_10 = [0.744, 0.744, 0.768, 0.862, 0.884, 0.896, 0.916, 0.936, 0.962]
res_2_40 = [0.744, 0.744, 0.768, 0.862, 0.884, 0.896, 0.916, 0.936, 0.962]

results = dict()
""" Order 1 """
results[5] = res_1_05
results[10] = res_1_10
results[40] = res_1_40
non_trivial_percentages = []
for i, d in enumerate(max_distances):
    non_trivial_percentages.append([])
    for t in thresholds:
        trivial, max_spread = parse_pred_file('predictions/mate-1-' + str(d) + '-' + str(t) + '.csv', d)
        non_trivial_percentages[i].append(1 - trivial)

plt.plot(thresholds, results[5], "-", color="#F6A800", label='precision for max_dist = 5')
plt.plot(thresholds, non_trivial_percentages[0], '--', color="#F6A800", label='non_trivial_perc for max_dist = 5')
plt.plot(thresholds, results[5], ".", color="#F6A800")
plt.plot(thresholds, non_trivial_percentages[0], ".", color="#F6A800")

plt.plot(thresholds, results[10], "-", color="#DD640C", label='precision for max_dist = 10')
plt.plot(thresholds, non_trivial_percentages[1], '--', color="#DD640C", label='non_trivial_perc for max_dist = 10')
plt.plot(thresholds, results[10], "x", color="#DD640C")
plt.plot(thresholds, non_trivial_percentages[1], "x", color="#DD640C")

plt.plot(thresholds, results[40], "-", color="#B1063A", label='precision for max_dist = 40')
plt.plot(thresholds, non_trivial_percentages[2], '--', color="#B1063A", label='non_trivial_perc for max_dist = 40')
plt.plot(thresholds, results[40], ".", color="#B1063A")
plt.plot(thresholds, non_trivial_percentages[2], ".", color="#B1063A")

axes = plt.gca()
axes.set_ylim([0.0, 1.0])
plt.legend()
plt.xlabel('Threshold')
plt.ylabel('Ratio')
plt.title("Order 1")
plt.savefig("results/order1.png")
plt.show()


""" Order 2 """
results[5] = res_2_05
results[10] = res_2_10
results[40] = res_2_40
non_trivial_percentages = []
for i, d in enumerate(max_distances):
    non_trivial_percentages.append([])
    for t in thresholds:
        trivial, max_spread = parse_pred_file('predictions/mate-2-' + str(d) + '-' + str(t) + '.csv', d)
        non_trivial_percentages[i].append(1 - trivial)

plt.plot(thresholds, results[5], "-", color="#F6A800", label='precision for max_dist = 5')
plt.plot(thresholds, non_trivial_percentages[0], '--', color="#F6A800", label='non_trivial_perc for max_dist = 5')
plt.plot(thresholds, results[5], ".", color="#F6A800")
plt.plot(thresholds, non_trivial_percentages[0], ".", color="#F6A800")

plt.plot(thresholds, results[10], "-", color="#DD640C", label='precision for max_dist = 10')
plt.plot(thresholds, non_trivial_percentages[1], '--', color="#DD640C", label='non_trivial_perc for max_dist = 10')
plt.plot(thresholds, results[10], "x", color="#DD640C")
plt.plot(thresholds, non_trivial_percentages[1], "x", color="#DD640C")

plt.plot(thresholds, results[40], "-", color="#B1063A", label='precision for max_dist = 40')
plt.plot(thresholds, non_trivial_percentages[2], '--', color="#B1063A", label='non_trivial_perc for max_dist = 40')
plt.plot(thresholds, results[40], ".", color="#B1063A")
plt.plot(thresholds, non_trivial_percentages[2], ".", color="#B1063A")

axes = plt.gca()
axes.set_ylim([0.0, 1.0])
plt.legend()
plt.xlabel('Threshold')
plt.ylabel('Ratio')
plt.title("Order 2")
plt.savefig("results/order2.png")
plt.show()

