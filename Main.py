from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA
from Analyser_Class import BPIAnalyser
from Tester_Class import Tester


def main():
    # hardcoded input values for order 1 LTL: Fb
    states = ['A', 'B', 'B2']
    start_state = ['B']
    alphabet = ['a', 'b']
    final_states = ['A', 'B2']
    state_transition_matrix = [[['a'], [], ['b']], [['a'], ['b'], []], [['a'], [], ['b']]]

    # create DFA Object with a State Transition Matrix Object
    matrix1 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    dfa1 = DFA(states, start_state, alphabet, final_states, matrix1)

    dfa1.increase_unambiguity(2)
    Tester.test_correct_unambiguity_2(dfa1)
    #print('#########################################')
    #dfa1.increase_unambiguity(3)

    states = ['A', 'B']
    start_state = ['B']
    alphabet = ['a', 'b']
    final_states = ['B']
    state_transition_matrix = [[['a'], ['b']], [['a'], ['b']]]
    order = 2

    matrix2 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    dfa2 = DFA(states, start_state, alphabet, final_states, matrix2)

################################################################################

    analyser = BPIAnalyser()
    dfa = analyser.get_dfa()
    print("Starting unambiguity 1")
    dfa.increase_unambiguity(1)
    print("Starting unambiguity 2")
    dfa.increase_unambiguity(2)

    analyser.train_matrix(dfa, 'data/hospital_log.csv', 75000)

    print(analyser.trained_matrix)


main()