import copy

class State_Transition_Matrix:
    def __init__(self, states, alphabet, matrix):
        self.state_list = states
        self.alphabet = alphabet
        self.matrix = matrix


    def get_predecessor_states(self, state):
        predecessors = []
        for i in range(0, len(self.state_list)):
            if self.matrix[i][self.state_list.index(state)] != []:
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

        #print('get_paths: ' + str(depth) + current_state)
        paths = []
        for letter_pos in range(0, len(matrix[self.state_list.index(current_state)])):
            #print(letter_pos)
            if matrix[self.state_list.index(current_state)][letter_pos] != []:
                letters = matrix[self.state_list.index(current_state)][letter_pos]
                #print(letters)

                for letter in letters:
                    #print(letter)
                    next_state = self.state_list[letter_pos]
                    #print(next_state)
                    next_paths = self.get_paths(matrix, depth-1, next_state)
                    #print(next_paths)
                    for next_path in next_paths:
                        #print(next_path)
                        #print(letter)
                        paths.append(next_path + letter)
        #print(paths)
        return paths


    def get_prepaths(self, depth, current_state): # is still buggy
        transpose_matrix = self.transpose_matrix()
        #print(transpose_matrix)
        return list(set(self.get_paths(transpose_matrix, depth, current_state)))


    def insert_state(self, state):
        #self.matrix.append([])
        #for i in range(0, len(self.state_list)):
        #    self.matrix[len(self.state_list)].append([])
        #    print(self.matrix)

        #self.state_list.append(state)
        #for i in range(0, len(self.state_list)):
        #    print(i)
        #    print(self.matrix[i])
        #    self.matrix[i].append([])
        #    print(self.matrix)


        self.state_list.append(state)
        self.matrix.append([])
        #print(self.matrix)
        for i in range(0, len(self.state_list)):
            self.matrix[self.state_list.index(state)].append([])
            #print(self.matrix)
            if i < len(self.state_list)-1:
                self.matrix[i].append([])
                #print(self.matrix)


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
        transposed_matrix = []
        #print(self.matrix)
        #print(range(len(self.matrix)))
        for column in range(len(self.matrix)):
            #print('column: ' + str(column))
            transposed_matrix.append([])
            #print(transposed_matrix)
            #print(self.matrix[column])
            #print(range(len(self.matrix[column])))
            for row in range(len(self.matrix[column])):
                #print(row)
                #print(transposed_matrix)
                transposed_matrix[column].append(self.matrix[row][column])
        return transposed_matrix


    def add_transition(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)].append(letter)

    def remove_transition(self, source, target, letter):
        self.matrix[self.state_list.index(source)][self.state_list.index(target)].remove(letter)
