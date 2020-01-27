import csv

from Tester_Class import Tester
from UseCaseAnalyser_Class import BPI19UseCaseAnalyser
import logging
import datetime


def main():
    logging.basicConfig(filename="logs/general.log", level=logging.INFO)

    """ BPI19 use case """
    logging.info(str(datetime.datetime.now()) + " # Starting BPI19 Use Case with LTL: Fa")
    logging.info(str(datetime.datetime.now()) + " ## Starting creating use case dfa")
    bpi19_analyser = BPI19UseCaseAnalyser()
    dfa_bpi19 = bpi19_analyser.get_dfa()
    logging.info(str(datetime.datetime.now()) + " ## Finished creating use case dfa")
    with open('logs/dfaBPI19.csv', 'w') as dfa_file:
        csv.writer(dfa_file).writerow([str(dfa_bpi19)])


    # TODO change to [1, 2, 3]
    orders_to_test = [1]
    training_log_size = 1000
    prediction_size = 500
    for order in orders_to_test:
        logging.info(str(datetime.datetime.now()) + " ## Starting increasing unambiguity: " + str(order))
        dfa_bpi19.increase_unambiguity(order)
        logging.info(str(datetime.datetime.now()) + " ## Finished increasing unambiguity: " + str(order))
        logging.info(str(datetime.datetime.now()) + " ## Starting training matrix")
        bpi19_analyser.train_matrix(dfa_bpi19, 'data/bpi19.csv', training_log_size)
        logging.info(str(datetime.datetime.now()) + " ## Finished training matrix")
        with open('logs/trainedMatrixBPI19.csv', 'w') as matrix_file:
            csv.writer(matrix_file).writerow(str(bpi19_analyser.trained_matrix))
        data_path = 'data/bpi19.csv'
        tested_thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        max_distances = [10]  # TODO change to something way bigger (5 for 3 event types --> for 40 event types: 40-67!
        logging.info(str(datetime.datetime.now()) + " ## Starting tests with order " + str(order))
        for distance in max_distances:
            logging.info(str(datetime.datetime.now()) + " ### Starting tests for max_distance: " + str(distance))
            for threshold in tested_thresholds:
                prediction_path = 'predictions/bpi19-' + str(order) + '-' + str(distance) + '-' + str(threshold) + '.csv'
                logging.info(str(datetime.datetime.now()) + " #### Starting prediction for threshold " + str(threshold))
                bpi19_analyser.predict_matrix(dfa_bpi19, data_path, training_log_size, training_log_size + prediction_size + 1, prediction_path, distance, threshold)
                logging.info(str(datetime.datetime.now()) + " #### Finished prediction for threshold " + str(threshold))
                logging.info(str(datetime.datetime.now()) + " #### Starting precision calculation for threshold " + str(threshold))
                precision = bpi19_analyser.get_precision(data_path, prediction_path, training_log_size + 1, 0, prediction_size, distance)
                logging.info(str(datetime.datetime.now()) + " #### Finished precision calculation for threshold " + str(threshold) + " - precision: " + str(precision))


# Tester.test_precision()
main()
