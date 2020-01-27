class DFA:
    def __init__(self, states, start_state, alphabet, final_states, state_transition_matrix):
        self.states = states
        self.start_state = start_state
        self.alphabet = alphabet
        self.final_states = final_states
        self.state_transition_matrix = state_transition_matrix

    def __str__(self):
        return f"States: {str(self.states)} \n Start State: {str(self.start_state)} \n Final States: {str(self.final_states)} \n Alphabet: {str(self.alphabet)} \n Matrix: {str(self.state_transition_matrix)}"

    def get_predecessor_states(self, state):
        return self.state_transition_matrix.get_predecessor_states(state)

    def get_prepaths(self, depth, current_state):
        return self.state_transition_matrix.get_prepaths(depth, current_state)

    def insert_state(self, state):
        return self.state_transition_matrix.insert_state(state)

    def delta(self, state, letter):
        return self.state_transition_matrix.delta(state, letter)

    def copy_delta(self, source, target):
        return self.state_transition_matrix.copy_delta(source, target)

    def set_transition(self, source, target, letter):
        self.state_transition_matrix.set_transition(source, target, letter)

    def increase_unambiguity(self, order):
        initial_states = list(self.states)
        #print(self.state_transition_matrix.matrix)
        #print(initial_states)
        for q in initial_states:
            print("Processing state: " + str(q))
            #print('initial_states loop:')
            #print('q: ' + q)
            pre_paths = self.get_prepaths(order, q) #still buggy
            #print('pre_paths:')
            #print(pre_paths)
            while len(pre_paths) > 1:
                #print("pre_path length: " + str(len(pre_paths)))
                a = pre_paths[0]
                qa = q + str(pre_paths[0])
                #print('choosen word: ' + a)
                #print('new state: ' + qa)

                # add qa to matrix
                #self.states.append(qa)
                #print('new states: ' + str(self.states
                #print('old matrix:')
                #print(self.state_transition_matrix.matrix)
                self.insert_state(qa)

                #print('new states: ' + str(self.states))
                #print('new matrix:')
                #print(self.state_transition_matrix.matrix)

                if q in self.final_states:
                    self.final_states.append(qa)

                #pre_paths_qa = a
                #predecessor_states_qa = []

                self.copy_delta(q, qa)
                #print('matrix after copy delta:')
                #print(self.state_transition_matrix.matrix)

                #print('get_predecessor_states(q): ' + str(self.get_predecessor_states(q)))
                for p in self.get_predecessor_states(q):
                    #print('p: ' + p)
                    #print('a[-1]: ' + a[-1])
                    #print(self.delta(p, a[-1]))
                    if (self.delta(p, a[-1]) == q) and (a[:-1] in self.get_prepaths(order-1, p)):
                        self.state_transition_matrix.remove_transition(p, q, a[-1])
                        self.state_transition_matrix.add_transition(p, qa, a[-1])
                #print('matrix after adjusting transitions:')
                #print(self.state_transition_matrix.matrix)
                #for p in self.get_predecessor_states(q):
                #    if all(q != delta(p, x, matrix) for x in alphabet):
                #        predecessor_dict[q].remove(q)
                pre_paths.remove(a)
