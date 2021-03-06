import numpy as np

class DFA:
    def __init__(self, states, start_state, alphabet, final_states, state_transition_matrix):
        self.states = states
        self.start_state = start_state
        self.alphabet = alphabet
        self.final_states = final_states
        self.state_transition_matrix = state_transition_matrix

    def get_predecessor_states(self, state):
        return self.state_transition_matrix.get_predecessor_states(state)

    def get_predecessor_states_np(self, state):
        return self.state_transition_matrix.get_predecessor_states_np(state)

    def get_prepaths(self, depth, current_state, transposed_matrix=None):
        return self.state_transition_matrix.get_prepaths(depth, current_state, transposed_matrix)

    def get_prepaths_np(self, depth, current_state):
        return self.state_transition_matrix.get_prepaths_np(depth, current_state)

    def insert_state(self, state):
        return self.state_transition_matrix.insert_state(state)

    def insert_state_np(self, state):
        return self.state_transition_matrix.insert_state_np(state)

    def delta(self, state, letter):
        return self.state_transition_matrix.delta(state, letter)

    def delta_np(self, state, letter):
        return self.state_transition_matrix.delta_np(state, letter)

    def copy_delta(self, source, target):
        return self.state_transition_matrix.copy_delta(source, target)

    def set_transition(self, source, target, letter):
        self.state_transition_matrix.set_transition(source, target, letter)

    def increase_unambiguity_to_1(self):
        order = 1
        initial_states = list(self.states)
        for q in initial_states:
            print("Processing state: " + str(q))
            pre_paths = self.get_prepaths(order, q)
            while len(pre_paths) > 1:
                a = pre_paths[0]
                qa = q + str(a) + "_" + str(order)

                # add qa to matrix
                self.insert_state(qa)

                if q in self.final_states:
                    self.final_states.append(qa)

                self.copy_delta(q, qa)
                transposed_matrix = self.state_transition_matrix.transpose_matrix()
                for p in self.get_predecessor_states(q):
                    if (self.delta(p, a[-1]) == q) and (a[:-1] in self.get_prepaths(order - 1, p, transposed_matrix)):
                        self.state_transition_matrix.remove_transition(p, q, a[-1])
                        self.state_transition_matrix.add_transition(p, qa, a[-1])
                pre_paths.remove(a)
        self.state_transition_matrix.transform_to_np()

    def increase_unambiguity(self, order):
        new_matrix_shape = len(self.alphabet) * len(self.states)
        new_matrix = np.zeros(shape=[new_matrix_shape, new_matrix_shape])
        old_matrix = self.state_transition_matrix.matrix
        new_matrix[0:old_matrix.shape[0], 0:old_matrix.shape[1]] = old_matrix
        self.state_transition_matrix.matrix = new_matrix
        initial_states = list(self.states)
        for q in initial_states:
            print("Processing state: " + str(q))
            pre_paths = self.get_prepaths_np(order, q)
            while len(pre_paths) > 1:
                a = pre_paths[0]
                qa = q + str(a) + "_" + str(order)

                # add qa to matrix
                self.insert_state_np(qa)

                if q in self.final_states:
                    self.final_states.append(qa)

                self.copy_delta(q, qa)
                for p in self.get_predecessor_states_np(q):
                    if (self.delta_np(p, a[-1]) == q) and (a[:-1] in self.get_prepaths_np(order-1, p)):
                        self.state_transition_matrix.remove_transition_np(p, q, a[-1])
                        self.state_transition_matrix.add_transition_np(p, qa, a[-1])
                pre_paths.remove(a)
        # remove empty rows + columns
        new_matrix_shape = len(self.states)
        new_matrix = np.zeros(shape=[new_matrix_shape, new_matrix_shape])
        old_matrix = self.state_transition_matrix.matrix
        new_matrix = old_matrix[0:new_matrix.shape[0], 0:new_matrix.shape[1]]
        self.state_transition_matrix.matrix = new_matrix
