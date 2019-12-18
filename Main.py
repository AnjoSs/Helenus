from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA
from operator import itemgetter
from BPI_Analyser_Class import BPIAnalyser


def main():
    # hardcoded input values
    states = ['A', 'B', 'B2']
    start_state = ['B']
    alphabet = ['a', 'b']
    final_states = ['A', 'B2']
    state_transition_matrix = [[['a'], [], ['b']], [['a'], ['b'], []], [['a'], [], ['b']]]
    order = 2


    # create DFA Object with a State Transition Matrix Object
    matrix1 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    dfa1 = DFA(states, start_state, alphabet, final_states, matrix1)

    #dfa1.increase_unambiguity(2)
    #assert sorted(dfa1.states) == sorted(['A', 'B', 'B2', 'Aba', 'B2ab'])
    #assert sorted(dfa1.state_transition_matrix.matrix) == sorted([[['a'], [], [], [], ['b']], [[], ['b'], [], ['a'], []], [[], [], ['b'], ['a'], []], [['a'], [], [], [], ['b']], [[], [], ['b'], ['a'], []]])

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
    # a = "cea - tumormarker mbv meia"
    # b = "squamous cell carcinoma mbv eia"
    #
    # states = ["A", "B"]
    # start_state = ["B"]
    # final_states = ["B"]
    #
    # analyser = BPIAnalyser()
    # alphabet = analyser.get_alphabet()
    # state_transition_matrix = analyser.get_matrix_GaFb(a, b)
    #
    # matrix = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    # dfa = DFA(states, start_state, alphabet, final_states, matrix)
    # print("Starting unambiguity 1")
    # dfa.increase_unambiguity(1)
    # print("Starting unambiguity 2")
    # dfa.increase_unambiguity(2)
    #
    # analyser.train_matrix(dfa)
    #
    # print(analyser.trained_matrix)


main()
