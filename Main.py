from DFA2Markov import increase_unambiguity
from State_Transition_Matrix_Class import State_Transition_Matrix
from DFA_Class import DFA

def main():
    #states = Input_DFA.states
    #final_states = Input_DFA.final_states
    #alphabet = Input_DFA.alphabet
    #matrix = Input_DFA.initial_matrix
    #desired_order = 2 #hard coded order that we want to train our markov chain on
    #for order in range(1, desired_order+1):
    #    increase_unambiguity(states, final_states, alphabet, order, matrix)
    #    print(matrix)

    # hardcoded input values
    states = ['A', 'B', 'B2']
    start_state = ['B']
    alphabet = ['a', 'b']
    final_states = ['A', 'B2']
    state_transition_matrix = [['a', '','b'], ['a', 'b', ''], ['a', '','b']]
    order = 2


    # create DFA Object with a State Transition Matrix Object
    matrix = State_Transition_Matrix(states, state_transition_matrix)
    dfa = DFA(states, start_state, alphabet, final_states, matrix)

    ## make DFA iteratively unambiguous
    #for i in range(1, order):
    dfa.increase_unambiguity(2)

    # train unambiguous dfa's matrix



main()
