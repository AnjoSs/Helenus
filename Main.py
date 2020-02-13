import csv

from UseCaseAnalyser_Class import BigMateUseCaseAnalyser
import logging
import datetime


def main():
    logging.basicConfig(filename="logs/general.log", level=logging.INFO)

    """ Mate use case """
    logging.info(str(datetime.datetime.now()) + " # Starting Mate Use Case with LTL: G(m --> Fs)")
    logging.info(str(datetime.datetime.now()) + " ## Starting creating use case dfa")
    mate_analyser = BigMateUseCaseAnalyser()
    dfa_mate = mate_analyser.get_dfa()
    logging.info(str(datetime.datetime.now()) + " ## Finished creating use case dfa")
    with open('logs/mate.csv', 'w') as dfa_file:
        csv.writer(dfa_file).writerow([str(dfa_mate)])


    # TODO change to [1, 2, 3]
    orders_to_test = [1, 2, 3]
    training_log_size = 1000
    prediction_size = 500
    for order in orders_to_test:
        print("Processing order " + str(order))
        logging.info(str(datetime.datetime.now()) + " ## Starting increasing unambiguity: " + str(order))
        dfa_mate.increase_unambiguity(order)
        logging.info(str(datetime.datetime.now()) + " ## Finished increasing unambiguity: " + str(order))
        tested_thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        max_distances = [5, 10, 40]  # TODO change to something way bigger (5 for 3 event types --> for 40 event types: 40-67!
        logging.info(str(datetime.datetime.now()) + " ## Starting tests with order " + str(order))
        for distance in max_distances:
            logging.info(str(datetime.datetime.now()) + " ## Starting training matrix")
            # TODO auslagern
            mate_analyser.train_matrix(dfa_mate, 'data/mate.csv', training_log_size, distance, False)
            logging.info(str(datetime.datetime.now()) + " ## Finished training matrix")
            with open('logs/trainedMatrixMate-' + str(order) + '-' + str(distance) + '.csv', 'w') as matrix_file:
                csv.writer(matrix_file).writerow(str(mate_analyser.trained_matrix))
            data_path = 'data/mate.csv'
            print("Processing distance: " + str(distance))
            logging.info(str(datetime.datetime.now()) + " ### Starting tests for max_distance: " + str(distance))
            for threshold in tested_thresholds:
                print("Processing threshold: " + str(threshold))
                prediction_path = 'predictions/mate-' + str(order) + '-' + str(distance) + '-' + str(threshold) + '.csv'
                logging.info(str(datetime.datetime.now()) + " #### Starting prediction for threshold " + str(threshold))
                mate_analyser.predict_matrix(dfa_mate, data_path, training_log_size + 1, training_log_size + 1 + prediction_size, prediction_path, distance, threshold)
                logging.info(str(datetime.datetime.now()) + " #### Finished prediction for threshold " + str(threshold))
                logging.info(str(datetime.datetime.now()) + " #### Starting precision calculation for threshold " + str(threshold))
                precision = mate_analyser.get_precision(data_path, prediction_path, training_log_size + 1, 0, prediction_size, distance)
                logging.info(str(datetime.datetime.now()) + " #### Finished precision calculation for threshold " + str(threshold) + " - precision: " + str(precision))


# Tester.test_precision()
main()
