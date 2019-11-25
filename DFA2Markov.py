# Find all input sequences of length depth that lead to the target state.
# Save them in paths.
def dfs(depth, v, path, target, paths, G, matrix):
    if depth == 0 and v == target:  # stop clause for successful branch
        flat_path = [item for sublist in path for item in sublist]
        if flat_path not in paths:
            paths.append(flat_path)
        return
    if depth == 0:  # stop clause for non successful branch
        return
    for u in Q:
        if v in G[u]:  # each vertex u such that (v,u) is an edge
            path.append(matrix[v][u])  # add the edge to current vertex to the path
            dfs(depth-1, u, path, target, paths, G, matrix)  # recursively check all paths for of shorter depth
            path.pop()  # remove last element


# Returns the resulting state when input_char is received in state start_state
def delta(start_state, input_char):
    for endState, wordList in matrix[start_state].items():
        for word in wordList:
            if word != "" and input_char == word[len(word) - 1]:
                return endState

# algorithm from paper
def main(Q, F, A, m, matrix):
    G = {}
    Q0 = Q
    for q in Q:
        # find predecessors of q
        G[q] = []
        for k, value in matrix.items():
            if value[q] != [""]:
                G[q].append(k)

    D = {}
    for q in Q:
        # find strings that lead to q of length m
        paths = []
        dfs(m, q, [], q, paths, G, matrix)
        D[q] = paths

    for q in Q0:
        while len(D[q]) > 1:
            a = D[q][0]
            qa = "Q" + str(D[q][0])
            # add qa to matrix
            qa_matrix_row = {}
            for state in Q:
                qa_matrix_row[state] = []
                matrix[state][qa] = []
            qa_matrix_row[qa] = []
            matrix[qa] = qa_matrix_row
            Q.append(qa)
            if q in F:
                F.append(qa)
            D[qa] = [a]
            # Dm1[qa] = [a[-1]]
            G[qa] = []
            for b in A:
                matrix[qa][delta(q, b)].append(b)
                G[delta(q, b)].append(qa)
            # for delta the the power of -(m-1)
            Dm1 = {}
            for y in Q:
                # find strings that lead to y of length m - 1
                paths = []
                dfs(m - 1, y, [], y, paths, G, matrix)
                Dm1[y] = paths
            for p in G[q]:
                if delta(p, a[-1]) == q and a[:-1] in Dm1[p]:
                    G[qa] = p
                    matrix[p][qa].append(a[-1])
                    matrix[p][q].remove(a[-1])
                    G[q].remove(p)
            for p in G[q]:
                if all(q != delta(p, x) for x in A):
                    G[q].remove(q)
            D[q].remove(a)
    print(Q)
    print(D)
    print(G)
    print(matrix)
    # TODO: sadly, not correct yet


# Test if algorithm returns the correct paths
def test_dfs():
    paths = []
    dfs(1, "A", [], "A", paths)
    assert paths == [["a"]]

    paths = []
    dfs(2, "A", [], "A", paths)
    assert paths == [["a", "a"], ["b", "a"]]

    paths = []
    dfs(4, "B", [], "B", paths)
    assert paths == [["b", "b", "b", "b"]]

    paths = []
    dfs(2, "B2", [], "B2", paths)
    assert paths == [["a", "b"], ["b", "b"]]

    paths = []
    dfs(3, "B2", [], "B2", paths)
    assert sorted(paths) == sorted([["a", "b", "b"], ["b", "b", "b"], ["a", "a", "b"], ["b", "a", "b"]])


Q = ["B", "A", "B2"]
F = ["A", "B2"]
A = {"a", "b"}
matrix = {"B": {"B": ["b"], "A": ["a"], "B2": [""]},
          "A": {"B": [""], "A": ["a"], "B2": ["b"]},
          "B2": {"B": [""], "A": ["a"], "B2": ["b"]}}
m = 2

# test_dfs()
main(Q, F, A, m, matrix)
