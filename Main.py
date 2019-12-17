from DFA2Markov import increase_unambiguity
from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA

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

    states = ['A', 'B']
    start_state = ['B']
    alphabet = ['a', 'b']
    final_states = ['B']
    state_transition_matrix = [[['a'], ['b']], [['a'], ['b']]]
    order = 2

    matrix2 = State_Transition_Matrix(states, alphabet, state_transition_matrix)
    dfa2 = DFA(states, start_state, alphabet, final_states, matrix2)

    ## make DFA iteratively unambiguous
    #for i in range(1, order):
    dfa1.increase_unambiguity(2)
    print('#########################################')
    dfa1.increase_unambiguity(3)

    # train unambiguous dfa's matrix



main()
