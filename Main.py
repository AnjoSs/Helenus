import csv

from Tester_Class import Tester
from UseCaseAnalyser_Class import BPI19UseCaseAnalyser, BPI19FinallyAnalyser
import logging
import datetime
import cProfile


def main():
    logging.basicConfig(filename="logs/general.log", level=logging.INFO)

    """ BPI19 use case """
    logging.info(str(datetime.datetime.now()) + " # Starting BPI19 Use Case with LTL: Fa")
    logging.info(str(datetime.datetime.now()) + " ## Starting creating use case dfa")
    bpi19_analyser = BPI19FinallyAnalyser()
    dfa_bpi19 = bpi19_analyser.get_dfa()
    logging.info(str(datetime.datetime.now()) + " ## Finished creating use case dfa")
    with open('logs/dfaBPI19.csv', 'w') as dfa_file:
        csv.writer(dfa_file).writerow([str(dfa_bpi19)])


    # TODO change to [1, 2, 3]
    orders_to_test = [1, 2, 3]
    training_log_size = 1000000
    # prediction_size = 500
    for order in orders_to_test:
        print("Processing order " + str(order))
        logging.info(str(datetime.datetime.now()) + " ## Starting increasing unambiguity: " + str(order))
        if order == 1:
            dfa_bpi19.increase_unambiguity_to_1()
        else:
            dfa_bpi19.increase_unambiguity(order)
        logging.info(str(datetime.datetime.now()) + " ## Finished increasing unambiguity: " + str(order))
        tested_thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        max_distances = [2, 3, 5, 10]
        logging.info(str(datetime.datetime.now()) + " ## Starting tests with order " + str(order))

        for distance in max_distances:
            logging.info(str(datetime.datetime.now()) + " ## Starting training matrix")
            bpi19_analyser.train_matrix(dfa_bpi19, 'data/bpi19_cleaned.csv', training_log_size, distance, True, True)
            logging.info(str(datetime.datetime.now()) + " ## Finished training matrix")

            with open('logs/trainedMatrixBPI19-' + str(order) + '-' + str(distance) + '.csv', 'w') as matrix_file:
                csv.writer(matrix_file).writerow(str(bpi19_analyser.trained_matrix))
            print("Processing distance: " + str(distance))
            logging.info(str(datetime.datetime.now()) + " ### Starting tests for max_distance: " + str(distance))
            prec_file = open("logs/precision_" + str(order) + "_" + str(distance) + ".csv", "w+", newline='')
            dur_file = open("logs/duration_" + str(order) + "_" + str(distance) + ".csv", "w+", newline='')
            for threshold in tested_thresholds:
                print("Processing threshold: " + str(threshold))
                precisions = []
                durations = []
                for i in range(0, 100):
                    data_path = 'data/instances/' + str(i) + '.csv'
                    prediction_path = 'predictions/bpi19-' + str(order) + '-' + str(distance) + '-' + str(threshold) + '_' + str(i) + '.csv'
                    # logging.info(str(datetime.datetime.now()) + " #### Starting prediction for threshold " + str(threshold))
                    start = datetime.datetime.now()
                    bpi19_analyser.predict_matrix(dfa_bpi19, data_path, 0, None, prediction_path, distance, threshold)
                    duration = datetime.datetime.now() - start
                    durations.append(duration)
                    # logging.info(str(datetime.datetime.now()) + " #### Finished prediction for threshold " + str(threshold))
                    # logging.info(str(datetime.datetime.now()) + " #### Starting precision calculation for threshold " + str(threshold))
                    precision = bpi19_analyser.get_precision(data_path, prediction_path, 0, 0, None, distance)
                    precisions.append(precision)
                p = sum(precisions) / len(precisions)
                dur_sum = 0
                for d in durations:
                    dur_sum += d.total_seconds()
                duration = dur_sum / len(durations)
                logging.info(str(datetime.datetime.now()) + " #### Finished precision calculation for threshold " + str(threshold) + " - precision: " + str(p))
                csv.writer(prec_file).writerow([str(p)])
                csv.writer(dur_file).writerow([str(duration)])


# Tester.test_precision()
cProfile.run("main()")
# main()
