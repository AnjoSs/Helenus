from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA
from UseCaseAnalyser_Class import BPIUseCaseAnalyser, ABCUseCaseAnalyser, BPI19UseCaseAnalyser, MateUseCaseAnalyser
from Tester_Class import Tester
import datetime


def main():
    """ Old hardcoded test cases """
    # hardcoded input values for order 1 LTL: Fb
    # states = ['A', 'B', 'B2']
    # start_state = ['B']
    # alphabet = ['a', 'b']
    # final_states = ['A', 'B2']
    # state_transition_matrix = [[['a'], [], ['b']], [['a'], ['b'], []], [['a'], [], ['b']]]
    #
    # # create DFA Object with a State Transition Matrix Object
    # matrix1 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    # dfa1 = DFA(states, start_state, alphabet, final_states, matrix1)
    #
    # dfa1.increase_unambiguity(2)
    # Tester.test_correct_unambiguity_2(dfa1)
    # #print('#########################################')
    # #dfa1.increase_unambiguity(3)
    #
    # states = ['A', 'B']
    # start_state = ['B']
    # alphabet = ['a', 'b']
    # final_states = ['B']
    # state_transition_matrix = [[['a'], ['b']], [['a'], ['b']]]
    # order = 2
    #
    # matrix2 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    # dfa2 = DFA(states, start_state, alphabet, final_states, matrix2)

################################################################################

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
    # mate_analyser.train_matrix(dfa, 'data/abc_fixed.csv', 999, max_distance)
    # print("Starting prediction")
    # start = datetime.datetime.now()
    # mate_analyser.predict_matrix(dfa, 'data/abc_fixed.csv', 0, 100, 'results/abc.csv', max_distance, threshold)
    # duration = datetime.datetime.now() - start
    # print("Prediction Order 3: " + str(duration))
    # p = mate_analyser.get_precision('data/abc_fixed.csv', 'results/abc.csv', 0, 0, 100, max_distance)
    # print(p)

    """ BPI19 use case """
    bpi19_analyser = BPI19UseCaseAnalyser()
    dfa_bpi19 = bpi19_analyser.get_dfa()

    threshold = 0.8
    max_distance = 4
    dfa_bpi19.increase_unambiguity(1)
    # dfa_bpi19.increase_unambiguity(2)  # TODO takes ages!
    print("Starting training")
    bpi19_analyser.train_matrix(dfa_bpi19, 'data/bpi19.csv', 1000, max_distance)
    Tester.test_correct_trained_matrix_bpi19(bpi19_analyser.trained_matrix)
    print("Starting prediction")
    bpi19_analyser.predict_matrix(dfa_bpi19, 'data/bpi19.csv', 1, 200, 'results/bpi19.csv', max_distance, threshold)
    precision = bpi19_analyser.get_precision('data/bpi19.csv', 'results/bpi19.csv', 1, 0, 199, max_distance)
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


# Tester.test_precision()
main()
