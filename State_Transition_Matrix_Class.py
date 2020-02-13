import copy

class State_Transition_Matrix:
    def __init__(self, states, alphabet, matrix):
        self.state_list = states
        self.alphabet = alphabet
        self.matrix = matrix

    # TODO use transformed matrix instead?!
    def get_predecessor_states(self, state):
        predecessors = []
        for i in range(0, len(self.state_list)):
            if self.matrix[i][self.state_list.index(state)]:
                predecessors.append(self.state_list[i])
        return predecessors


    def delta_non_deterministic(self, matrix, state):
        next_states = []
        #print('delta n d')
        for letter_array in matrix[self.state_list.index(state)]:
            #print(letter_array)
            next_states.append(self.state_list[matrix[self.state_list.index(state)].index(letter_array)])
            #print(next_states)
        #print('delta end')
        return next_states


    def get_paths(self, matrix, depth, current_state):
        if depth == 0:
            return ['']

        paths = []
        for letter_pos in range(0, len(matrix[self.state_list.index(current_state)]) - 1):
            if matrix[self.state_list.index(current_state)][letter_pos]:
                letters = matrix[self.state_list.index(current_state)][letter_pos]

                for letter in letters:
                    next_state = self.state_list[letter_pos]
                    next_paths = self.get_paths(matrix, depth-1, next_state)
                    for next_path in next_paths:
                        if next_path == '':
                            paths.append([letter])
                        else:
                            paths.append([next_path, letter])
        return paths

    def get_prepaths(self, depth, current_state):  # is still buggy
        transpose_matrix = self.transpose_matrix()
        paths = self.get_paths(transpose_matrix, depth, current_state)
        unique_paths = []
        for p in paths:
            if p not in unique_paths:
                unique_paths.append(p)
        if unique_paths == ['']:
            return [[]]
        return unique_paths

    def insert_state(self, state):
        self.state_list.append(state)
        self.matrix.append([])
        for i in range(0, len(self.state_list)):
            self.matrix[self.state_list.index(state)].append([])
            if i < len(self.state_list)-1:
                self.matrix[i].append([])

    def delta(self, state, letter):
        row = self.matrix[self.state_list.index(state)]
        if letter in row:
            return self.state_list[row.index(letter)]
        for col in row:
            if letter in col:
                return self.state_list[row.index(col)]

    def copy_delta(self, source, target):
        self.matrix[self.state_list.index(target)] = copy.deepcopy(self.matrix[self.state_list.index(source)])

    def transpose_matrix(self):
        # transposed_matrix = copy.deepcopy(self.matrix)
        # for row_idx in range(0, len(self.matrix)):
        #     for col_idx in range(0, len(self.matrix[0])):
        #         transposed_matrix[col_idx][row_idx] = copy.deepcopy(self.matrix[row_idx][col_idx])
        # return transposed_matrix

        transposed_matrix = []
        for original_col_id in range(0, len(self.matrix[0])):
            transposed_matrix.append([])
            for original_row_id in range(0, len(self.matrix)):
                transposed_matrix[original_col_id].append(self.matrix[original_row_id][original_col_id])
        return transposed_matrix


    def add_transition(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)].append(letter)

    def remove_transition(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)].remove(letter)
