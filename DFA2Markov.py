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
def delta(start_state, input_char, matrix):
    for endState, wordList in matrix[start_state].items():
        for word in wordList:
            if word != "" and input_char == word[-1]:
                return endState


def updateD(D, G, m, matrix, Q):
    for q in Q:
        # find strings that lead to q of length m
        paths = []
        for t in Q:
            dfs(m, t, [], q, paths, G, matrix)
        D[q] = paths


# algorithm from paper
def main(Q, F, A, m, matrix):
    G = {}
    Q0 = list(Q)
    for q in Q:
        # find predecessors of q
        G[q] = []
        for k, value in matrix.items():
            if value[q] != [""]:
                G[q].append(k)
    D = {}
    updateD(D, G, m, matrix, Q)

    for q in Q0:
        while len(D[q]) > 1:
            a = D[q][1]
            qa = "Q" + str(D[q][1])

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
            G[qa] = []

            for b in A:
                matrix[qa][delta(q, b, matrix)].append(b)
                G[delta(q, b, matrix)].append(qa)
                # TODO: Validate - do we need that?
                updateD(D, G, m, matrix, Q)

            # for delta to the power of -(m-1)
            Dm1 = {}
            for y in Q:
                # find strings that lead to y of length m - 1
                paths = []
                dfs(m - 1, y, [], y, paths, G, matrix)
                Dm1[y] = paths

            for p in G[q]:
                if delta(p, a[-1], matrix) == q and a[:-1] in Dm1[p]:
                    G[qa].append(p)
                    matrix[p][qa].append(a[-1])
                    matrix[p][q].remove(a[-1])
                    G[q].remove(p)

                    updateD(Dm1, G, m-1, matrix, Q)
            for p in G[q]:
                if all(q != delta(p, x, matrix) for x in A):
                    G[q].remove(q)
            D[q].remove(a)
    print(Q)
    print(D)  # TODO: D[Qab] empty - problem for higher orders?
    print(G)
    print(F)
    print(matrix)


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


Q = ["B", "A", "B2"]
F = ["A", "B2"]
A = {"a", "b"}
initial_matrix = {"B": {"B": ["b"], "A": ["a"], "B2": [""]},
                  "A": {"B": [""], "A": ["a"], "B2": ["b"]},
                  "B2": {"B": [""], "A": ["a"], "B2": ["b"]}}
m = 2

test_dfs()
main(Q, F, A, m, initial_matrix)
