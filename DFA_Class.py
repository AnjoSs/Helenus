class DFA:
    def __init__(self, states, start_state, alphabet, final_states, state_transition_matrix):
        self.states = states
        self.start_state = start_state
        self.alphabet = alphabet
        self.final_states = final_states
        self.state_transition_matrix = state_transition_matrix

    def get_predecessor_states(self, state):
        return self.state_transition_matrix.get_predecessor_states(state)

    def get_prepaths(self, depth, current_state, target): # wtf is the target?
        return self.state_transition_matrix.get_prepaths(depth, current_state, [], target, [])

    def insert_state(self, state):
        return self.state_transition_matrix.insert_state(state)

    def increase_unambiguity(self, order):
        initial_states = list(self.states)
        print(initial_states)
        for q in initial_states:
            pre_paths = self.get_prepaths(order, q, q)
            print(pre_paths)
            while len(pre_paths) > 1:
                a = pre_paths[0]
                qa = "Q" + str(pre_paths[0])

                # add qa to matrix
                self.states.append(qa)
                self.state_transition_matrix.insert_state(qa)

                if q in self.final_states:
                    self.final_states.append(qa)


                ### Todo
                pre_paths_dict[qa] = [a]
                predecessor_dict[qa] = []

                for b in alphabet:
                    matrix[qa][delta(q, b, matrix)].append(b)
                    predecessor_dict[delta(q, b, matrix)].append(qa)

                # for delta to the power of -(m-1)
                Dm1 = {}
                update_pre_paths_dict(Dm1, predecessor_dict, order - 1, matrix, states)

                for p in predecessor_dict[q]:
                    if delta(p, a[-1], matrix) == q and a[:-1] in Dm1[p]:
                        predecessor_dict[qa].append(p)
                        matrix[p][qa].append(a[-1])
                        matrix[p][q].remove(a[-1])
                        predecessor_dict[q].remove(p)

                        update_pre_paths_dict(Dm1, predecessor_dict, order - 1, matrix, states)
                for p in predecessor_dict[q]:
                    if all(q != delta(p, x, matrix) for x in alphabet):
                        predecessor_dict[q].remove(q)
                pre_paths_dict[q].remove(a)
