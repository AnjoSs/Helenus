import copy
import numpy as np


class State_Transition_Matrix:
    def __init__(self, states, alphabet, matrix):
        self.state_list = states
        self.alphabet = alphabet
        self.matrix = matrix

    def transform_to_np(self):
        new_matrix = np.zeros(shape=[len(self.state_list), len(self.state_list)])
        for row_idx, row in enumerate(self.matrix):
            for col_idx, col in enumerate(self.matrix[row_idx]):
                if col:
                    new_matrix[row_idx][col_idx] = col[0]
        self.matrix = new_matrix

    # TODO use transformed matrix instead?!
    def get_predecessor_states(self, state):
        predecessors = []
        state_idx = self.state_list.index(state)
        for i in range(0, len(self.state_list)):
            if self.matrix[i][state_idx]:
                predecessors.append(self.state_list[i])
        return predecessors

    def get_predecessor_states_np(self, state):
        predecessors = []
        state_idx = self.state_list.index(state)
        for col_idx, cell in enumerate(self.matrix.T[state_idx]):
            if cell != 0.0:
                predecessors.append(self.state_list[col_idx])
        return predecessors

    def delta_non_deterministic(self, matrix, state):
        next_states = []
        state_idx = self.state_list.index(state)
        for letter_array in matrix[state_idx]:
            next_states.append(self.state_list[matrix[state_idx].index(letter_array)])
        return next_states

    def get_paths(self, matrix, depth, current_state):
        if depth == 0:
            return [[]]

        paths = []
        state_idx = self.state_list.index(current_state)
        for letter_pos in range(0, len(self.state_list)):
            if matrix[state_idx][letter_pos]:
                letters = matrix[state_idx][letter_pos]

                for letter in letters:
                    next_state = self.state_list[letter_pos]
                    next_paths = self.get_paths(matrix, depth-1, next_state)
                    for next_path in next_paths:
                        next_path.append(letter)
                        paths.append(next_path)
        return paths

    def get_paths_np(self, matrix, depth, current_state):
        if depth == 0:
            return [[]]

        paths = []
        state_idx = self.state_list.index(current_state)
        for col_idx in range(0, len(self.state_list)):
            if matrix[state_idx][col_idx] != 0.0:
                letter = matrix[state_idx][col_idx]
                next_state = self.state_list[col_idx]
                next_paths = self.get_paths_np(matrix, depth-1, next_state)
                for next_path in next_paths:
                    next_path.append(letter)
                    paths.append(next_path)
        return paths

    def get_prepaths(self, depth, current_state, transposed_matrix=None):
        if not transposed_matrix:
            transposed_matrix = self.transpose_matrix()
        paths = self.get_paths(transposed_matrix, depth, current_state)
        unique_paths = []
        for p in paths:
            if p not in unique_paths:
                unique_paths.append(p)
        return unique_paths

    def get_prepaths_np(self, depth, current_state):
        paths = self.get_paths_np(self.matrix.T, depth, current_state)
        unique_paths = []
        for p in paths:
            if p not in unique_paths:
                unique_paths.append(p)
        return unique_paths

    def insert_state(self, state):
        self.state_list.append(state)
        self.matrix.append([])
        state_idx = self.state_list.index(state)
        len_state_list = len(self.state_list)
        for i in range(0, len_state_list):
            self.matrix[state_idx].append([])
            if i < len_state_list-1:
                self.matrix[i].append([])

    def insert_state_np(self, state):
        self.state_list.append(state)

    def delta(self, state, letter):
        row = self.matrix[self.state_list.index(state)]
        # if letter in row:
        #     return self.state_list[row.index(letter)]
        for col_idx, col in enumerate(row):
            if letter in col:
                return self.state_list[col_idx]

    def delta_np(self, state, letter):
        row = self.matrix[self.state_list.index(state)]
        for col_idx, col in enumerate(row):
            if col == letter:
                return self.state_list[col_idx]

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

    def add_transition_np(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)] = letter

    def remove_transition(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)].remove(letter)

    def remove_transition_np(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)] = 0.0
