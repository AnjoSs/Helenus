import numpy as np

class State_Transition_Matrix:
    def __init__(self, states, matrix):
        self.state_list = states
        #print(self.state_list)
        #self.matrix = np.zeros((len(self.state_list), len(self.state_list)))
        #print("initialized Matrix with zeros:")
        #print(self.matrix)
        self.matrix = matrix

    def get_predecessor_states(self, state):
        predecessors = []
        for i in range(0, len(self.state_list)):
            if self.matrix[i][self.state_list.index(state)] != '':
                predecessors.append(self.state_list[i])
        return predecessors

    def get_prepaths(self, depth, current_state, path, target, paths): # is still buggy
        if depth == 0 and current_state == target:  # stop clause for successful branch
            flat_path = [item for sublist in path for item in sublist]
            if flat_path not in paths:
                paths.append(flat_path)
            return
        if depth == 0:  # stop clause for non successful branch
            return
        for u in self.state_list:
            if current_state in self.get_predecessor_states(current_state):  # each vertex u such that (v,u) is an edge
                path.append(self.matrix[self.state_list.index(u)][self.state_list.index(current_state)])  # add the edge to current vertex to the path
                self.get_prepaths(depth - 1, u, path, target, paths)  # recursively check all paths for of shorter depth
                path.pop()  # remove last element
        return paths # has also elements of shorter length

    def insert_state(self, state):
        self.state_list.append(state)
        self.matrix.append([])
        for i in range(0, len(self.state_list)):
            self.matrix[self.state_list.index(state)].append('')
            if i < len(self.state_list)-1:
                self.matrix[i].append('')

    def delta(self, state, letter):
        return self.state_list[self.matrix[state].index(letter)]

    def copy_delta(self, source, target):
        self.matrix[self.state_list.index(target)] = self.matrix[self.state_list.index(source)]
