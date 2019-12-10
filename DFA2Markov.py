# Find all input sequences of length depth that lead to the target state.
# Save them in paths.
def dfs(depth, current_state, path, target, paths, predecessor_dict, matrix):
    if depth == 0 and current_state == target:  # stop clause for successful branch
        flat_path = [item for sublist in path for item in sublist]
        if flat_path not in paths:
            paths.append(flat_path)
        return
    if depth == 0:  # stop clause for non successful branch
        return
    for u in states:
        if current_state in predecessor_dict[u]:  # each vertex u such that (v,u) is an edge
            path.append(matrix[current_state][u])  # add the edge to current vertex to the path
            dfs(depth - 1, u, path, target, paths, predecessor_dict, matrix)  # recursively check all paths for of shorter depth
            path.pop()  # remove last element


# Returns the resulting state when input_char is received in state start_state
def delta(start_state, input_char, matrix):
    for end_state, word_list in matrix[start_state].items():
        for word in word_list:
            if word != "" and input_char == word[-1]:
                return end_state


def update_pre_paths_dict(pre_paths_dict, predecessor_dict, order, matrix, states):
    for q in states:
        # find strings that lead to q of length order
        paths = []
        for t in states:
            dfs(order, t, [], q, paths, predecessor_dict, matrix)
        pre_paths_dict[q] = paths


# algorithm from paper
def increase_unambiguity(states, final_states, alphabet, order, matrix):
    predecessor_dict = {}
    initial_states = list(states)
    for q in states:
        # find predecessors of q
        predecessor_dict[q] = []
        for state, transitions in matrix.items():
            if transitions[q] != [""]:
                predecessor_dict[q].append(state)
    pre_paths_dict = {}
    update_pre_paths_dict(pre_paths_dict, predecessor_dict, order, matrix, states)

    for q in initial_states:
        while len(pre_paths_dict[q]) > 1:
            a = pre_paths_dict[q][1]
            qa = "Q" + str(pre_paths_dict[q][1])

            # add qa to matrix
            qa_matrix_row = {}
            for state in states:
                qa_matrix_row[state] = []
                matrix[state][qa] = []
            qa_matrix_row[qa] = []
            matrix[qa] = qa_matrix_row
            states.append(qa)
            if q in final_states:
                final_states.append(qa)
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
    #print(states)
    #print(pre_paths_dict)  # TODO: pre_paths_dict[Qab] empty - problem for higher orders?
    #print(predecessor_dict)
    #print(final_states)
    #print(matrix)

    #assert(matrix == {'B': {'B': ['b'], 'A': ['a'], 'B2': [''], "Q['a', 'a']": [], "Q['b', 'b']": []}, 'A': {'B': [''], 'A': [], 'B2': ['b'], "Q['a', 'a']": ['a'], "Q['b', 'b']": []}, 'B2': {'B': [''], 'A': ['a'], 'B2': [], "Q['a', 'a']": [], "Q['b', 'b']": ['b']}, "Q['a', 'a']": {'B': [], 'A': [], 'B2': ['b'], "Q['a', 'a']": ['a'], "Q['b', 'b']": []}, "Q['b', 'b']": {'B': [], 'A': ['a'], 'B2': [], "Q['a', 'a']": [], "Q['b', 'b']": ['b']}})


# Test if algorithm returns the correct paths
def test_dfs():
    test_matrix = {"B": {"B": ["b"], "A": ["a"], "B2": [""]},
                   "A": {"B": [""], "A": ["a"], "B2": ["b"]},
                   "B2": {"B": [""], "A": ["a"], "B2": ["b"]}}
    test_Q = {"B", "A", "B2"}
    G = {}
    for q in test_Q:
        # find predecessors of q
        G[q] = []
        for k, value in test_matrix.items():
            if value[q] != [""]:
                G[q].append(k)

    paths = []
    dfs(1, "A", [], "A", paths, G, test_matrix)
    assert paths == [["a"]]

    paths = []
    dfs(2, "A", [], "A", paths, G, test_matrix)
    assert paths == [["a", "a"], ["b", "a"]]

    paths = []
    dfs(4, "B", [], "B", paths, G, test_matrix)
    assert paths == [["b", "b", "b", "b"]]

    paths = []
    dfs(2, "B2", [], "B2", paths, G, test_matrix)
    assert paths == [["a", "b"], ["b", "b"]]

    paths = []
    dfs(3, "B2", [], "B2", paths, G, test_matrix)
    assert sorted(paths) == sorted([["a", "b", "b"], ["b", "b", "b"], ["a", "a", "b"], ["b", "a", "b"]])


states = ["B", "A", "B2"]
final_states = ["A", "B2"]
alphabet = {"a", "b"}
initial_matrix = {"B": {"B": ["b"], "A": ["a"], "B2": [""]},
                  "A": {"B": [""], "A": ["a"], "B2": ["b"]},
                  "B2": {"B": [""], "A": ["a"], "B2": ["b"]}}
order = 2

test_dfs()
#increase_unambiguity(states, final_states, alphabet, order, initial_matrix)
