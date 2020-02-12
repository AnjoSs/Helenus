from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA
from UseCaseAnalyser_Class import BPIUseCaseAnalyser, ABCUseCaseAnalyser, BPI19UseCaseAnalyser, MateUseCaseAnalyser, \
    AutoUseCaseAnalyser
from Tester_Class import Tester
import datetime


def main():
    """ BPI11 use case"""
    # TODO something is wrong with this use case. if unambiguity is 2, the percentage per row is not 1.
    # probably due to not taking all event types and thus missing state transitions
    # data_path = 'data/hospital_log.csv'
    # pred_path = 'results/bpi11.csv'
    # analyser = BPIUseCaseAnalyser()
    # dfa = analyser.get_dfa()
    # print("Starting unambiguity 1")
    # dfa.increase_unambiguity(1)
    # Tester.test_correct_dfa_bpi11(dfa)
    # # print("Starting unambiguity 2")
    # # dfa.increase_unambiguity(2)
    # # Tester.test_correct_dfa_bpi11(dfa)
    #
    # analyser.train_matrix(dfa, data_path, 75000)
    # Tester.test_correct_trained_matrix_bpi11(analyser.trained_matrix)
    # threshold = 0.5
    # max_distance = 4
    # analyser.predict_matrix(dfa, data_path, 1, 10000, pred_path, max_distance, threshold)
    # p = analyser.get_precision(data_path, pred_path, 1, 200, max_distance)
    # print(p)

    """ ABC use case for testing """
    # threshold = 0.9
    # max_distance = 50
    # mate_analyser = ABCUseCaseAnalyser()
    # dfa = mate_analyser.get_dfa()
    # print("Starting unambiguity 1")
    # dfa.increase_unambiguity(1)
    # Tester.test_unambiguous(dfa)
    # mate_analyser.train_matrix(dfa, 'data/abc_fixed.csv', 999, max_distance)
    # Tester.test_correct_trained_matrix_abc(mate_analyser.trained_matrix)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/abc_fixed.csv', 0, 100, 'results/abc.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 1: " + str(duration))
    # Tester.test_correct_prediction_abc(mate_analyser)
    # p = mate_analyser.get_precision('data/abc_fixed.csv', 'results/abc.csv', 0, 0, 100, max_distance)
    # print(p)
    #
    # dfa.increase_unambiguity(2)
    # Tester.test_unambiguous(dfa)
    # mate_analyser.train_matrix(dfa, 'data/abc_fixed.csv', 999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/abc_fixed.csv', 0, 100, 'results/abc.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 2: " + str(duration))
    # p = mate_analyser.get_precision('data/abc_fixed.csv', 'results/abc.csv', 0, 0, 100, max_distance)
    # print(p)
    #
    # dfa.increase_unambiguity(3)
    # Tester.test_unambiguous(dfa)
    # mate_analyser.train_matrix(dfa, 'data/abc_fixed.csv', 999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/abc_fixed.csv', 0, 100, 'results/abc.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 3: " + str(duration))
    # p = mate_analyser.get_precision('data/abc_fixed.csv', 'results/abc.csv', 0, 0, 100, max_distance)
    # print(p)

    """ BPI19 use case """
    auto_analyser = BPI19UseCaseAnalyser()
    dfa_auto = auto_analyser.get_dfa()

    threshold = 0.8
    max_distance = 4
    dfa_auto.increase_unambiguity(1)
    Tester.test_unambiguous(dfa_auto)
    # dfa_bpi19.increase_unambiguity(2)  # TODO takes ages!
    print("Starting training")
    auto_analyser.train_matrix(dfa_auto, 'data/bpi19.csv', 1000, max_distance, True)
    Tester.test_correct_trained_matrix_bpi19(auto_analyser.trained_matrix)
    print("Starting prediction")
    auto_analyser.predict_matrix(dfa_auto, 'data/bpi19.csv', 1, 200, 'results/bpi19.csv', max_distance, threshold)
    precision = auto_analyser.get_precision('data/bpi19.csv', 'results/bpi19.csv', 1, 0, 199, max_distance)
    print(precision)

    """ Mate use case """
    # threshold = 0.8
    # max_distance = 10
    # mate_analyser = MateUseCaseAnalyser()
    # dfa = mate_analyser.get_dfa()
    # print("Starting unambiguity 1")
    # dfa.increase_unambiguity(1)
    # print(dfa.state_transition_matrix.matrix)
    # mate_analyser.train_matrix(dfa, 'data/mate.csv', 99999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/mate.csv', 0, 1000, 'results/mate.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 1: " + str(duration))
    # p = mate_analyser.get_precision('data/mate.csv', 'results/mate.csv', 0, 0, 1000, max_distance)
    # print(p)
    #
    # print("Starting unambiguity 2")
    # dfa.increase_unambiguity(2)
    # print(dfa.state_transition_matrix.matrix)
    # mate_analyser.train_matrix(dfa, 'data/mate.csv', 999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/mate.csv', 0, 100, 'results/mate2.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 2: " + str(duration))
    # p = mate_analyser.get_precision('data/mate.csv', 'results/mate2.csv', 0, 0, 100, max_distance)
    # print(p)
    #
    # print("Starting unambiguity 3")
    # dfa.increase_unambiguity(3)
    # print(dfa.state_transition_matrix.matrix)
    # mate_analyser.train_matrix(dfa, 'data/mate.csv', 999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/mate.csv', 0, 100, 'results/mate2.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 2: " + str(duration))
    # p = mate_analyser.get_precision('data/mate.csv', 'results/mate2.csv', 0, 0, 100, max_distance)
    # print(p)

    """ Auto Use Case """
    # auto_analyser = AutoUseCaseAnalyser()
    # dfa_auto = auto_analyser.get_dfa()
    #
    # threshold = 0.7
    # max_distance = 10
    # dfa_auto.increase_unambiguity(1)
    # Tester.test_unambiguous(dfa_auto)
    # print("Starting training")
    # auto_analyser.train_matrix(dfa_auto, 'data/auto.csv', 1000, max_distance, True)
    # Tester.test_correct_trained_matrix_bpi19(auto_analyser.trained_matrix)
    # print("Starting prediction")
    # auto_analyser.predict_matrix(dfa_auto, 'data/auto_one_instance.csv', 0, 8, 'results/auto.csv', max_distance, threshold)
    # precision = auto_analyser.get_precision('data/auto_one_instance.csv', 'results/auto.csv', 0, 0, 7, max_distance)
    # print(precision)


# Tester.test_precision()
main()
