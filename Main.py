from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA
from UseCaseAnalyser_Class import BPIUseCaseAnalyser, ABCUseCaseAnalyser, BPI19UseCaseAnalyser
from Tester_Class import Tester


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
    abc_analyser = ABCUseCaseAnalyser()
    dfa = abc_analyser.get_dfa()
    print("Starting unambiguity 1")
    dfa.increase_unambiguity(1)  # should not change anything
    print(dfa.state_transition_matrix.matrix)

    threshold = 0.9
    max_distance = 10
    print("Starting training")
    abc_analyser.train_matrix(dfa, 'data/abc.csv', 999)
    Tester.test_correct_trained_matrix_abc(abc_analyser.trained_matrix)
    print("Starting prediction")
    abc_analyser.predict_matrix(dfa, 'data/abc.csv', 0, 100, 'results/abc.csv', max_distance, threshold)
    Tester.test_correct_prediction_abc(abc_analyser)
    p = abc_analyser.get_precision('data/abc.csv', 'results/abc.csv', 0, 100, max_distance)
    print(p)

    """ BPI19 use case """
    # bpi19_analyser = BPI19UseCaseAnalyser()
    # dfa_bpi19 = bpi19_analyser.get_dfa()
    #
    # dfa_bpi19.increase_unambiguity(1)
    # # dfa_bpi19.increase_unambiguity(2)  # TODO takes ages!
    # print("Starting training")
    # bpi19_analyser.train_matrix(dfa_bpi19, 'data/bpi19.csv', 1000)
    # Tester.test_correct_trained_matrix_bpi19(bpi19_analyser.trained_matrix)
    # threshold = 0.8
    # max_distance = 4
    # print("Starting prediction")
    # bpi19_analyser.predict_matrix(dfa_bpi19, 'data/bpi19.csv', 1, 200, 'results/bpi19.csv', max_distance, threshold)
    # precision = bpi19_analyser.get_precision('data/bpi19.csv', 'results/bpi19.csv', 1, 199, max_distance)
    # print(precision)


Tester.test_precision()
main()
